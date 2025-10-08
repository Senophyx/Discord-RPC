import discordrpc
from discordrpc import Activity
from discordrpc.utils import ProgressBar


rpc = discordrpc.RPC(app_id=1234567891011)

rpc.set_activity(
    state="With Progressbar",
    details="Music",
    act_type=Activity.Listening,
    **ProgressBar(50, 200)
)

rpc.run()
