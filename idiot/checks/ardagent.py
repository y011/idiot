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
import idiot
from idiot import ProcessCheck


class RemoteManagementCheck(ProcessCheck):
    name = "Remote Management"
    process_names = ["ARDAgent"]
    fail_msg = "enabled in Sharing Prefs: Remote Management - pids: {pids}"
    success_message = "disabled"


if __name__ == "__main__":
    print(RemoteManagementCheck().run())
