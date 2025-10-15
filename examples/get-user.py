import discordrpc

rpc = discordrpc.RPC(app_id=123456789)

print(rpc.User.id)
print(rpc.User.name)
print(f"@{rpc.User.username}")
print(rpc.User.avatar)

rpc.run()
