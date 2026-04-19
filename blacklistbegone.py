import platform
import sys
import click
import plistlib

from pathlib import Path
from sparserestore import backup, perform_restore
from pymobiledevice3.exceptions import NoDeviceConnectedError
from pymobiledevice3.lockdown import create_using_usbmux

def exit(code=0):
    if platform.system() == "Windows" and getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        input("Press Enter to exit...")

    sys.exit(code)

try:
    lockdown = create_using_usbmux()
except NoDeviceConnectedError:
        click.secho("No device detected! Please connect your device via USB and try again.", fg="red")
        exit(1)

def get_device_info():
    os_names = {
        "iPhone": "iOS",
        "iPad": "iPadOS",
        "iPod": "iOS",
        "RealityDevice": "visionOS",
    }
    device_class = lockdown.get_value(key="DeviceClass")
    product_version = lockdown.get_value(key="ProductVersion")
    info_text = f"{lockdown.get_value(key="DeviceName")} ({(os_names[device_class] + " " + product_version) if device_class in os_names else ""})"
    return info_text

click.secho("BlacklistBeGone v2.0 - by jailbreak.party\nMade possible by JJTech (@JJTech0130), Duy Tran (@khanhduytran0) and Mineek (@mineekdev)", fg="blue")
click.secho(f"Connected to {get_device_info()}", fg="green")

click.secho("This will clear the app revokes and certificate validity databases.", fg="yellow")
click.secho("NOTE: This tool is experimental and has a chance of damaging your device, or causing data loss.\nWe take zero responsibility in the event this happens. Use this tool at your own risk.", fg="red")

while True:
        value = input("To continue, type \"CONTINUE\" and hit Enter. Otherwise, the script will exit.\n").strip()
        if value == "CONTINUE":
            click.secho("Creating backup...", fg="yellow")

            plist_contents = plistlib.dumps({})

            cloudconfig_path = Path.joinpath(Path.cwd(), "files/CloudConfigurationDetails.plist")
            cloudconfig_contents = open(cloudconfig_path, "rb").read()

            purplebuddy_path = Path.joinpath(Path.cwd(), "files/com.apple.purplebuddy.plist")
            purplebuddy_contents = open(purplebuddy_path, "rb").read()

            back = backup.Backup(files=[
                # using Directory now for persistence (thanks Duy!!).
                # idk why the backup system lets us do this, but it's very nice cause it messes up writes to these files entirely
                # now we pray misagent/installd/trustd don't get updated...
                backup.Directory("", "DatabaseDomain"),
                backup.Directory("MobileIdentityData", "DatabaseDomain"),
                backup.Directory("MobileIdentityData/Rejections.plist", "DatabaseDomain"),
                backup.Directory("MobileIdentityData/AuthListBannedUpps.plist", "DatabaseDomain"),
                backup.Directory("MobileIdentityData/AuthListBannedCdHashes.plist", "DatabaseDomain"),
                backup.Directory("", "ProtectedDomain"),
                backup.Directory("trustd", "ProtectedDomain"),
                backup.Directory("trustd/valid.sqlite3", "ProtectedDomain"),
                backup.Directory("trustd/valid.sqlite3-shm", "ProtectedDomain"),
                backup.Directory("trustd/valid.sqlite3-wal", "ProtectedDomain"),
                # skip setup
                backup.Directory("", "SysSharedContainerDomain-systemgroup.com.apple.configurationprofiles"),
                backup.Directory("Library", "SysSharedContainerDomain-systemgroup.com.apple.configurationprofiles"),
                backup.Directory("Library/ConfigurationProfiles", "SysSharedContainerDomain-systemgroup.com.apple.configurationprofiles"),
                backup.ConcreteFile("Library/ConfigurationProfiles/CloudConfigurationDetails.plist", "SysSharedContainerDomain-systemgroup.com.apple.configurationprofiles", contents=cloudconfig_contents),
                backup.Directory("", "ManagedPreferencesDomain"),
                backup.Directory("mobile", "ManagedPreferencesDomain"),
                backup.ConcreteFile("mobile/com.apple.purplebuddy.plist", "ManagedPreferencesDomain", contents=purplebuddy_contents),
            ])

            click.secho("Restoring backup...", fg="yellow")
            perform_restore(back, reboot=True)

            click.secho("Finished! Your device should reboot shortly. If it does not, you may reboot it manually.")
        click.secho("Exiting script...", fg="red")
        exit()