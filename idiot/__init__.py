# -*- coding: utf-8 -*-
import rumps
import AppKit
import logging
import datetime
import random

from scruffy import *
from Foundation import *

OK_TITLES = [u"😏", u"😁", u"😃", u"😄", u"😆"]
NOT_OK_TITLES = [u"🚑"]


def init():
    global env, config, log
    env = Environment(
        main_dir=Directory(
            '~/.idiot', create=True,
            config=ConfigFile('~/.idiot/config', defaults=File('config/default.conf', parent=PackageDirectory())),
            user_checks=PluginDirectory('checks'),
            log=LogFile('idiot.log', logger='')
        ),
        pkg_checks=PluginDirectory('checks', parent=PackageDirectory())
    )
    config = env.config
    log = logging.getLogger()
    if config.debug_logging:
        log.setLevel(logging.DEBUG)


@rumps.notifications
def notification_center(info):
    if info['activationType'] == 2:
        app.cm.snooze(info['name'])


class CheckPlugin(Plugin):
    name = 'Unknown'
    snooze_until = None
    snooze_index = -1
    snooze_intervals = None
    last_result = (True, "Not run yet")

    def __init__(self):
        # if custom snooze intervals are not defined for this check, use the config's
        if self.snooze_intervals is None:
            self.snooze_intervals = config.snooze_intervals.to_dict()

    def snooze(self):
        """
        Disable notifications for this check for a period.
        """
        # increment snooze index, but not past the number of intervals
        self.snooze_index += 1
        self.snooze_index = min(self.snooze_index, len(self.snooze_intervals) - 1)

        if self.snooze_intervals[self.snooze_index] == 'forever':
            # snooze forever
            log.debug("Snoozing check {} forever".format(self))
            self.snooze_until = True
        else:
            # set snooze until time to now + the currently selected interval
            self.snooze_until = datetime.datetime.now() + datetime.timedelta(seconds=self.snooze_intervals[self.snooze_index])
            log.debug("Snoozing check {} until {}".format(self, self.snooze_until))

    @property
    def snoozing(self):
        """
        Return a boolean indicating whether or not the check is currently
        snoozing (notifications are disabled).
        """
        if self.snooze_until is None:
            return False
        elif self.snooze_until is True:
            # snoozing forever
            return True
        else:
            return datetime.datetime.now() < self.snooze_until

    def run(self):
        """
        Run the check. Subclasses must implement this method.
        """
        return (False, "Subclass hasn't implemented the `run` method.")


class CheckManager(PluginManager):
    last_ok = True

    def __init__(self):
        self._checks = []
        for cls in PluginRegistry.plugins:
            if cls.__name__ != "CheckPlugin":
                if cls.__name__ in config.enabled:
                    if cls.name != "Unknown":
                        log.info("Loaded plugin {}".format(cls.__name__))
                        check = cls()
                        self._checks.append(check)
                    else:
                        log.error("Plugin {} needs a `name` property set. Not loading.".format(cls))
                else:
                    log.info("Did not load plugin {}".format(cls.__name__))

    @property
    def checks(self):
        return self._checks

    @checks.setter
    def checks(self, value):
        self._checks = value

    def check_named(self, name):
        [check] = [c for c in self._checks if c.name == name]
        return check

    def snooze(self, check_name):
        self.check_named(check_name).snooze()

    def run_checks(self, _=None):
        log.debug("Running checks")
        all_ok = True
        for check in self.checks:
            log.debug("Running check {}".format(check))
            success, msg = check.run()
            check.last_result = (success, msg)
            if success:
                log.debug("Success: {}".format(msg))
            else:
                all_ok = False
                log.error("Fail: {}".format(msg))
                if not check.snoozing:
                    log.debug("Sending notification")
                    rumps.notification("{} check failed".format(check.name), "", msg, data={"name": check.name},
                                       actionButton="Snooze", otherButton="Dismiss")
                else:
                    log.debug("Check is snoozing until {} - not sending notification".format(check.snooze_until))

        try:
            if self.last_ok != all_ok:
                self.last_ok = all_ok
                if all_ok:
                    app.title = random.choice(OK_TITLES)
                else:
                    app.title = random.choice(NOT_OK_TITLES)

            app.update_menu()
        except NameError:
            log.error("No app")


class IdiotApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super(IdiotApp, self).__init__(*args, **kwargs)
        self.title = random.choice(OK_TITLES)
        self.cm = CheckManager()
        self.quit_button = None
        self.update_menu()
        self.timer = rumps.Timer(self.cm.run_checks, config.check_interval)
        self.timer.start()

    def update_menu(self):
        def dummy(*args, **kwargs):
            pass

        for item in self.menu:
            del self.menu[item]
        menu = []
        for check in self.cm.checks:
            (success, msg) = check.last_result
            item = rumps.MenuItem("{} ({})".format(check.name, msg), callback=dummy)
            item.state = 1 if success else -1
            menu.append(item)
        self.menu = menu + [None, rumps.MenuItem('Quit', callback=rumps.quit_application)]


def main():
    global app
    init()
    app = IdiotApp("Idiot")
    app.run()
