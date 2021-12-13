import DiscordRPC
import time

app_id = 'app id'  # Application ID (cannot int)
rpc = DiscordRPC.RPC.Set_ID(app_id=app_id)

while True:
    rpc.set_activity(
      state="Rank : Radiant", 
      details="Competitive", 
      timestamp=rpc.timestamp()
    )
    time.sleep(600) # to update the PC, recommended: every 10 minutes or 600 seconds
