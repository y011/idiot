"""
Idiot check for Apple Remote Desktop management with ARDAgent

purpose: indicates if Sharing Preferences: Remote Management using Apple Remote Desktop management is permitted to this
    machine

daemon: 
    /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/MacOS/ARDAgent

requirement: ARD permits remote execution and beyond as the accessing or 
    logged in user. Also permits remote console/interactive access of course
"""

import psutil
import re

from idiot import CheckPlugin


class ARDAgentCheck(CheckPlugin):
    name = "ARDAgent"

    def run(self):
        """
        Run the check.

        All check scripts must implement this method. It must return a tuple of:
        (<success>, <message>)

        In this example, if the check succeeds and the ARDAgent process is nowhere
        to be found, the check will return (True, "No ARDAgent processes found").

        If the check fails and an ARDAgent process is found, it returns
        (False, "Found ARDAgent processes with pids <pids>")
        """
        pids = []
        for p in psutil.process_iter():
            try:
                if p.name() == 'ARDAgent':
                    pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass

        if len(pids):
            return (False, "Found ARDAgent processes with pids: {} - Disable Sharing Prefs: Remote Management".format(', '.join([str(p) for p in pids])))
        else:
            return (True, "ARDAgent is disabled")


if __name__ == "__main__":
    print(ARDAgentCheck().run())
