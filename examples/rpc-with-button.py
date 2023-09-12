import discordrpc

rpc = discordrpc.RPC.set_id(app_id=1234567891011)

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
