import smtplib
from config import Config

class ServerSMTP():

    _instances = {}

    def __init__(self):
        self.server = smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT) # Instância encapsula uma conexão SMTP
        self.server.ehlo() # Identifique-se em um servidor ESMTP usando EHLO
        self.server.starttls() # Coloca a conexão SMTP no modo TLS. Todos os comandos SMTP a seguir serão criptografados.
        self.login_server() # Login em um servidor SMTP que requer autenticação


    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            instance = super().__call__(*args, **kwargs)
            self._instances[self] = instance
        return self._instances[self]


    def login_server(self):
        self.server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD) # Login em um servidor SMTP que requer autenticação


    def close_server(self):
        self.server.quit() # Fecha a conexão SMTP
