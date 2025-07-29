import discordrpc
from discordrpc import use_local_time


rpc = discordrpc.RPC(app_id=1397914682659963050)

rpc.set_activity(
    state="Wow! It's shows my clock",
    details="Local time example",
    **use_local_time()
)

rpc.run()
