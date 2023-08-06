from scinode.core import DBItem
from scinode.engine.send_to_queue import send_message_to_queue
from scinode.engine.config import broker_queue_name
import traceback
import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class EngineNode(DBItem):
    """EngineNode Class.
    Process the node with the data from the database.
    It can be called by the daemon or called manually.

    uuid: str
        uuid of the node.
    name: str
        name of the node.

    Example:
    >>> # load node data from database
    >>> query = {"uuid": "your-node-uuid"}
    >>> dbdata = scinodedb["node"].find_one(query)
    >>> node = EngineNode(uuid=dbdata["uuid"])  # , self.daemon_name)
    >>> future = node.process(pool, future)

    """

    db_name: str = "node"

    def __init__(self, uuid=None, dbdata=None, daemon_name="localhost") -> None:
        """init a instance

        Args:
            uuid (str, optional): uuid of the node.
                Defaults to None.
            dbdata (dict, optional): data of the node from database.
                Defaults to None.
        """
        # print("Init Node Engine...")
        if dbdata:
            uuid = dbdata["uuid"]
        super().__init__(uuid)
        self.record = self.dbdata
        self.name = self.record["name"]
        self.daemon_name = daemon_name
        self.id = self.record["id"]
        self.nodetree_uuid = self.record["metadata"]["nodetree_uuid"]
        self.scattered_from = self.record["metadata"]["scattered_from"]
        self.scattered_label = self.record["metadata"]["scattered_label"]

    def process(self, pool, future=None, action=None):
        """process data based on the action flag.

        Args:
            pool (ThreadPoolExecutor): Pool used to submit job
            future (concurrent.futures.Future, optional): Defaults to None.

        Returns:
            oncurrent.futures.Future: _description_
        """
        print(f"Node Engine, process: {self.name}")
        try:
            future = self.apply_action(pool, future, action=action)
        except Exception:
            import traceback

            error = traceback.format_exc()
            log = "xxxxxxxxxx Failed xxxxxxxxxx\nNode {} failed due to: {}".format(
                self.name, error
            )
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
            )
            self.update_db_keys({"error": str(error)})
            self.write_log(log)

        return future

    def apply_action(self, pool, future=None, action=None):
        """Apply node action

        Args:
            pool (dict): _description_
            future (future, optional): _description_. Defaults to None.
            action (_type_, optional): _description_. Defaults to None.

        Returns:
            future: _description_
        """
        if not action:
            action = self.record["action"]
        log = "\nDaemon: {}\n".format(self.daemon_name)
        log += "\nAction: {}\n".format(action)
        self.write_log(log)
        if action is None or action.upper() == "NONE":
            return
        elif action.upper() == "LAUNCH":
            print(type(pool))
            future = self.launch(pool)
        elif action.upper() == "GATHER":
            self.gather()
            return None
        elif action.upper() == "CANCEL":
            self.cancel(future)
            return None
        else:
            log = "\nAction {} is not supported.".format(self.action)
            self.write_log(log)
        return future

    def launch(self, pool=None):
        """Launch node"""
        from scinode.utils.node import (
            get_input_parameters_from_db,
            inspect_executor_arguments,
            get_executor,
        )

        # code here
        dbdata = self.record
        log = "\nLaunch node {}, {}\n".format(dbdata["id"], dbdata["name"])
        parameters = get_input_parameters_from_db(dbdata)
        # print("parameters: ", parameters)
        args, kwargs = inspect_executor_arguments(
            parameters, dbdata["metadata"]["args"], dbdata["metadata"]["kwargs"]
        )
        # print("  Parameters: ", parameters)
        log += "  args, kwargs {} {} \n".format(args, kwargs)
        Executor, executor_type = get_executor(self.dbdata["executor"])
        # print("  Executor: ", Executor)
        # future = pool.submit(executor, parameters)
        # self.action = "NONE"
        # self.state = "RUNNING"
        send_message_to_queue(
            broker_queue_name,
            f"{self.nodetree_uuid},node,{self.name}:state:RUNNING",
        )
        if executor_type.upper() == "CLASS":
            # For user defined node, we can add daemon name to kwargs
            executor = Executor(
                *args, **kwargs, dbdata=dbdata, daemon_name=self.daemon_name
            )
            future = pool.submit(executor.run)
        else:
            future = pool.submit(Executor, *args, **kwargs)
        future.add_done_callback(self.check_future_done)
        self.write_log(log)
        return future

    def gather(self):
        """gather result from child nodes"""
        from scinode.utils.node import get_results
        from scinode.utils.db import replace_one
        from scinode.database.client import scinodedb
        from scinode.database.client import db_node

        dbdata = self.dbdata
        outputs = dbdata["outputs"]
        no = len(outputs)
        # init the results as a list
        for i in range(no):
            outputs[i]["value"] = []
        # fetch results from children
        children = db_node.find(
            {"metadata.scattered_from": dbdata["uuid"]},
            {"uuid": 1, "name": 1, "outputs": 1},
        )
        for child in children:
            child_results = get_results(child["outputs"])
            for i in range(no):
                value = child_results[i]["value"]
                outputs[i]["value"].append(value)
        # print("  Save results: ", results)
        for i in range(no):
            replace_one(outputs[i], scinodedb["data"])
        log = f"Node: {dbdata['name']} is gathered.\n"
        log += "Results: {}".format(outputs)
        # self.state = "FINISHED"
        # self.action = "NONE"
        send_message_to_queue(
            broker_queue_name,
            f"{self.nodetree_uuid},node,{self.name}:state:FINISHED",
        )
        self.write_log(log)

    @property
    def input_node_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        from scinode.utils.node import get_input_node_data
        from scinode.database.client import db_node

        nodes = get_input_node_data(self.record, db_node)
        # print("Total: {} parent nodes.".format(len(nodes)))
        return nodes

    def check_future_done(self, future):
        """Check if node finished

        Args:
            future (_type_): _description_

        Raises:
            Exception: _description_
        """
        log = "\n  Check result for Node: {}, {}.".format(self.id, self.name)
        if future.exception() is not None:
            error = traceback.format_exc()
            log += "\nxxxxxxxxxx Failed xxxxxxxxxx\n{}".format(error)
            # self.state = "FAILED"
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
            )
            self.update_db_keys({"error": str(error)})
            self.write_log(log)
            return
        elif future.cancelled():
            log == "\n  Job was cancelled"
            # self.state = "CANCELLED"
            # self.action = "NONE"
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
            )
            self.update_db_keys({"error": "Job was cancelled"})
            self.write_log(log)
            return
        else:
            # job is done, try to get result
            try:
                self.save_result(future)
            except Exception:
                error = traceback.format_exc()
                log += "\nxxxxxxxxxx Failed xxxxxxxxxx\nFetch results from future failed, due to: {}".format(
                    error
                )
                # self.state = "FAILED"
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
                )
                self.update_db_keys({"error": str(error)})
                self.write_log(log)
                return

    def save_result(self, future):
        """Save result to database."""
        from scinode.utils.node import get_executor
        from scinode.database.client import scinodedb
        from scinode.utils.db import replace_one

        future_results = future.result()
        log = "\n    results from future: {}".format(future_results)
        dbdata = self.dbdata
        outputs = dbdata["outputs"]
        no = len(outputs)
        # update results with the future_results
        if not isinstance(future_results, tuple):
            future_results = (future_results,)
        if len(future_results) != no:
            # self.state = "FAILED"
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
            )
            log += """xxxxxxxxxx Error xxxxxxxxxx\nNumber of results from future:
    {} does not equal to number of sockets: {}.\n""".format(
                len(future_results), no
            )
            self.write_log(log)
            raise Exception(log)
        for i in range(no):
            Executor, executor_type = get_executor(outputs[i]["serialize"])
            outputs[i]["value"] = Executor(future_results[i])
            # print("  Save results: ", outputs[i])
            replace_one(outputs[i], scinodedb["data"])
        # self.state = "FINISHED"
        # self.action = "NONE"
        send_message_to_queue(
            broker_queue_name,
            f"{self.nodetree_uuid},node,{self.name}:state:FINISHED",
        )
        log += "\n  Node: {} is finished".format(dbdata["name"])
        print("\n  Node: {} is finished".format(dbdata["name"]))
        self.write_log(log)

    def __repr__(self) -> str:
        s = ""
        s += 'EngineNode(name="{}", uuid="{}", nodetree_uuid = {},\
scattered_from = {}, state={}, action={})'.format(
            self.name,
            self.uuid,
            self.nodetree_uuid,
            self.state,
            self.action,
        )
        return s

    def write_log(self, log, daemon=False, database=True):
        if daemon:
            print(log)
        if database:
            old_log = self.db.find_one({"uuid": self.uuid}, {"_id": 0, "log": 1})["log"]
            log = old_log + log
            self.update_db_keys({"log": log})
