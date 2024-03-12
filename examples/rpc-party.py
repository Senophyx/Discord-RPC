import discordrpc

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    details='VALORANT',
    state='Join if you want!',

    party_id=12345, # Your party ID (Must be strings! even if it is an int it will still be changed to a string).
                    #Not really useful, I guess. But it's required if you want to create party!
    party_size=[1, 10], # Party size (must in list), [current_size, max_size]

    join_secret='playvalowithme', # Not really useful, I guess. But it's required if you want to make 'Ask to Join' button!
    spectate_secret='spectateme', # Not really useful, I guess. But it's required!
    match_secret='idkbrofr' # Not really useful, I guess. But it's required!
)

rpc.run()