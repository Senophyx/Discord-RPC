import discordrpc
from discordrpc import Activity, Progressbar


rpc = discordrpc.RPC(app_id=1397914682659963050)

rpc.set_activity(
    state="With Progressbar",
    details="Music",
    act_type=Activity.Listening,
    **Progressbar(50, 200)
)

rpc.run()
