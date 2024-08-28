import discordrpc

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    state="With timestamp!",
    details="Timestamp",
    ts_start=discordrpc.get_timestamp(),  # Timestamp start
    ts_end=1752426021  # Timestamp end
)

rpc.run()
