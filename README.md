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


## Contributors
Big thanks for contributors who help this project keep updated, and maintained.


<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://pukima.site"><img src="https://avatars.githubusercontent.com/u/58347116?v=4?s=100" width="100px;" alt="Pukima"/><br /><sub><b>Pukima</b></sub></a><br /><a href="#bug-Pukimaa" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/k9ur"><img src="https://avatars.githubusercontent.com/u/67886793?v=4?s=100" width="100px;" alt="k9er"/><br /><sub><b>k9er</b></sub></a><br /><a href="#doc-k9ur" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.kaleko.dev/"><img src="https://avatars.githubusercontent.com/u/54416665?v=4?s=100" width="100px;" alt="Kale"/><br /><sub><b>Kale</b></sub></a><br /><a href="#bug-Kale-Ko" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/TaIFeel"><img src="https://avatars.githubusercontent.com/u/94287800?v=4?s=100" width="100px;" alt="TaIFeel"/><br /><sub><b>TaIFeel</b></sub></a><br /><a href="#code-TaIFeel" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://buymeacoffee.com/saves"><img src="https://avatars.githubusercontent.com/u/8108358?v=4?s=100" width="100px;" alt="Jesusaves"/><br /><sub><b>Jesusaves</b></sub></a><br /><a href="#bug-pazkero" title="Bug reports">🐛</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## Links
- [Github Repository](https://github.com/Senophyx/Discord-RPC)
- [PyPI Project page](https://pypi.org/project/discord-rpc/)
- [TestPyPI Project page](https://test.pypi.org/project/discord-rpc/)
- [Discord Server](https://discord.gg/qpT2AeYZRN)

## Licence & Copyright

```
This Project under MIT License
Copyright (c) 2021-2024 Senophyx
```
