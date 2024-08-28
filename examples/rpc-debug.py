# Basically it's "print-rpc-output.py" but with more informative output :)
import logging

import discordrpc

# Add debug=True to get more outputs
# Default = False
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s :: [%(levelname)s @ %(filename)s.%(funcName)s:%(lineno)d] :: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    state="A super simple rpc",
    details="simple RPC"
)

rpc.run()
