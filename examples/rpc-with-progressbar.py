import discordrpc
from discordrpc import Progressbar


rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    state="With Progressbar",
    details="Music",
    progressbar=Progressbar(50, 200)
)

rpc.run()
