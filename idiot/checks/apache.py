"""
Example check for Idiot.
"""

import idiot
from idiot import ProcessCheck


class ApacheCheck(ProcessCheck):
    name = "Apache"
    process_names = ["httpd"]


if __name__ == "__main__":
    print(ApacheCheck().run())
