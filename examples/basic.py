import DiscordRPC
import time

app_id = '825958235134754847'  # Application ID
rpc = DiscordRPC.RPC.Set_ID(app_id=app_id)

while True:
    rpc.set_activity(
      state="up to you", 
      details="up to you", 
      timestamp=rpc.timestamp(), 
      large_text="Competitive", 
      small_text="Radiant", 
      large_image="Valorant", 
      small_image="Radiant_logo"
    )
    time.sleep(600) # to update the PC, recommended: every 10 minutes or 600 seconds
