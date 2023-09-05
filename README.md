[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FLyQuid12%2FDiscord-RPC&label=Visitors&countColor=%2337d67a&style=flat&labelStyle=none)](https://github.com/LyQuid12/Discord-RPC)
[![Discord](https://img.shields.io/discord/887650006977347594?label=EterNomm&logo=discord)](https://discord.gg/qpT2AeYZRN)
[![Total Downloads](https://static.pepy.tech/badge/discord-rpc)](https://pepy.tech/project/discord-rpc)
[![PyPI](https://img.shields.io/pypi/v/discord-rpc?label=PyPI%20Version&logo=pypi)](https://pypi.org/project/discord-rpc)
[![PyPI - Status](https://img.shields.io/pypi/status/discord-rpc?label=Packages%20Status&logo=pypi)](https://pypi.org/project/discord-rpc)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/LyQuid12/discord-rpc?label=Commit%20Activity&logo=github)](https://github.com/LyQuid12/discord-rpc)

# Discord RPC
An Python wrapper for Discord RPC API. Allow you to make own custom RPC.

[![Changelog](https://img.shields.io/badge/Discord--RPC-Changelog-informational?style=for-the-badge&logo=github)](https://gist.github.com/LyQuid12/019b77be3cca743c4ada423ccf80b836)

## Install
- PyPI
```
pip install discord-rpc
```

## Quick example
```py
import discordrpc

rpc = discordrpc.RPC.set_id(app_id=12345678910)

rpc.set_activity(
      state="pip install discord-rpc",
      details="Discord RPC"
    )

rpc.run()
```
Note that `rpc.run()` is only required to keep your program alive. If another task is doing so then it isn't required.

More examples [here](https://github.com/LyQuid12/discord-rpc/tree/main/examples)

## Other

Join our Discord server [here](https://discord.gg/qpT2AeYZRN)

## Licence & Copyright

```
This Project under MIT License
Copyright (c) 2021-present EterNomm
```
