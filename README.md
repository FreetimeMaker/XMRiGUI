# XMRiGUI

XMRiGUI is a free and open-source crypto miner for Windows and Linux. It provides a modern, high-performance GUI for [XMRig](https://github.com/xmrig/xmrig).

Built with **Python 3** and **GTK 3**.

![Preview of XMRiGUI](preview.png)

## Features

### Supported Miners
*   **XMRig**: For Monero, Ravencoin, and most CPU-based coins.

### Key Capabilities
*   **Multi-Profile Support**: Manage up to 3 different mining configurations simultaneously.
*   **Intelligent Auto-Switching**: Automatically selects the best miner binary based on the selected coin.
*   **Real-time Stats**: Live tracking of Hashrate (H/s) and Shares (Accepted/Rejected).
*   **System Tray Integration**: Run the miner in the background with quick-access controls.
*   **Cross-Platform**: Native look and feel on both Windows and Linux.

## Installation

### Windows
1. Download the latest `XMRiGUI_Setup.exe` from the [Releases](https://github.com/FreetimeMaker/XMRiGUI/releases) page.
2. Run the installer.
3. *Note: If you run from source, you need to install GTK3 (e.g., via MSYS2 or the gvsbuild installer).*

> [!WARNING]
> **Security & Code Signing**
>
> XMRiGUI is currently **not** signed with a commercial Code Signing certificate.
> *   Windows SmartScreen may display a warning ("Windows protected your PC").
> *   This is standard for many open-source projects due to high certificate costs.
> *   To proceed, click **"More Info"** and then **"Run Anyway"**.
> *   Antivirus software may flag this tool as a "Miner" or "PUA" (Potentially Unwanted Application). This is expected behavior for mining software.

### Linux

#### Debian / Ubuntu (APT)
1. Download the `.deb` file or use the APT Repository:

```bash
sudo nano /etc/apt/sources.list.d/Freetime-Repo.list
```

then add:
```text
deb [trusted=yes arch=amd64] https://apt.fury.io/freetimemaker/ /
```

then run:
```bash
sudo apt update
sudo apt install xmrigui
```

#### Fedora / Red Hat (RPM)
1. Download the `.rpm` file or use the YUM Repository:

```bash
sudo nano /etc/yum.repos.d/freetime.repo
```

then add:
```text
[freetimemaker]
name=Freetime Repo
baseurl=https://yum.fury.io/freetimemaker/
enabled=1
gpgcheck=0
```

then run:
```bash
sudo dnf install xmrigui
```

## Build for Windows (Standalone EXE & Installer)

### 1. Create the Executable
To create a single `.exe` file that contains everything:
1. Install Python 3.
2. Install build tools:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```
3. Run: `python build_windows.py`
   The result will be in `dist/XMRiGUI.exe`.

### 2. Create the Installer (Optional)
1. Install [Inno Setup](https://jrsoftware.org/isinfo.php).
2. Open the [installer.iss](installer.iss) file.
3. Click **Compile** to generate `Output/XMRiGUI_Setup.exe`.

## Linux Makefile Commands

If you want to build XMRiGUI from source, you'll need to have:
* python3
* gtk3
* pyinstaller
* pygobject
* gir1.2-ayatanaappindicator3-0.1
  <br>
  <br>

Build:

`sudo make install`

or if you want deb package:

`make deb`
<br>
<br>

## Command Line Options
*   `start`: Start mining all active profiles immediately.
*   `stop`: Stop all active mining processes.

## Contribute

### Support the Project
If you find this tool useful, consider supporting development:
*   **Monero (XMR)**: `49szz88CqMWGgyDxp7VqvBS62pGLQcV4YPSBHcLwtxAXLz1Wngf8vW6is4w13Au7C2RovrTiJQaGDV5VBhFnyMBsM44Pn2P`

### Development
Pull requests and bug reports are welcome on [GitHub](https://github.com/FreetimeMaker/XMRiGUI).

---
**Disclaimer**: Mining can be intensive for your hardware. Ensure proper cooling. Use at your own risk.
