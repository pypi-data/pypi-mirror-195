from pprint import pprint
import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def get_executor(data):
    import importlib

    module = importlib.import_module("{}".format(data["path"]))
    executor = getattr(module, data["name"])
    type = data.get("type", "function")
    return executor, type


def get_node_data(query, proj={"_id": 0}):
    from scinode.database.client import scinodedb

    ndata = scinodedb["node"].find_one(query, proj)
    for key in ["properties"]:
        if ndata.get(key):
            ndata[key] = deserialize(ndata[key])
    return ndata


def serialize(ndata):
    if isinstance(ndata, list):
        for i in range(len(ndata)):
            ndata[i] = serialize_item(ndata[i])
    else:
        for key, data in ndata.items():
            ndata[key] = serialize_item(data)
    return ndata


def deserialize(ndata):
    # print("deserialize", ndata)
    if isinstance(ndata, list):
        for i in range(len(ndata)):
            ndata[i] = deserialize_item(ndata[i])
    else:
        for key, data in ndata.items():
            ndata[key] = deserialize_item(data)
    return ndata


def serialize_item(data):
    Executor, executor_type = get_executor(data["serialize"])
    data["value"] = Executor(data["value"])
    return data


def deserialize_item(data):
    Executor, executor_type = get_executor(data["deserialize"])
    data["value"] = Executor(data["value"])
    return data


def yaml_to_dict(node):
    """Convert yaml data into dict."""
    metadata = node.get("metadata", {})
    metadata["identifier"] = node.pop("identifier")
    node["metadata"] = metadata
    # properties
    properties = {}
    if node.get("properties"):
        for name, p in node["properties"].items():
            properties[name] = {"value": p}
    node["properties"] = properties
    return node


def to_edit_dict(node_full):
    import yaml

    # print("ntdata: ", ntdata)
    nd = {
        "identifier": node_full["metadata"]["identifier"],
        "name": node_full["name"],
        "uuid": node_full["uuid"],
        "state": node_full["state"],
        "action": node_full["action"],
        "description": node_full["description"],
        "metadata": {
            "daemon_name": node_full["metadata"]["daemon_name"],
        },
    }
    if node_full["metadata"]["node_type"].upper() == "REF":
        return nd
    # set node_full properties
    properties = node_full.get("properties")
    if properties:
        nd["properties"] = {}
        for name, p in properties.items():
            nd["properties"][name] = p["value"]
    # inputs
    nd["inputs"] = []
    for input in node_full["inputs"]:
        for link in input["links"]:
            link["to_socket"] = input["name"]
            nd["inputs"].append(link)
    return nd


def get_input_parameters_from_db(dbdata):
    """get inputs from database

    The inputs are the outputs of parent nodes and
    the properties of the node itself.

    Returns:
        _type_: _description_
    """
    # get data of the node itself
    paramters = deserialize(dbdata.get("properties"))
    # print("data: ", paramters)
    # get inputs sockets data
    inputs = dbdata.get("inputs")
    for input in inputs:
        # un-linked socket
        # print(input["links"])
        if len(input["links"]) == 0:
            logger.debug("un-linked socket")
            if input["name"] not in paramters:
                paramters[input["name"]] = {"value": None}
        elif len(input["links"]) == 1:
            # linked socket
            logger.debug("    single-linked socket")
            link = input["links"][0]
            results = get_data(query={"uuid": link["from_socket_uuid"]})
            print(
                "results of node {}, data uuid {}: ".format(
                    link["from_node"], link["from_socket_uuid"]
                ),
                results,
            )
            value = results["value"] if results is not None else None
            paramters[input["name"]] = {"value": value}
        # check multi-input
        elif len(input["links"]) > 1:
            # linked socket
            logger.debug("    multi-linked socket")
            paramters[input["name"]] = {"value": []}
            for link in input["links"]:
                results = get_data(query={"uuid": link["from_socket_uuid"]})
                value = results["value"] if results is not None else None
                # find the input socket based on socket name
                if isinstance(value, dict):
                    paramters[input["name"]]["value"].update(value)
                elif isinstance(value, list):
                    paramters[input["name"]]["value"].extend(value)
                else:
                    paramters[input["name"]]["value"].append(value)
        # print("Input {}".format(input["name"]), paramters[input["name"]])
    return paramters


def inspect_executor_arguments(parameters, args_keys, kwargs_keys):
    """Get the positional and keyword arguments

    Args:
        executor (_type_): _description_
        parameters (_type_): _description_
    """
    args = []
    kwargs = {}
    for key in args_keys:
        args.append(parameters[key]["value"])
    for key in kwargs_keys:
        kwargs[key] = parameters[key]["value"]
    return args, kwargs


def get_results(outputs):
    """Item data from database
    Returns:
        dict: _description_
    """
    from scinode.database.client import scinodedb
    from scinode.utils.node import deserialize_item

    results = []
    for output in outputs:
        query = {"uuid": output["uuid"]}
        data = scinodedb["data"].find_one(query, {"_id": 0})
        if data:
            results += [deserialize_item(data)]
        else:
            results += [data]
    return results


def get_data(query):
    from scinode.database.db import scinodedb

    data = scinodedb["data"].find_one(query)
    # print("get_data: ", data)
    if data is None:
        return data
    data = deserialize_item(data)
    # print("get_data: ", data)
    return data


def write_log(uuid, log, database=True):
    from scinode.database.client import scinodedb

    if database:
        old_log = scinodedb["node"].find_one({"uuid": uuid}, {"_id": 0, "log": 1})[
            "log"
        ]
        log = old_log + log
        newvalues = {"$set": {"log": log}}
        scinodedb["node"].update_one({"uuid": uuid}, newvalues)


def node_shape(self, data):
    """_summary_

    Args:
        data (_type_): _description_


    =========
    |       o
    |       |
    |t      |
    |x      |
    o       |
    ========
    """
    pass
