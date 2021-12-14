import DiscordRPC
import time 

rpc = DiscordRPC.RPC.Set_ID(app_id=12345678910)

rpc.set_activity(
      state="Rank : Radiant",
      details="Competitive",
      timestamp=rpc.timestamp()
    )

while True:
    time.sleep(600) # to update the RPC, recommended: every 10 minutes or 600 seconds
