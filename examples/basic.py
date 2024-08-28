import discordrpc

rpc = discordrpc.RPC(app_id=12345678910)

rpc.set_activity(
    state="A super simple rpc",
    details="simple RPC"
)

# Required if you only run Discord RPC on this file or current instance.
rpc.run()
