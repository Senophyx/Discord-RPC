import discordrpc


# Set show_output to True to get RPC output (Like whether RPC works well or not)
# Default = True
rpc = discordrpc.RPC(app_id=123456789101112, output=True)

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
