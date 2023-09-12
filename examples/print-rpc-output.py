import discordrpc

rpc = discordrpc.RPC.set_id(app_id=123456789101112)

rpc.show_output = True # Set show_output to True to get RPC output (Like whether RPC works well or not)

button = discordrpc.button(
  button_one_label="Repository",
  button_one_url="https://github.com/LyQuid12/discord-rpc",
  button_two_label="Discord Server",
  button_two_url="https://discord.gg/qpT2AeYZRN"
  )

rpc.set_activity(
      state="Made by LyQuid",
      details="Discord-RPC",
      buttons=button
    )

# REQUIRED !
rpc.run()
