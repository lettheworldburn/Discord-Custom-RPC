# Discord Rich Presence Script (pypresence)

A simple Python script that sets a custom Discord Rich Presence — the
"Playing a game" style status shown on your profile — complete with
text, images, an elapsed timer, and up to two clickable buttons.

## Requirements

- Python 3.7+
- The **Discord desktop app** running and logged in (Rich Presence does
  not work with the browser version of Discord)
- The `pypresence` library

## 1. Install dependencies

```bash
pip install pypresence
```

## 2. Create a Discord Application (to get a Client ID)

Rich Presence works by pretending your script is a "game" registered
as a Discord Application.

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**, give it any name (this name may show up
   depending on your Discord settings)
3. Copy the **Application ID** shown on the General Information page —
   this is your `CLIENT_ID`
4. (Optional, for images) Go to the **Rich Presence → Art Assets** tab
   and upload images. Each image gets a **key name** (e.g. `main_logo`)
   — you'll use that key name in the script, not the file itself.

## 3. Configure the script

Open `discord_rpc.py` and edit the top section:

```python
CLIENT_ID = "YOUR_DISCORD_APPLICATION_CLIENT_ID"

PRESENCE_CONFIG = {
    "state": "Building cool things",
    "details": "Working on a Python project",
    "large_image": "main_logo",
    "large_text": "My Awesome App",
    "small_image": "status_icon",
    "small_text": "Online",
    "buttons": [
        {"label": "GitHub Repo", "url": "https://github.com/yourusername/yourrepo"},
        {"label": "Visit Website", "url": "https://example.com"},
    ],
}
```

| Field         | Description                                                        |
|---------------|----------------------------------------------------------------------|
| `state`       | Second line of the status text                                     |
| `details`     | First line of the status text                                      |
| `large_image` | Key name of an uploaded Art Asset (large image)                    |
| `large_text`  | Tooltip text shown when hovering the large image                   |
| `small_image` | Key name of an uploaded Art Asset (small badge on large image)     |
| `small_text`  | Tooltip text shown when hovering the small image                   |
| `buttons`     | List of up to **2** dicts: `{"label": ..., "url": ...}`             |

## 4. Run it

Make sure Discord is open, then run:

```bash
python discord_rpc.py
```

You should see:

```
[*] Connecting to Discord...
[+] Connected to Discord.
[+] Presence updated. Press Ctrl+C to stop.
```

Your Discord profile will now show the custom status. Press `Ctrl+C`
to stop the script and clear the presence.

## Notes & Limitations

- **You can't see your own buttons** in some Discord client versions —
  ask a friend to check your profile, or view it from a second account.
- Buttons need valid `http://` or `https://` URLs; Discord will reject
  buttons pointing to invalid links.
- Rich Presence images **must** be uploaded as Art Assets in the
  Developer Portal first — you reference them by their key name, not
  a direct image URL.
- If Discord is closed or you're using the browser client, `rpc.connect()`
  will fail with `DiscordNotFound`.
- The presence automatically clears when the script exits (`Ctrl+C`) or
  when the connection drops.

## Customizing further

- Change `UPDATE_INTERVAL` in the script to control how often the
  presence refreshes (useful if you want to reflect changing state,
  e.g. current song, current file being edited, etc.)
- You can call `rpc.update(...)` with different values dynamically —
  for example, wire this into another script that tracks what you're
  currently working on.
