### Basically it's "print-rpc-output.py" but with more informative output :)

import discordrpc

# Add debug=True to get more outputs
# Default = False
rpc = discordrpc.RPC(app_id=123456789, debug=True)

rpc.set_activity(
      state="A super simple rpc",
      details="simple RPC"
    )


rpc.run()