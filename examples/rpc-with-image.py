import DiscordRPC
import time 

rpc = DiscordRPC.RPC.Set_ID(app_id=123456789101112) # Application ID must string

# Upload your image(s) here:
# https://discordapp.com/developers/applications/<APP ID>/rich-presence/assets

button = DiscordRPC.button(
  button_one_label="Repository",
  button_one_url="https://github.com/LyQuid12/discord-rpc",
  button_two_label="Discord Server",
  button_two_url="https://discord.gg/qpT2AeYZRN"
  )

rpc.set_activity(
      state="pip install discord-rpc",
      details="Discord-RPC by LyQuid",
      timestamp=rpc.timestamp(),
      large_image="eternomm_logo", # Make sure you are using the same name that you used when uploading the image
      large_text="EterNomm",
      small_image="github", # Make sure you are using the same name that you used when uploading the image
      small_text="Github",
      buttons=button
    )
print(rpc.output()) 
 
while True:
    time.sleep(15)
