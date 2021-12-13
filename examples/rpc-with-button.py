import DiscordRPC
import time 

rpc = DiscordRPC.RPC.Set_ID(app_id="919914790556672031") # Application ID must string

button = DiscordRPC.button(button_one_label="Repository", button_one_url="https://github.com/LyQuid12/discord-rpc", button_two_label="Discord Server", button_two_url="https://discord.gg/qpT2AeYZRN")

while True:
    rpc.set_activity(
      state="Made by LyQuid",
      details="Discord-RPC",
      timestamp=rpc.timestamp(),
      buttons=button
    )
    time.sleep(600) # to update the PC, recommended: every 10 minutes or 600 seconds
