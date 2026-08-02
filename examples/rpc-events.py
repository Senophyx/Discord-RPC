import discordrpc
from discordrpc import Event

rpc = discordrpc.RPC(app_id=123456789)

@rpc.on(Event.JOIN)
@rpc.on(Event.JOIN_REQUEST)
@rpc.on(Event.SPECTATE)
@rpc.on(Event.INVITE)
def on_event(data):
    print(data)

rpc.set_activity(
    name="VALORANT",
    details="Valorant Ranked",
    party_id=1234,
    join_secret="anything",
    spectate_secret="idk"
)

try:
    rpc.run()
except KeyboardInterrupt:
    rpc.disconnect()
