import DiscordRPC
import time 

rpc = DiscordRPC.RPC.Set_ID(app_id=123456789101112)

while True:
    rpc.set_activity(
      state="Rank : Radiant",
      details="Competitive",
      timestamp=rpc.timestamp()
    )
    time.sleep(600) # to update the PC, recommended: every 10 minutes or 600 seconds
