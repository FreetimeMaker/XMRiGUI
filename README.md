# XMRiGUI

XMRiGUI is a free and open-source crypto miner for Windows and Linux. It provides a modern, high-performance GUI for [XMRig](https://github.com/xmrig/xmrig) and other popular miners.

Built with **C++ 17**, **Qt6**, and the latest **CMake 4.3** standard.

![Preview of XMRiGUI](preview.png)

## Features

### Supported Miners
*   **XMRig**: For Monero, Ravencoin, and most CPU-based coins.
*   **CPUMiner-Multi**: Automatically used for Bitcoin and Litecoin.
*   **lolMiner**: Automatically used for Ethereum Classic.

### Key Capabilities
*   **Multi-Profile Support**: Manage up to 3 different mining configurations simultaneously.
*   **Intelligent Auto-Switching**: Automatically selects the best miner binary based on the selected coin.
*   **Real-time Stats**: Live tracking of Hashrate (H/s) and Shares (Accepted/Rejected).
*   **System Tray Integration**: Run the miner in the background with quick-access controls.
*   **Cross-Platform**: Native look and feel on both Windows and Linux.
*   **Auto-Updates**: Checks for new versions of XMRiGUI and XMRig binaries automatically.

### Supported Coins & Algorithms
*   **Monero** (RandomX)
*   **Bitcoin** (SHA-256)
*   **Litecoin** (Scrypt)
*   **Ethereum Classic** (Etchash)
*   **Ravencoin** (KawPow)
*   ...and 20+ other algorithms (Ghostrider, Argon2, AstroBWT, etc.)

## Installation

### Windows
1. Download the latest `XMRiGUI-Windows.zip` from the [Releases](https://github.com/FreetimeMaker/XMRiGUI/releases) page.
2. Extract the files and run `XMRiGUI.exe`.

### Linux
1. Download the `XMRiGUI-Linux.tar.gz`.
2. Ensure you have Qt6 libraries installed:
   ```bash
   sudo apt install qt6-base-dev
   ```
3. Run the binary: `./XMRiGUI`

## Security & Code Signing

### Why is my antivirus flagging this?
Since XMRiGUI is a crypto mining tool, it is often flagged by antivirus programs and Windows Defender as a "Potentially Unwanted Application" (PUA) or even malware. This is standard behavior for mining software.

### Missing Digital Signature
Official releases are currently **not** signed with a commercial Code Signing certificate (EV certificate). Such certificates from trusted authorities (like DigiCert or Sectigo) involve high annual costs, which is not feasible for this open-source project at this time.

**What this means for you:**
*   You might see a **Windows SmartScreen** warning ("Windows protected your PC") when launching the app.
*   You may need to add an exclusion to your antivirus software for the installation directory or `XMRiGUI.exe`.

**Recommendation:**
If you do not trust the provided binaries, you can build XMRiGUI from source at any time. The code is fully transparent and available for inspection on GitHub.

## Build from Source

### Requirements
*   **CMake 4.3+**
*   **Qt 6.6+** (with Widgets and Network modules)
*   C++ 17 compatible compiler (MSVC on Windows, GCC/Clang on Linux)

### Compilation
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

### Create Linux Packages (.deb, .rpm)
To generate installation packages for Debian/Ubuntu or Fedora/openSUSE:
```bash
cd build
cpack
```
This will create `xmrigui-1.8.0-Linux.deb` and `xmrigui-1.8.0-Linux.rpm` in your build directory.

## Command Line Options
*   `start`: Start mining all active profiles immediately.
*   `stop`: Stop all active mining processes.
*   `--open`: Open the main window.
*   `--close`: Hide to system tray.

## Contribute

### Support the Project
If you find this tool useful, consider supporting development:
*   **Monero (XMR)**: `49szz88CqMWGgyDxp7VqvBS62pGLQcV4YPSBHcLwtxAXLz1Wngf8vW6is4w13Au7C2RovrTiJQaGDV5VBhFnyMBsM44Pn2P`

### Development
Pull requests and bug reports are welcome on [GitHub](https://github.com/FreetimeMaker/XMRiGUI).

---
**Disclaimer**: Mining can be intensive for your hardware. Ensure proper cooling. Use at your own risk.
