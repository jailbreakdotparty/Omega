from tempfile import TemporaryDirectory
from pathlib import Path

from pymobiledevice3.lockdown import create_using_usbmux, UsbmuxLockdownClient
from pymobiledevice3.services.mobilebackup2 import Mobilebackup2Service
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3.exceptions import PyMobileDevice3Exception

from . import backup

async def perform_restore(backup: backup.Backup, client: UsbmuxLockdownClient, reboot: bool = False):
    try:
        with TemporaryDirectory() as backup_dir:
            backup.write_to_directory(Path(backup_dir))
                
            async with Mobilebackup2Service(client) as mb:
                await mb.restore(backup_dir, system=True, reboot=reboot, copy=False, source=".")
            if reboot:
                async with DiagnosticsService(client) as diagnostics_service:
                    await diagnostics_service.restart()
    except PyMobileDevice3Exception as e:
        if "Find My" in str(e):
            print("Find My must be disabled in order to use this tool.")
            print("Disable Find My from Settings (Settings -> [Your Name] -> Find My) and then try again.")
            raise e
        elif "crash_on_purpose" not in str(e):
            raise e
