import discordrpc
import time

rpc = discordrpc.RPC(app_id=123456789)

print("Setting activity...")
rpc.set_activity(
    state="Working hard",
    details="Coding in Python",
    large_image="eternomm_logo",
    large_text="EterNomm"
)

# Wait 10 seconds to let you see the activity on your profile
time.sleep(10)

print("Clearing activity...")
rpc.clear() # This removes the Rich Presence from your profile without disconnecting

print("Activity cleared! Disconnecting in 5 seconds...")
time.sleep(5)
rpc.disconnect()
