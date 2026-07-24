import discordrpc

rpc = discordrpc.RPC(app_id=123456789)

print(rpc.assets.names)

for asset in rpc.assets:
    print(asset.url)

rpc.set_activity(
    state="Assets example",
    large_image=rpc.assets.get("cat")
)
rpc.run()
