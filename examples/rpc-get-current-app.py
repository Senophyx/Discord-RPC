"""
GCAR function currently disabled due a bug.
"""


import DiscordRPC
import time 

rpc = DiscordRPC.RPC.Set_ID(app_id=123456789)

while True:
    current_app = DiscordRPC.GCAR()
    rpc.set_activity(
          state="pip install discord-rpc",
          details=current_app
        )

    time.sleep(15)

# run() not required if using while loop (only if you use GCAR method.)
