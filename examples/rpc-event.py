import discordrpc
from discordrpc import Event

rpc = discordrpc.RPC(app_id=12345678910)

@rpc.on(Event.JOIN_REQUEST)
def handle_join(data):
    print(data)

rpc.set_activity(
    state="In Lobby",
    party_id="party123", party_size=[2, 4],
    join_secret="game_session_abc123",
)

rpc.run()
