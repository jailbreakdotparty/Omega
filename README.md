# Omega
***(formerly BlacklistBeGone)***

Clears app revoke and certificate validity databases on iOS, for sideloaders.
<p align="left">
  <strong><a href="https://jailbreak.party/discord">Join our Discord!</a></strong>
</p>

>[!WARNING]
>Make a backup before using this tool **JUST IN CASE.** We are not responsible for any damages that this may cause to your device, so use at your own risk.

## Usage
**Requrements**
- A computer with Python 3.9+, [pymobiledevice3](https://github.com/doronz88/pymobiledevice3), and `click` installed.
- On Windows, [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k) or [iTunes](https://support.apple.com/en-us/106372) installed.
- On Linux, [usbmuxd](https://github.com/libimobiledevice/usbmuxd) and [libimobiledevice](https://github.com/libimobiledevice/libimobiledevice).
- An iOS device running iOS 16 or higher.

**Steps**
1. Disable Find My on your device. This is required to restore the partial backup, you can re-enable it after you're done.
2. Connect your device to your computer via USB.
3. Run `omega.py` with your Python install.
4. Profit

## Info
iOS stores certain databases containing information on which sideloaded apps are revoked and the validity of signing certificates at `/var/db/MobileIdentityData/` and `/var/protected/trustd/`.

Using partial backups, we can restore these files and clear them, or replace them with directories.

This tool replaces the databases with directories of the same name, which causes the system to fail when attempting to write to them, therefore preventing your device from "remembering" any revokes or blacklisted certificates.

## Credits
- [Mineek](https://github.com/mineek) - documented & discovered [this whole concept](https://gist.github.com/mineek/f17df8b95e6fb168a9b9929e2993e900/)
- [Duy Tran](https://github.com/khanhduytran0) - shared persistence (directory overwrite) strategy
- [JJTech](https://github.com/JJTech0130/) - developed [sparserestore](https://github.com/JJTech0130/TrollRestore/tree/main/sparserestore) (backup creation) library
- [LeminLimez](https://github.com/leminlimez) - reference and skipsetup config
- [Skadz](https://github.com/skadz108) - developer