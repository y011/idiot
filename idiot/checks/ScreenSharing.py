"""
Idiot check for ScreenSharing

purpose: indicates if Sharing Preferences: Screen Sharing / VNC is permitted to 
    this machine

daemons:
    /System/Library/CoreServices/RemoteManagement/screensharingd.bundle/Contents/MacOS/screensharingd
    /System/Library/CoreServices/RemoteManagement/ScreensharingAgent.bundle/Contents/MacOS/ScreensharingAgent

requirement: ScreenSharing permits remote console/interactive access.
This checks both launchd enabling the above and manually starting them.

info:
We're only checking launchd for this service. Not sure if this can be manually 
invoked without it needing other launchd XPC kicked stuff like kdc.

Detecting this is tricky because until it's accessed neither of the above are 
forked as processes visible in process table. Once a system has been accessed, 
though, these processes remain until Sharing:Screen Sharing is disabled

 One way to check this is by calling launchctl

 $ launchctl print system/com.apple.screensharing

If it's enabled then properties will be returned (with return code 0) including

state = waiting

Which seems to indicate it's configured to spawn screensharingd

If it's not enabled in Sharing prefs nothing will be returned (except a non-0
return code like 113)

$ launchctl print system/com.apple.screensharing state
Could not find service "com.apple.screensharing" in domain for system

"""
import logging
import subprocess
import os
import psutil

import idiot
from idiot import CheckPlugin

log = logging.getLogger()

class ScreenSharingCheck(CheckPlugin):
    name = "Screen Sharing"

    def run(self):
        with open(os.devnull, 'w') as devnull:
            try:
                # If the service is disabled in Preferences
                # the query returns a non-zero error
                # should use this query better in future
                if subprocess.check_call(['launchctl', 'print', 'system/com.apple.screensharing'], stdout=devnull, stderr=devnull):
                    return (True, "Dat")
                else:
                    return (False, "enabled in Sharing Prefs: Screen Sharing")           
            except subprocess.CalledProcessError as e:
                # this only gets run if screensharing isn't enabled by
                # launchd as checked above
                """
                pids = []
                for p in psutil.process_iter():
                    try:
                        if (p.name() == 'ScreensharingAgent' or p.name() == 'screensharingd'):
                            pids.append(p.pid)
                    except psutil.NoSuchProcess:
                        pass
                if len(pids):
                    return (False, "enabled manually - see pids: {} ".format(', '.join([str(p) for p in pids])))
                else:
                    """
                return (True, "disabled")

if __name__ == "__main__":
    idiot.init()
    print(ScreenSharingCheck().run())