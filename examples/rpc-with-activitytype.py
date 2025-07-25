import discordrpc
from discordrpc import Activity
import time


rpc = discordrpc.RPC(app_id=123456789)


current_time = int(time.time())
finish_time = current_time + 200

rpc.set_activity(
      state="With activity type",
      details="Music",
      act_type=Activity.Listening,
      ts_start=current_time,
      ts_end=finish_time
)


rpc.run()
