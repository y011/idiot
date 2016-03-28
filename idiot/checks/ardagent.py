"""
Idiot check for Apple Remote Desktop management with ARDAgent

purpose: indicates if Sharing Preferences: Remote Management using Apple Remote Desktop management is permitted to this
    machine

daemon:
    /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/MacOS/ARDAgent

requirement: ARD permits remote execution and beyond as the accessing or
    logged in user. Also permits remote console/interactive access of course
    This checks both launchd enabling ARDAgent and manually starting ARDAgent
    ARDAgent is defined in launchd (seen in launchctl list but doesn't output config
    from a launchctl print. The PID-based check is what actually detects ARDAgent
    but we'll try to check the launchctl one too later

"""
import logging
import subprocess
import os
import psutil

import idiot
from idiot import CheckPlugin

log = logging.getLogger()


class RemoteManagementCheck(CheckPlugin):
    name = "Remote Management"

    def run(self):
        pids = []
        for p in psutil.process_iter():
            try:
                if p.name() == "ARDAgent":
                    pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass
        if len(pids):
            return (False, "enabled in Sharing Prefs: Remote Management - pids: {}".format(', '.join([str(p) for p in pids])))
        else:
            return (True, "disabled")

if __name__ == "__main__":
    print(RemoteManagementCheck().run())
