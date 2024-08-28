import discordrpc

rpc = discordrpc.RPC(app_id=1234567891011)

button = discordrpc.Buttons(
    discordrpc.Button(label="Repository", url="https://github.com/Senophyx/discord-rpc"),
    discordrpc.Button(label="Discord Server", url="https://discord.gg/qpT2AeYZRN")
)

rpc.set_activity(
    state="Made by Senophyx",
    details="Discord-RPC",
    buttons=button
)

rpc.run()
