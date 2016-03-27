"""
Idiot check for sshd / Remote Login

purpose: indicates if "Sharing Preferences: Remote Login" or OpenSSH's sshd is
    otherwise running

daemon:
    /usr/sbin/sshd

requirement: sshd provides interactive access with valid creds. Best left off.



info:
Detecting this is tricky because until it's accessed launchd hasn't
forked the sshd process so there's nothing visible in process table.
While a system is being accessed (or scanned even), though, the sshd process
is visible. Once a session ends (or login times out) the sshd process exits
leaving launchd to listen for the SSH client to connect

The correct way to check for this being enabled is using launchctl
checking output of:

$ launchctl print system/com.openssh.sshd state

which would have state = waiting which indicates it's configured to spawn sshd.
If it's not enabled in Sharing prefs nothing will be returned:

    $ launchctl print system/com.openssh.sshd state
    Could not find service "com.openssh.sshd" in domain for system

checking the pid is easier and, much more importantly, would catch
a manually invoked sshd left behind from, say, an rsync serving or a breach
(you pick)

"""

import psutil
import re

import idiot
from idiot import CheckPlugin


class SSHDCheck(CheckPlugin):
    name = "sshd"

    def run(self):
        """
        Run the check.

        All check scripts must implement this method. It must return a tuple of:
        (<success>, <message>)

        In this example, if the check succeeds and the sshd process is nowhere
        to be found, the check will return (True, "No sshd processes found").

        If the check fails and an sshd process is found, it returns
        (False, "Found sshd processes with pids <pids>")
        """
        pids = []
        for p in psutil.process_iter():
            try:
                if p.name() == 'sshd':
                    pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass

        if len(pids):
            return (False, "Found sshd processes with pids: {} - Disable Sharing Prefs: Remote Login".format(', '.join([str(p) for p in pids])))
        else:
            return (True, "sshd is disabled")


if __name__ == "__main__":
    idiot.init()
    print(SSHDCheck().run())
