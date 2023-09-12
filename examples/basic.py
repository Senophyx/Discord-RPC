import discordrpc

rpc = discordrpc.RPC.set_id(app_id=12345678910)

rpc.set_activity(
      state="A super simple rpc",
      details="simple RPC"
    )

# REQUIRED !
rpc.run()
