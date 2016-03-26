"""
Idiot check for FileSharing via SMB or AFP is on

purpose: indicates if Sharing Preferences: File Sharing using SMB or AFP is 
    permitted to this machine

daemons: 
    /usr/sbin/AppleFileServer
    /usr/sbin/smbd

requirement: oversharing is always bad


These are managed by launchd (as seen below) but I'm not sure how just yet. Not 
directly but from something else.

$ sudo lsof -n -i tcp:548
COMMAND    PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
launchd      1  root   30u  IPv4 0x57975ec6347d4d57      0t0  TCP *:afpovertcp (LISTEN)
launchd      1  root   63u  IPv6 0x57975ec62c9c40b7      0t0  TCP *:afpovertcp (LISTEN)
AppleFile 4704  root    3u  IPv4 0x57975ec6347d4d57      0t0  TCP *:afpovertcp (LISTEN)
AppleFile 4704  root    4u  IPv6 0x57975ec62c9c40b7      0t0  TCP *:afpovertcp (LISTEN)
AppleFile 4704  root   12u  IPv6 0x57975ec62c9c4617      0t0  TCP [::1]:afpovertcp->[::1]:51743 (ESTABLISHED)

$ ps -ax |grep -i AppleFile
 4704 ??         0:00.05 /usr/sbin/AppleFileServer


$ sudo lsof -n -i tcp:445
COMMAND  PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
launchd    1  root   67u  IPv4 0x57975ec62ea0a65f      0t0  TCP *:microsoft-ds (LISTEN)
launchd    1  root   68u  IPv6 0x57975ec62c9c4b77      0t0  TCP *:microsoft-ds (LISTEN)
smbd    4967  root    4u  IPv4 0x57975ec62ea0a65f      0t0  TCP *:microsoft-ds (LISTEN)
smbd    4967  root    5u  IPv6 0x57975ec62c9c4b77      0t0  TCP *:microsoft-ds (LISTEN)
smbd    4967  root    6u  IPv6 0x57975ec62c9c4617      0t0  TCP [::1]:microsoft-ds->[::1]:51853 (ESTABLISHED)

$ ps -ax |grep -i smb
 4728 ??         0:00.01 /usr/sbin/smbd


Might be from com.apple.sharingd although I think that's more client functions for mDNS-happy sharing fun
"""

import psutil
import re

from idiot import CheckPlugin


class FileSharingCheck(CheckPlugin):
    name = "FileSharing"

    def run(self):
        """
        Run the check.

        All check scripts must implement this method. It must return a tuple of:
        (<success>, <message>)

        In this example, if the check succeeds and FileSharing processes are nowhere
        to be found, the check will return (True, "No FileSharing processes found").

        If the check fails and an FileSharing process is found, it returns
        (False, "Found SMB or AFP FileSharing processes with pids <pids>")
        """
        pids = []
        for p in psutil.process_iter():
            try:
                if (p.name() == 'AppleFileServer' or p.name() == 'smbd'):
                    pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass

        if len(pids):
            return (False, "Found SMB or AFP FileSharing processes with pids: {} - Disable Sharing Prefs: File Sharing".format(', '.join([str(p) for p in pids])))
        else:
            return (True, "FileSharing is disabled")


if __name__ == "__main__":
    print(FileSharingCheck().run())
