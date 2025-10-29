# Discord‑RPC —  Documentation

A lightweight Python client for Discord’s Rich Presence via the local IPC pipe. This library helps you set and update the activity shown on a user’s Discord profile with minimal code.

---

## Table of Contents

- [Installation](#installation)
- [Getting Application ID](#getting-application-id)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
  - [RPC](#rpc)
    - [`__init__`](#rpc__init__)
    - [`set_activity`](#rpcset_activity)
    - [`run`](#rpcrun)
    - [`clear`](#rpcclear)
    - [`disconnect`](#rpcdisconnect)
  - [Buttons](#buttons)
  - [Utils](#utils)
    - [`timestamp`](#utilstimestamp)
    - [`date_to_timestamp`](#utilsdate_to_timestamp)
    - [`use_local_time`](#utilsuse_local_time)
    - [`ProgressBar`](#utilsprogressbar)
  - [Types](#types)
    - [`Activity`](#discordactivity---enum)
    - [`StatusDisplay`](#discordstatusdisplay---enum)
    - [`User`](#rpcuser)
  - [Exceptions](#exceptions)
- [Examples](#examples)
  - [Basic presence](#basic-presence)
  - [Presence with buttons](#presence-with-buttons)
  - [Timed/Progress presence](#timedprogress-presence)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Links](#links)
- [License](#licence--copyright)

---

## Installation

```bash
pip install discord-rpc
```

> Discord desktop app must be running on the same machine.

---

## Getting Application ID

1. Go to https://discord.com/developers/applications
2. Click "New Application" if you don't have application
3. Insert the name of your application
4. Copy `APPLICATION ID`

---

## Quick Start

Step-by-step making simple rich presence using Discord-RPC.
1. Make sure Discord-RPC is installed.
2. Import Discord-RPC
    ```py
    import discordrpc
    ```

3. Make `rpc` variable from `discordrpc.RPC` with your unique ([Application ID](#getting-application-id)).
    ```py
    rpc = discordrpc.RPC(app_id=1234) #Change app_id to your app id
    ```

4. Customizing activity using `rpc.set_activity()`.
    ```py
    rpc.set_activity(
      state="A super simple rpc",
      details="simple RPC"
    )
    ```

5. Creating loop for `rpc` so that it can keep running. (Only required if you only run Discord RPC on this file or current instance)
    ```py
    rpc.run()
    ```

6. Done! Run your file.

---

## API Reference

### `RPC`

```python
class RPC:
    def __init__(...): -> None
```

#### `RPC.__init__`

Creates an IPC client and attempts to connect to the local Discord instance.

Parameters :
- **app_id**: Your Discord *Application (Client) ID* (int or str).  
- **debug**: If `True`, enables verbose logging (DEBUG).  
- **output**: If `False`, silences logger output.  
- **exit_if_discord_close**: If `True`, raises when Discord is not found/closed.  
- **exit_on_disconnect**: If `True`, exits the process when the socket disconnects.



#### `RPC.set_activity`

```python
def set_activity(...): -> bool
```

Sets or updates the current Rich Presence. Returns `True` on success.

Parameters (all optional unless stated):

- **details** *(str)* — Upper line of the activity.
- **state** *(str)* — Lower line of the activity.
- **act_type** *(Activity, default: `Activity.Playing`)* — See [Types](#types).
- **status_type** *(StatusDisplay, default: `StatusDisplay.Name`)* — Which field (name/state/details) is considered the “status name” for some clients.
- **large_image** *(str)* — Key of an uploaded **Rich Presence Asset** (application’s Art Assets).
- **large_text** *(str)* — Tooltip text when hovering the large image.
- **large_url** *(str)* — Optional URL for the large image (supported by this lib/client side feature).
- **small_image** *(str)* — Key of a small asset.
- **small_text** *(str)* — Tooltip for the small image.
- **small_url** *(str)* — Optional URL for the small image.
- **state_url**, **details_url** *(str)* — Optional link targets when clicking the text (if supported).
- **ts_start**, **ts_end** *(int)* — Unix timestamps (seconds). Use helpers in [Utils](#utils).
- **party_id** *(str)* — ID to identify a party/session.
- **party_size** *(list[int, int])* — Current and max size, e.g. `[2, 5]`.
- **join_secret**, **spectate_secret**, **match_secret** *(str)* — Secrets for join/spectate/match (if your flow uses them).
- **buttons** *(list[dict])* — Up to 2 buttons created by [`button.Button`](#buttons).
- **clear** *(bool)* — If `True`, clears the activity. Same thing as `rpc.clear()`

Variables :
- **is_connected** -> bool — Check whether the RPC successfully handshaked and connected to the Discord socket.
- **is_running** -> bool — Checks whether the RPC successfully running and updated `RPC.set_activity` or not.
- **self.User** — Returns information about the user to whom the connection occurred. [Available attributes](#rpcuser).

**Notes & validation:**  
- `act_type` **must** be a value of `types.Activity`; otherwise `InvalidActivityType` is raised.  
- As of Discord policy, `Activity.Streaming` and `Activity.Custom` are disabled for Rich Presence updates and will raise `ActivityTypeDisabled`.  
- If Discord is not running, `DiscordNotOpened` may be raised (depending on `exit_if_discord_close`).



### `RPC.run()`

```python
def run(update_every:int=1): -> None
```

Keeping the RPC alive. Not required if another tasks is running on the same file.

Parameter :
  - **update_every** *(int, default: `1`)* : `time.sleep` every inputed second.

Exceptions :
  - `KeyboardInterrupt` will call `RPC.disconnect`.



### `RPC.clear()`

```python
def clear(): -> None
```

Clear activity status.



#### `RPC.disconnect()`

```python
def disconnect(): -> None
```

Closes the IPC socket and marks the client as disconnected. If `exit_on_disconnect=True`, the process exits after issuing the close command.

---

## Buttons

```python
def Button(text: str, url: str): -> dict
```
Creates a Discord-compatible button payload. Discord allows up to **2 buttons** per activity.

Variables :
- **text** — Button label (1–32 chars recommended).  
- **url** — Must start with `http://` or `https://`. If invalid, raises `InvalidURL`.

[Example](#presence-with-buttons)

---

## Utils

```python
from discordrpc import utils
```

### `utils.timestamp`

```python
timestamp -> int
```
A variable to return current time in epoch timestamp.



### `utils.date_to_timestamp`

```python
def date_to_timestamp(date:str): -> int
```
Date to timestamp converter.

Parameters :
- date (`str`) : a date and time in string with format `%d/%m/%Y-%H:%M:%S` or `day/month/year-hour:minute:second`. Example :

    ```python
    date_to_timestamp('14/06/2025-00:00:00')
    ```



### `utils.use_local_time`

```python
def use_local_time(): -> dict
```
Simplified `ts_start` payload in `RPC.set_activity`.



### `utils.ProgressBar`

```python
def ProgressBar(current:int, duration:int) -> dict
```

Simplified `ts_start` and `ts_end` payload in `RPC.set_activity`.

  Parameters :
  - current (`int`)
  - duration (`int`)

  Return : Payload dict of `ts_start` and `ts_end`.



---

## Types

### `discord.Activity -> enum`

```python
from discordrpc import Activity
```

Types `Streaming` and `Custom` are currently disabled from Discord itself.

Attributes :
- Playing
- Streaming
- Listening
- Watching
- Custom
- Competing



### `discord.StatusDisplay -> enum`

```python
from discordrpc import StatusDisplay
```

Attributes :
- Name
- State
- Details



### `rpc.User()`

```python
rpc = discordrpc.RPC()
rpc.User()
```

A lightweight `User` model populated after handshake, with attributes commonly provided by Discord (e.g., `id`, `name`, `global_name`, `avatar`, `bot`, `premium_type`). The `avatar` helper builds the correct CDN URL based on hash/animation.

Use it as variable from [`RPC.__init__`](#rpc__init__).

Attributes :
  - id (`int`)
  - username (`str`)
  - name (`str`)
  - avatar (URL `str`)
  - bot (`bool`)
  - premium_type (`int`) ([details](https://discord.com/developers/docs/resources/user#user-object-premium-types))

[Example](https://github.com/Senophyx/Discord-RPC/blob/main/examples/get-user.py)

---

### Exceptions

Module: `exceptions.py` (all extend `RPCException`)

- `Error(message)` — Base user error.
- `DiscordNotOpened()` — Discord not found/running.
- `ActivityError()` — Malformed/invalid activity payload.
- `InvalidURL()` — URL did not start with `http://` or `https://`.
- `PipeException(message)` — IPC pipe error.
- `ConnectionClosed()` — The pipe/socket was closed.
- `HandshakeFailed()` — IRC/IPC handshake did not complete successfully.
- `SystemNotSupported()` — Unsupported OS/platform for this action.
- `InvalidActivityType(message)` — `act_type` is not a `types.Activity` member.
- `ActivityTypeDisabled()` — `Streaming`/`Custom` types are blocked by Discord for Rich Presence.
- `ProgressbarError(message)` — Invalid progress values (e.g., current > duration).

> Catch `RPCException` if you want to handle all library errors.

---

## Examples

### Basic presence
```python
import discordrpc

rpc = discordrpc.RPC(app_id=12345678910)

rpc.set_activity(
      state="A super simple rpc",
      details="simple RPC"
    )

rpc.run()
```

### Presence with buttons
```python
import discordrpc
from discordrpc import Button

buttons = [
    Button("Repository", "https://github.com/Senophyx/discord-rpc"),
    Button("Discord", "https://discord.gg/qpT2AeYZRN"),
]

rpc = discordrpc.RPC(app_id=1234567891011)

rpc.set_activity(
      state="Made by Senophyx",
      details="Discord-RPC",
      buttons=buttons
    )


rpc.run()
```

More examples can be found [here](https://github.com/Senophyx/Discord-RPC/tree/main/examples).

---

## Troubleshooting

- **“Discord is closed” / could not find IPC:** Ensure the desktop app is open. On Linux, confirm `$XDG_RUNTIME_DIR` or `/tmp` contains `discord-ipc-*` sockets.
- **`ActivityTypeDisabled`:** Discord no longer accepts `Streaming` and `Custom` via Rich Presence updates. Use another `Activity` value.
- **Buttons don’t show:** You can only have up to **2** buttons. All URLs must begin with `http://` or `https://`.
- **No images appear:** Upload assets to the **Art Assets** section of your application and reference their **keys**, not file paths.
- **App exits on disconnect:** Set `exit_on_disconnect=False` when creating `RPC` if you prefer to handle disconnects yourself.
- **Silence logs:** Pass `output=False` to `RPC(...)` to disable log output.

---

## FAQ

**Q: Do I need a bot token?**  
A: No. This library communicates locally with the Discord client via IPC; only an Application ID is needed.

**Q: Can I update the presence from a server?**  
A: No. This is a client-side integration; the user’s Discord app must run on the same machine.

**Q: Can I use streaming or custom activity?**  
A: Those types are disabled for RPC updates and raise `ActivityTypeDisabled`.

---

## Links
- [Github Repository](https://github.com/Senophyx/Discord-RPC)
- [PyPI Project page](https://pypi.org/project/discord-rpc/)
- [TestPyPI Project page](https://test.pypi.org/project/discord-rpc/)
- [Discord Server](https://discord.gg/qpT2AeYZRN)

## Licence & Copyright
```
Discord-RPC project is under MIT License.
Copyright (c) 2021-2025 Senophyx.
```