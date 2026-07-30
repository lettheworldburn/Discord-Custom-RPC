import time
import sys
from pypresence import Presence, exceptions

# Config edit these values to customize your Rich Presence

CLIENT_ID = "YOUR_DISCORD_APPLICATION_CLIENT_ID"  # from discord.com/developers/applications

PRESENCE_CONFIG = {
    # Main two lines of text shown under your Discord name
    "state": "Building cool things",
    "details": "Working on a Python project",

    # Large image: set to the "key" you uploaded in the Rich Presence > Art Assets
    # tab of your Discord application, NOT a raw URL.
    "large_image": "main_logo",
    "large_text": "My Awesome App",

    # Small image (overlaid on the bottom-right corner of the large image)
    "small_image": "status_icon",
    "small_text": "Online",

    # Buttons: max 2, each needs a label (max 32 chars) and a valid URL.
    # NOTE: Discord does not allow buttons to link to another Discord invite
    # in some contexts, and buttons will NOT show on your own client's
    # preview in older Discord versions — ask a friend to check, or view
    # your profile from another account.
    "buttons": [
        {"label": "GitHub Repo", "url": "https://github.com/yourusername/yourrepo"},
        {"label": "Visit Website", "url": "https://example.com"},
    ],
}

# How often (in seconds) to refresh the connection / keep it alive.
UPDATE_INTERVAL = 15


# Scripts logic
def build_presence_kwargs(config: dict, start_time: float) -> dict:
    """Translate our config dict into pypresence.update() kwargs."""
    kwargs = {
        "state": config.get("state"),
        "details": config.get("details"),
        "large_image": config.get("large_image"),
        "large_text": config.get("large_text"),
        "small_image": config.get("small_image"),
        "small_text": config.get("small_text"),
        "start": start_time,
    }

    buttons = config.get("buttons")
    if buttons:
        # pypresence expects a list of dicts: {"label": ..., "url": ...}
        kwargs["buttons"] = buttons[:2]  # Discord allows a maximum of 2 buttons

    # Strip keys with None values (pypresence doesn't like explicit Nones
    # for some fields depending on version)
    return {k: v for k, v in kwargs.items() if v is not None}


def main():
    if CLIENT_ID == "YOUR_DISCORD_APPLICATION_CLIENT_ID":
        print(
            "[!] You haven't set your CLIENT_ID yet.\n"
            "    Edit CLIENT_ID at the top of this script — see the README\n"
            "    for how to get one from the Discord Developer Portal."
        )
        sys.exit(1)

    rpc = Presence(CLIENT_ID)

    print("[*] Connecting to Discord...")
    try:
        rpc.connect()
    except exceptions.DiscordNotFound:
        print("[!] Could not find a running Discord client. Is Discord open?")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Failed to connect: {e}")
        sys.exit(1)

    print("[+] Connected to Discord.")
    start_time = time.time()

    try:
        while True:
            kwargs = build_presence_kwargs(PRESENCE_CONFIG, start_time)
            rpc.update(**kwargs)
            print("[+] Presence updated. Press Ctrl+C to stop.")
            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        print("\n[*] Stopping and clearing presence...")
        try:
            rpc.clear()
            rpc.close()
        except Exception:
            pass
        print("[+] Done.")


if __name__ == "__main__":
    main()
