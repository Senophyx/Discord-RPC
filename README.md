[![Visistors](https://visitor-badge.glitch.me/badge?page_id=LyQuid12.discord-rpc)](https://github.com/EterNomm/Chathon)
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

rpc = DiscordRPC.RPC.Set_ID(app_id="your app id") # Application ID must string 

while True:
    rpc.set_activity(
      state="Rank : Radiant",
      details="Competitive",
      timestamp=rpc.timestamp()
    )
    time.sleep(600) # to update the PC, recommended: every 10 minutes or 600 seconds
```

More examples [here](https://github.com/LyQuid12/discord-rpc/tree/main/examples)

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
