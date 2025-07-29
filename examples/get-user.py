import discordrpc

rpc = discordrpc.RPC(app_id=1397914682659963050)

print(rpc.User.id)
print(rpc.User.name)
print(f"@{rpc.User.username}")
print(rpc.User.avatar)

rpc.run()
