import discordrpc

rpc = discordrpc.RPC(app_id=123456789)

# You can use an uploaded asset key from your Discord Developer Portal,
# OR a direct external URL to an image (supports PNG, JPEG, WebP, GIF, AVIF).
# Upload assets here: https://discord.com/developers/applications/<APP ID>/rich-presence/assets

rpc.set_activity(
      state="pip install discord-rpc",
      details="Discord-RPC by Senophyx",
      
      # Using an uploaded asset key
      large_image="eternomm_logo", 
      large_text="EterNomm",
      
      # Using an external HTTP URL (Example: animated GIF)
      small_image="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", 
      small_text="Github"
    )

rpc.run()
