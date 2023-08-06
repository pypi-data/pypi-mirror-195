#!/usr/bin/env python3

import webview
import platform
from backend import app


if __name__ == "__main__":
    window = webview.create_window(
        "badl - BiliBili Audio Downloader", app, width=500, height=700
    )
    if os := platform.system() == "Linux":
        gui = "gtk"
    elif os == "Windows":
        gui = "edgechromium"
    else:
        gui = ""
    webview.start(gui=gui)
