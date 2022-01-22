import DiscordRPC
import time 

rpc = DiscordRPC.RPC.Set_ID(app_id=123456789)

while True:
    current_app = DiscordRPC.GCAR()
    rpc.set_activity(
          state="pip install discord-rpc",
          details=current_app,
          timestamp=rpc.timestamp()
        )

    time.sleep(15)
