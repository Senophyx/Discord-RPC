import discordrpc


# Set show_output to True to get RPC output (Like whether RPC works well or not)
# Default = True
rpc = discordrpc.RPC(app_id=123456789101112, output=True)


button_list = [
  discordrpc.button("Repository", "https://github.com/Senophyx/discord-rpc"),
  discordrpc.button("Discord Server", "https://discord.gg/qpT2AeYZRN")
]

rpc.set_activity(
      state="Made by Senophyx",
      details="Discord-RPC",
      buttons=button_list
    )


rpc.run()