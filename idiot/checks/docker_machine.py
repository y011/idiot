"""
docker-machine check for Idiot.
"""
import logging
import subprocess

import idiot
from idiot import CheckPlugin

log = logging.getLogger()


class DockerMachineCheck(CheckPlugin):
    name = "Docker machine"

    def run(self):
        try:
            output = subprocess.check_output("docker-machine ls", shell=True).split('\n')[1:]
            running = [line.split()[0] for line in output if 'Running' in line]
            if len(running):
                return (False, "Docker machines are running: {}".format(', '.join(running)))
            else:
                return (True, "No Docker machines are running")
        except Exception as e:
            log.exception("Failed to get `docker-machine ls` output")
            return (False, "Failed to get `docker-machine ls` output")


if __name__ == "__main__":
    idiot.init()
    print(DockerMachineCheck().run())
