import logging

from fabric import Connection, Config

import config
from domain.wifi import Wifi


class WifiAnsible(Wifi):

    @staticmethod
    def connection():
        configuration = Config(overrides={'user': config.ansible_username,
                                          'port': config.ansible_port,
                                          'sudo': {'password': config.ansible_password}})
        try:
            conn = Connection(host=config.ansible_host, config=configuration)
            return conn
        except Exception as e:
            logging.error(f"Erreur de connexion au serveur : {e}")

    def execute(self, *args):
        conn = WifiAnsible.connection()
        playbook = args[0]

        try:
            conn.run(f"ansible-playbook {playbook}")
            logging.info(f"Playbook {playbook} executé avec succès")
        except Exception as e:
            logging.error(f"Erreur d'execution du playbook : {e}")
