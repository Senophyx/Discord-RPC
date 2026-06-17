import discordrpc
from discordrpc import button
import time

# Create RPC instance
rpc = discordrpc.RPC(app_id=123456789)

# Get current time for the timestamp
current_time = int(time.time())

# Set a complex activity combining all features: text, images, timestamps, party, and buttons
rpc.set_activity(
    state="In an Epic Boss Fight",
    details="Level 99 - The Abyss",
    
    # Images
    large_image="eternomm_logo", 
    large_text="Playing EterNomm",
    small_image="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", 
    small_text="Using Discord-RPC",
    
    # Timestamps (Time elapsed since start)
    ts_start=current_time,
    
    # Party details
    party_id="boss_raid_554",
    party_size=[3, 5], # 3 players out of 5 max
    
    # Secrets for "Ask to Join" (Required for party features)
    join_secret="raid_invite_xyz",
    spectate_secret="raid_spectate_xyz",
    match_secret="raid_match_xyz",
    
    # Buttons (Max 2)
    buttons=[
        button("Join Raid", "https://discord.gg/qpT2AeYZRN"),
        button("Source Code", "https://github.com/Senophyx/discord-rpc")
    ]
)

print("Complex RPC has been set!")
rpc.run()
