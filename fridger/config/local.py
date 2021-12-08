import os
import socket  # only if you haven't already imported this

from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True
    SECRET_KEY = "9d=e*jd2b6#=kn7i3h*rj%q&&f^f!$%c8h2bb8a*xs6khargq5"
    # Email backend to not send email just print content in console
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
