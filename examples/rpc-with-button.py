import discordrpc
from discordrpc import button

rpc = discordrpc.RPC(app_id=1234567891011)


rpc.set_activity(
      state="Made by Senophyx",
      details="Discord-RPC",
      buttons=[
        button("Repository", "https://github.com/Senophyx/discord-rpc"),
        button("Discord", "https://discord.gg/qpT2AeYZRN"),
      ]
    )


rpc.run()