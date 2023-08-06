import logging

from fabric import Connection, Config
import config
from domain.tools.nginx import Nginx


class NginxShell(Nginx):

    @staticmethod
    def connection():
        configuration = Config(overrides={'user': config.nginx_username,
                                          'port': config.nginx_port,
                                          'sudo': {'password': config.nginx_password},
                                          'connect_kwargs': {'password': config.nginx_password}})
        try:
            conn = Connection(host=config.nginx_host, config=configuration)
            return conn
        except Exception as e:
            logging.error(f"Erreur de connexion au serveur : {e}")

    @staticmethod
    def install_nginx(app_name: str):
        conn = NginxShell.connection()

        conn.put(config.nginx_config_file, app_name)

        commands = [
            'apt update',
            'apt install nginx -y',
            f'mkdir /var/www/{app_name}',
            f"mv {config.nginx_front_build_dir} /var/www/{app_name}",
            f"cp {app_name} /etc/nginx/sites-available",
            f"ln -s /etc/nginx/sites-available/{app_name} /etc/nginx/sites-enabled",
            f"rm /etc/nginx/sites-enabled/default",
            'sudo systemctl restart nginx']

        for command in commands:
            try:
                if config.use_sudo:
                    conn.sudo(command)
                else:
                    conn.run(command)
            except Exception as e:
                logging.error(f"Erreur d'installation de nginx : {e}")
