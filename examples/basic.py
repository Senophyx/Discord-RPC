import DiscordRPC

rpc = DiscordRPC.RPC.Set_ID(app_id=12345678910)

rpc.set_activity(
      state="A super simple rpc",
      details="simple RPC"
    )

# REQUIRED !
rpc.run()
