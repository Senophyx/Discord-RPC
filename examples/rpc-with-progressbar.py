import discordrpc
from discordrpc import Activity, Progressbar


rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    state="With Progressbar",
    details="Music",
    act_type=Activity.Listening,
    progressbar=Progressbar(50, 200)
)

rpc.run()
