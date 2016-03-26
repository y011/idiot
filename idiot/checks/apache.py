"""
Example check for Idiot.
"""

import psutil
import re

from idiot import CheckPlugin


class ApacheCheck(CheckPlugin):
    name = "Apache"

    def run(self):
        """
        Run the check.

        All check scripts must implement this method. It must return a tuple of:
        (<success>, <message>)

        In this example, if the check succeeds and the Apache process is nowhere
        to be found, the check will return (True, "No httpd processes found").

        If the check fails and an Apache process is found, it returns
        (False, "Found httpd processes with pids <pids>")
        """
        pids = []
        for p in psutil.process_iter():
            try:
                if p.name() == 'httpd':
                    pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass

        if len(pids):
            return (False, "Found httpd processes with pids: {}".format(', '.join([str(p) for p in pids])))
        else:
            return (True, "No httpd processes found")


if __name__ == "__main__":
    print(ApacheCheck().run())
