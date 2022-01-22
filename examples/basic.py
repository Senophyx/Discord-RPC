import DiscordRPC
import time 

rpc = DiscordRPC.RPC.Set_ID(app_id=12345678910)

rpc.set_activity(
      state="pip intall discord-rpc",
      details="Discord RPC",
      timestamp=rpc.timestamp()
    )
