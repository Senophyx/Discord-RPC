# Discord RPC Documentation

This package was created to make it easier for Discord users to create a custom rich presence on their profile. Yes, that's it.

<img src='https://raw.githubusercontent.com/Senophyx/Discord-RPC/main/media/preview.png' style='width: 30%;' alt='Dicord-RPC preview'>

## Getting application ID
1. Go to https://discord.com/developers/applications
2. Click "New Application" if you don't have application
3. Insert the name of your application
4. Copy `APPLICATION ID`


## Installing Discord-RPC
- **Installing stable version**

  The safetest way to install stable version is using PIP command line. Run this command in cmd/terminal :<br>
  ```
  pip install discord-rpc
  ```

- **Installing unstable/development version**

  There are 2 methods for installing the development version, namely from TestPyPI or directly from GitHub.
  1. **From TestPyPI**<br>
    ```
    pip install -i https://test.pypi.org/simple/ discord-rpc
    ```
  
  2. **Directly from Github**<br>
    ```
    pip install git+https://github.com/Senophyx/Discord-RPC.git
    ```


## Quickstart
Step-by-step making simple rich presence using Discord-RPC.
1. Make sure Discord-RPC is installed.
2. Import Discord-RPC
    ```py
    import discordrpc
    ```

3. Creating `rpc` variable from `discordrpc.RPC` with your unique ([Application ID](#getting-application-id)).
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


## Examples
Examples can be seen in the repository (`Discord-RPC/examples`) or [here](https://github.com/Senophyx/Discord-RPC/tree/main/examples).


## **All classes and functions**

## class `discordrpc.RPC()`
- `discordrpc.RPC()`<br><br>
    Parameters :
    - app_id (`int`) : Application ID ([Tutorial](#getting-application-id))
    - debug (`bool`) : Whether to include debug information in the output. Default = False
    - output (`bool`) : Whether to print the output. Default = True
    - exit_on_disconnect (`bool`) : Whether to quit program when disconnecting. Default = True

- method `RPC.set_activity()`<br>
    Set activity to be displayed on the user's Discord profile.<br>
    See [Activity Object](https://discord.com/developers/docs/events/gateway-events#activity-object) Discord documentation page for more details.
    Keep in mind that not every field is currently implemented.

    Parameters :
    - state (`str`) - Describes user's current party status.
    - details (`str`) - Describes what the player is currently doing.
    - act_type (`discordrpc.Activity`) : An [Activity Type](https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-types). Controls how the user's activity is described in their status (e.g. Playing Foo, Listening to Foo). (`Streaming` and `Custom` are currently disabled, see [#28](https://github.com/Senophyx/Discord-RPC/issues/28#issuecomment-2301287350))
    - status_type (`discordrpc.StatusDisplay`) : A [Status Display Type](https://discord.com/developers/docs/events/gateway-events#activity-object-status-display-types). Controls what is displayed in the user's activity status (e.g. Listening to Foo, Listening to Bar)
    - ts_start (`int`) : Timestamp representing the start time of an activity. Represented in UNIX epoch time, in seconds.
    - ts_end (`int`) : Timestamp representing the end time of an activity. Represented in UNIX epoch time, in seconds. When specified, a progress bar is displayed going from `ts_start` to `ts_end`.
    - large_image (`str`) : Either a unique name of an asset in your application, or a URL to an image. See [Activity Asset Image](https://discord.com/developers/docs/events/gateway-events#activity-object-activity-asset-image).
    - large_text (`str`) : Text shown when hovering over `large_image`.
    - large_url (`str`) : URL opened when clicking on `large_image`.
    - small_image (`str`) : Either a unique name of an asset in your application, or a URL to an image. See [Activity Asset Image](https://discord.com/developers/docs/events/gateway-events#activity-object-activity-asset-image).
    - small_text (`str`) : Text shown when hovering over  `small_image`.
    - small_url (`str`) : URL opened when clicking on `small_url`.
    - party_id (`int`) : ID of the user’s party.
    - party_size (`list`) : Party size in list with format `[current_size, max_size]` or `[1, 10]`.
    - join_secret (`str`) : Secret for chat invitations and ask to join button.
    - spectate_secret (`str`) : Secret for spectate button.
    - match_secret (`str`) : Secret for for spectate and join button.
    - buttons (`list`) :  A `list` of `dicts` for buttons on user's profile. A helper object `discordrpc.Button(text:str, url:str)` is provided.

  Returns : `True` if RPC successfully connected.

- method `RPC.disconnect()`<br>
  Disconnecting and closing RPC socket.

  Returns : `None`.

- method `RPC.run()`<br>
  Keeping the RPC alive. Not required if another tasks is running on the same file.

  Parameters :
  - update_every (`int`) : `time.sleep` every inputed second.

  Exceptions :
  - `KeyboardInterrupt` will call `RPC.disconnect`.

  Returns : `None`.

- variable `self.is_connected`<br>
  Check whether the RPC successfully handshaked and connected to the Discord socket.

  Return : `True` or `False`

- variable `self.is_running`<br>
  Checks whether the RPC successfully updated `RPC.set_activity` or not.

  Return : `True` or `False`


## class `discordrpc.Activity`
- Enum `Activity`<br>
  Simplified Activity type payload in `RPC.set_activity`

  Available values :
  - Playing
  - Streaming
  - Listening
  - Watching
  - Custom
  - Competing

> [!NOTE]
> Types `Streaming` and `Custom` are currently disabled.<br>
> [Details](https://github.com/Senophyx/Discord-RPC/issues/28#issuecomment-2301287350)

## class `discordrpc.Activity`
- Enum `StatusDisplay`<br>
  Simplified StatusDisplay type payload in `RPC.set_activity`

  Available values :
  - Name 
  - State
  - Details

## class `discordrpc.Button()`
- function `Button()`<br>
  Simplified button payload in `RPC.set_activity`

  Parameters :
  - text (`test`)
  - text (`url`)

  Returns : Payload dict.

> [!NOTE]
> Discord does not display buttons in your own Activity.<br>
> You won’t see them yourself — but other users will see them correctly.

## class `discordrpc.utils`
- variable `discordrpc.utils.timestamp()`<br>
  Return current time in epoch timestamp (`int`).

- function `discordrpc.utils.date_to_timestamp()`<br>
  Date to timestamp converter.

  Parameters :
  - date (`str`) : a date and time in string with format `%d/%m/%Y-%H:%M:%S` or `day/month/year-hour:minute:second`. Example : <br><br>
      ```py
      date_to_timestamp('14/06/2025-00:00:00')
      ```


## Exceptions & Errors
- `RPCException`<br>
    Raising errors that don't know what the specific error is and how to fix it.

- `Error`<br>
    Raising unspecific errors. The error and how to fix it are in the message.

- `DiscordNotOpened`<br>
    Discord client not running or not found.
    
    How-to-Fix : just open discord :)

- `ActivityError`<br>
    Error in the `set_activity` method. Usually due to entering the payload incorrectly.

    How-to-Fix : Make sure `set_activity` are set correctly.

- `InvalidURL`<br>
    The URL in the `Button` function is incorrect because it does not start with `http://` or `https://`.

    How-to-Fix : Make sure the URL starts with `http://` or `https://`

- `InvalidID`<br>
    Application ID is incorrect or not found.

    How-to-Fix : make sure you input the ID correctly from https://discord.com/developers/applications. ([Tutorial how to get application id](#getting-application-id))


- `ButtonError`<br>
    There is an error in the `Button` function, usually because the required parameters are not set/input.

    How-to-Fix : Check if `Button` function are set correctly



## Links
- [Github Repository](https://github.com/Senophyx/Discord-RPC)
- [PyPI Project page](https://pypi.org/project/discord-rpc/)
- [TestPyPI Project page](https://test.pypi.org/project/discord-rpc/)
- [Discord Server](https://discord.gg/qpT2AeYZRN)

## Licence & Copyright
```
Discord-RPC project is under MIT License
Copyright (c) 2021-2025 Senophyx.
```
