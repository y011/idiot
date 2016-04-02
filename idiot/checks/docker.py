"""
Docker container check for Idiot.
"""
import logging
import subprocess

import idiot
from idiot import CheckPlugin

log = logging.getLogger()


class DockerCheck(CheckPlugin):
    name = "Docker"

    def run(self):
        try:
            output = subprocess.check_output(['/usr/local/bin/docker-machine', 'ls']).split('\n')[1:]
            running = [line.split()[0] for line in output if 'Running' in line]

            for dm in running:
                log.debug("Enumerating docker-machine {}".format(dm))
                env = subprocess.check_output(['docker-machine', 'env', dm])
                ps = subprocess.check_output('\n'.join([env, 'docker ps']), shell=True).split('\n')[1:]
                images = [line.split()[1] for line in ps if len(line)]
                if len(images):
                    return (False, "docker containers are running: {}".format(', '.join(images)))
                else:
                    return (True, "no Docker containers are running")
        except Exception as e:
            log.exception("Failed to enumerate docker containers")
            return (False, "failed to enumerate docker containers")

        return (True, "no Docker machines are running")


if __name__ == "__main__":
    print(DockerCheck().run())
