import discordrpc

rpc = discordrpc.RPC.set_id(app_id=123456789)

rpc.set_activity(
      state="With timestamp!",
      details="Timestamp",
      timestamp=rpc.timestamp
    )

# REQUIRED !
rpc.run()
