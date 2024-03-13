[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FSenophyx%2FDiscord-RPC&label=Visitors&countColor=%2337d67a&style=flat&labelStyle=none)](https://github.com/Senophyx/Discord-RPC)
[![Discord](https://img.shields.io/discord/887650006977347594?label=EterNomm&logo=discord)](https://discord.gg/qpT2AeYZRN)
[![Total Downloads](https://static.pepy.tech/badge/discord-rpc)](https://pepy.tech/project/discord-rpc)
[![PyPI](https://img.shields.io/pypi/v/discord-rpc?label=PyPI%20Version&logo=pypi)](https://pypi.org/project/discord-rpc)
[![PyPI - Status](https://img.shields.io/pypi/status/discord-rpc?label=Packages%20Status&logo=pypi)](https://pypi.org/project/discord-rpc)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Senophyx/discord-rpc?label=Commit%20Activity&logo=github)](https://github.com/Senophyx/discord-rpc)

# Discord RPC
An Python wrapper for Discord RPC API. Allow you to make own custom RPC.

[![Changelog](https://img.shields.io/badge/Discord--RPC-Changelog-informational?style=for-the-badge&logo=github)](https://gist.github.com/Senophyx/019b77be3cca743c4ada423ccf80b836)

## Install
- PyPI
```
pip install discord-rpc
```

## Quick example
```py
import discordrpc

rpc = discordrpc.RPC(app_id=12345678910)

rpc.set_activity(
      state="A super simple rpc",
      details="simple RPC"
    )

# Required if you only run Discord RPC on this file or current instance.
rpc.run()
```
`rpc.run()` is only used if you are only running Discord RPC on the current file/instance. If there are other programs/tasks on the current instance, `rpc.run()` does not need to be used.

See documentation [here](https://github.com/Senophyx/Discord-RPC/blob/main/DOCS.md).<br>
More examples [here](https://github.com/Senophyx/discord-rpc/tree/main/examples).

## Other

Join our Discord server [here](https://discord.gg/qpT2AeYZRN)

## Licence & Copyright

```
This Project under MIT License
Copyright (c) 2021-2024 Senophyx
```
