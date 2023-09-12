import discordrpc

rpc = discordrpc.RPC.set_id(app_id=123456789101112)

# Upload your image(s) here:
# https://discord.com/developers/applications/<APP ID>/rich-presence/assets

rpc.set_activity(
      state="pip install discord-rpc",
      details="Discord-RPC by LyQuid",
      large_image="eternomm_logo", # Make sure you are using the same name that you used when uploading the image
      large_text="EterNomm",
      small_image="github", # Make sure you are using the same name that you used when uploading the image
      small_text="Github"
    )


# REQUIRED !
rpc.run()
