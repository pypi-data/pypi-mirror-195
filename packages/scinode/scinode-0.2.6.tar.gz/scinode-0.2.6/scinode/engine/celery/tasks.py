"""
TODO pass default daemon seting to task, e.g. work_dir
"""
from scinode.engine.celery.app import app
from scinode.engine.config import broker_queue_name
import traceback


@app.task
def get_daemon_status():
    """should broadcast to all daemon"""
    pass


@app.task
def process_message(msg):
    from scinode.engine.engine import Engine

    en = Engine()
    en.process(msg)
    return None


@app.task
def launch_nodetree(uuid):
    from scinode.engine.nodetree_engine import EngineNodeTree

    en = EngineNodeTree(uuid)
    en.launch_nodetree()
    return None


@app.task
def launch_node(nodetree_uuid, node_name):
    """Launch node"""
    from scinode.utils.node import (
        get_input_parameters_from_db,
        inspect_executor_arguments,
        get_executor,
        write_log,
    )
    from scinode.database.client import scinodedb
    from scinode.engine.send_to_queue import send_message_to_queue

    # get node data
    ntdata = scinodedb["nodetree"].find_one(
        {"uuid": nodetree_uuid}, {f"nodes.{node_name}": 1, "metadata.daemon_name": 1}
    )
    ntdata["uuid"] = nodetree_uuid
    node_uuid = ntdata["nodes"][node_name]["uuid"]
    dbdata = scinodedb["node"].find_one({"uuid": node_uuid})
    log = "\nLaunch node {}, {}\n".format(dbdata["id"], dbdata["name"])
    try:
        parameters = get_input_parameters_from_db(dbdata)
        # print("parameters: ", parameters)
        args, kwargs = inspect_executor_arguments(
            parameters, dbdata["metadata"]["args"], dbdata["metadata"]["kwargs"]
        )
        # print("  Parameters: ", parameters)
        log += "  args, kwargs {} {} \n".format(args, kwargs)
        Executor, executor_type = get_executor(dbdata["executor"])
    except Exception as error:
        error = traceback.format_exc()
        log += "\nxxxxxxxxxx Failed xxxxxxxxxx\n{}".format(error)
        # self.state = "FAILED"
        send_message_to_queue(
            broker_queue_name,
            f"{nodetree_uuid},node,{node_name}:state:FAILED",
        )
        write_log(node_uuid, log)
        return
    msgs = f"{nodetree_uuid},node,{node_name}:state:RUNNING"
    send_message_to_queue(broker_queue_name, msgs)
    try:
        if executor_type.upper() == "CLASS":
            # For user defined node, we can add daemon name to kwargs
            executor = Executor(
                *args,
                **kwargs,
                dbdata=dbdata,
            )
            future = executor.run()
        else:
            future = Executor(*args, **kwargs)
        save_result(ntdata, dbdata, future)
        msgs = f"{nodetree_uuid},node,{node_name}:state:FINISHED"
        send_message_to_queue(broker_queue_name, msgs)
        log += "\n  Node: {} is finished".format(dbdata["name"])
        print("\n  Node: {} is finished".format(dbdata["name"]))
        write_log(node_uuid, log)
    except Exception as error:
        error = traceback.format_exc()
        log += "\nxxxxxxxxxx Failed xxxxxxxxxx\n{}".format(error)
        # self.state = "FAILED"
        send_message_to_queue(
            broker_queue_name,
            f"{nodetree_uuid},node,{node_name}:state:FAILED",
        )
        write_log(node_uuid, log)


@app.task
def gather_node(nodetree_uuid, node_name):
    """gather result from child nodes"""
    # gather results
    from scinode.utils.node import get_results, write_log
    from scinode.utils.db import replace_one
    from scinode.database.client import scinodedb
    from scinode.engine.send_to_queue import send_message_to_queue

    # get node data
    ntdata = scinodedb["nodetree"].find_one(
        {"uuid": nodetree_uuid}, {f"nodes.{node_name}": 1, "metadata.daemon_name": 1}
    )
    ntdata["uuid"] = nodetree_uuid
    node_uuid = ntdata["nodes"][node_name]["uuid"]
    dbdata = scinodedb["node"].find_one({"uuid": node_uuid})
    log = "Gather node {}, {}\n".format(dbdata["id"], dbdata["name"])
    outputs = dbdata["outputs"]
    no = len(outputs)
    # init the results as a list
    for i in range(no):
        outputs[i]["value"] = []
    # fetch results from children
    children = scinodedb["node"].find(
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
        f"{nodetree_uuid},node,{node_name}:state:FINISHED",
    )
    write_log(dbdata["uuid"], log)


def save_result(ntdata, dbdata, future_results):
    """Save result to database."""
    from scinode.utils.node import get_executor, write_log
    from scinode.database.client import scinodedb
    from scinode.utils.db import replace_one
    from scinode.engine.send_to_queue import send_message_to_queue

    log = "\n    results from future: {}".format(future_results)
    outputs = dbdata["outputs"]
    no = len(outputs)
    nodetree_uuid = ntdata["uuid"]
    # update results with the future_results
    if not isinstance(future_results, tuple):
        future_results = (future_results,)
    if len(future_results) != no:
        # self.state = "FAILED"
        send_message_to_queue(
            broker_queue_name,
            f"{nodetree_uuid},node,{dbdata['name']}:state:FAILED",
        )
        log += """xxxxxxxxxx Error xxxxxxxxxx\nNumber of results from future:
{} does not equal to number of sockets: {}.\n""".format(
            len(future_results), no
        )
        write_log(dbdata["uuid"], log)
        raise Exception(log)
    for i in range(no):
        Executor, executor_type = get_executor(outputs[i]["serialize"])
        outputs[i]["value"] = Executor(future_results[i])
        # print("  Save results: ", outputs[i])
        replace_one(outputs[i], scinodedb["data"])
    write_log(dbdata["uuid"], log)


if __name__ == "__main__":
    import logging

    worker = app.Worker()
    worker.setup_defaults(loglevel=logging.INFO)
    worker.setup_queues("localhost")
    worker.start()
