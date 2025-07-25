import discordrpc
from discordrpc import Button

rpc = discordrpc.RPC(app_id=1234567891011)


rpc.set_activity(
      state="Made by Senophyx",
      details="Discord-RPC",
      buttons=[
        Button("Repository", "https://github.com/Senophyx/discord-rpc"),
        Button("Discord", "https://discord.gg/qpT2AeYZRN"),
      ]
    )



rpc.run()