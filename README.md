[![Discord](https://img.shields.io/discord/887650006977347594?label=EterNomm&logo=discord)](https://discord.gg/qpT2AeYZRN)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/discord-rpc?label=PyPI%20Downloads&logo=pypi)](https://pypi.org/project/discord-rpc)
[![PyPI](https://img.shields.io/pypi/v/discord-rpc?label=PyPI%20Version&logo=pypi)](https://pypi.org/project/discord-rpc)
[![PyPI - Status](https://img.shields.io/pypi/status/discord-rpc?label=Packages%20Status&logo=pypi)](https://pypi.org/project/discord-rpc)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/LyQuid12/discord-rpc?label=Commit%20Activity&logo=github)](https://github.com/LyQuid12/discord-rpc)

# Discord RPC
An Python wrapper for Discord RPC API. Allow you to make own custom RPC

## Install
- PyPI
```
pip install discord-rpc
```

## Quick example
```py
import DiscordRPC
import time

app_id = 'app id'  # Application ID (cannot int)
rpc = DiscordRPC.RPC.Set_ID(app_id=app_id)

while True:
    rpc.set_activity(
      state="up to you", 
      details="up to you", 
      timestamp=rpc.timestamp(), 
      large_text="Competitive", 
      small_text="Radiant", 
      large_image="Valorant", 
      small_image="Radiant_logo"
    )
    time.sleep(600) # to update the PC, recommended: every 10 minutes or 600 seconds
```

## Other
<details>
    <summary>Plan</summary>
    <br>
    <ul>
        <li>RPC Button</li>
        <p>Added button feature to RPC</p>
    </ul>
</details>

Join our Discord server [here](https://discord.gg/qpT2AeYZRN)
