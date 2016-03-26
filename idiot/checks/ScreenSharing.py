"""
Idiot check for ScreenSharing

purpose: indicates if Sharing Preferences: Screen Sharing / VNC is permitted to 
    this machine

daemons:
    /System/Library/CoreServices/RemoteManagement/screensharingd.bundle/Contents/MacOS/screensharingd
    /System/Library/CoreServices/RemoteManagement/ScreensharingAgent.bundle/Contents/MacOS/ScreensharingAgent

requirement: ScreenSharing permits remote console/interactive access.

info:
Detecting this is tricky because until it's accessed neither of the above are 
forked as processes visible in process table. Once a system has been accessed, 
though, these processes remain until Sharing:Screen Sharing is disabled

 Might need to read defaults or a plist instead.
 $ sudo lsof -n -i:5900
 is also good but insane

 Actually the *right* way to do this is by calling launchctl

 $ launchctl list 

 $ launchctl print system/com.apple.screensharing state

If it's enabled then properties will be returned including

state = waiting

Which seems to indicate it's configured to spawn screensharingd
If it's not enabled in Sharing prefs nothing will be returned

$ launchctl print system/com.apple.screensharing state
Could not find service "com.apple.screensharing" in domain for system

"""

import psutil
import re

from idiot import CheckPlugin


class ScreenSharingCheck(CheckPlugin):
    name = "ScreenSharing"

    def run(self):
        """
        Run the check.

        All check scripts must implement this method. It must return a tuple of:
        (<success>, <message>)

        In this example, if the check succeeds and the ScreenSharing process is nowhere
        to be found, the check will return (True, "No ScreenSharing processes found").

        If the check fails and an ScreenSharing process is found, it returns
        (False, "Found ScreenSharing processes with pids <pids>")
        """
        pids = []
        for p in psutil.process_iter():
            try:
                if (p.name() == 'ScreensharingAgent' or p.name() == 'screensharingd'):
                    pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass

        if len(pids):
            return (False, "Found ScreenSharing processes with pids: {} - Disable Sharing Prefs: Screen Sharing".format(', '.join([str(p) for p in pids])))
        else:
            return (True, "ScreenSharing is disabled")


if __name__ == "__main__":
    print(ScreenSharingCheck().run())
