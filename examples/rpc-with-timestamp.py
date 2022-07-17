import DiscordRPC

rpc = DiscordRPC.RPC.Set_ID(app_id=123456789)

rpc.set_activity(
      state="With timestamp!",
      details="Timestamp",
      timestamp=rpc.timestamp()
    )

# REQUIRED !
rpc.run()
