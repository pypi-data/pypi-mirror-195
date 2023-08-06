from scinode.utils.db import push_message
from scinode.profile.profile import profile_datas
from scinode.engine.config import broker_queue_name

# load celery tasks
if profile_datas["celery"]:
    from scinode.engine.celery import tasks


def send_message_to_queue(queue, msg):
    if profile_datas["celery"]:
        tasks.process_message.apply_async(queue=queue, args=(msg,))
    else:
        push_message(queue, msg)


def launch_nodetree(queue, nodetree_uuid):
    if profile_datas["celery"]:
        tasks.launch_nodetree.apply_async(
            queue=broker_queue_name, args=(nodetree_uuid,)
        )
    else:
        push_message(broker_queue_name, f"{nodetree_uuid},nodetree,action:LAUNCH")


def launch_node(queue, nodetree_uuid, node_name):
    if profile_datas["celery"]:
        tasks.launch_node.apply_async(queue=queue, args=(nodetree_uuid, node_name))
    else:
        push_message(queue, f"{nodetree_uuid},node,{node_name}:action:LAUNCH")


def gather_node(queue, nodetree_uuid, node_name):
    if profile_datas["celery"]:
        tasks.gather_node.apply_async(queue=queue, args=(nodetree_uuid, node_name))
    else:
        push_message(queue, f"{nodetree_uuid},node,{node_name}:action:GATHER")
