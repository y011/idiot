# idiot

*Your best is an idiot.*

Idiot is an OS X tool to remind you not to be stupid.

* Ever turn off your firewall because that Meterpreter callback wasn't working and then forget to turn it back on?
* Ever run Apache to test something and forget to kill it?
* Ever spin up a MongoDB instance in Docker and accidentally leave it running with no password and a ton of production data in it?

Idiot is the tool for you. Idiot runs checks (written in Python) every now and then, and if it finds something is awry it will throw up a notification dialog and put an indicative icon in the OS X status bar. It will keep reminding you every time it checks, until you either "snooze" notifications for that particular check or defenstrate your machine.

Built-in checks:

* Apache
* Firewall

## Installation

Note: Eventually this will be a proper `.app` but there's a bug that needs to be addressed which means it doesn't work as a `py2app` target yet.

To install Idiot:

    $ python setup.py install

## Operation

Currently the app can only be run from the command line while the `py2app` issue is resolved. This has the side effect of always having an icon in the Dock.

A command line entry point is installed by the `setup.py` script. Run it:

    $ idiot

## Configuration

Create a file at `~/.idiot/config` to customise configuration. See `config/default.conf` in the package for more info. You can probably guess.

## Extending

See `checks/*` in the `idiot` package for examples.

User-defined checks are placed in `~/.idiot/checks`.

New checks must be explicitly enabled in config. Edit your `~/.idiot/config` and copy in the list of enabled checks from `config/default.conf`, then add your user check's class name to the list:

    enabled:
      - ApacheCheck
      - MyUserCheck

When testing, you might want to edit your config to enable debug loggin, make the checks run more frequently and lower the snooze intervals with a config like this:

    debug_logging:  true
    check_interval: 10
    snooze_intervals: [60, 120, 'forever']

## License

See LICENSE file.