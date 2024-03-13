import discordrpc
from discordrpc.button import Button

rpc = discordrpc.RPC(app_id=1234567891011)

button = Button(
  button_one_label="Repository",
  button_one_url="https://github.com/Senophyx/discord-rpc",
  button_two_label="Discord Server",
  button_two_url="https://discord.gg/qpT2AeYZRN"
  )

rpc.set_activity(
      state="Made by Senophyx",
      details="Discord-RPC",
      buttons=button
    )



rpc.run()