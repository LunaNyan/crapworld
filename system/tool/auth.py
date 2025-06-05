import conf
from system.engine.settings import site_settings
from flask import request, session
from argon2 import PasswordHasher
from uuid import uuid4
import yaml

ph = PasswordHasher()
login_session = None


def get_shadow():
    with open("data/shadow.yaml", "r", encoding="utf-8") as j:
        shadow = yaml.load(j, yaml.FullLoader)
    return shadow


def set_account(username, passwd):
    d = {"username": username, "passwd": ph.hash(passwd), "session_key": uuid4().hex}
    with open("data/shadow.yaml", "w", encoding="utf-8") as j:
        yaml.dump(d, j, allow_unicode=True)


def is_admin(req: request):
    return True  # TODO : 만들기


def is_local_ip(req: request):
    # use_admin이 false면 뭔 짓을 해도 False가 나오도록 한다.
    if not site_settings()["use_admin"]:
        return False, ""
    ip = req.remote_addr
    # if localhost
    if ip.startswith("127."):
        if conf.cloudflare:
            cf_ip = req.headers.get('CF-Connecting-IP')
            return False, cf_ip
        else:
            return True, ip
    elif ip.startswith("192.168.") or ip.startswith("10."):
        # Private IP A or C Class
        return True, ip
    elif ip.startswith("172."):
        ip2 = int(ip.split(".")[1])
        if 16 <= ip2 <= 31:
            return True, ip
        else:
            return False, ip
    elif ip.startswith("100."):
        ip2 = int(ip.split(".")[1])
        if 64 <= ip2 <= 127:
            return True, ip
        else:
            return False, ip
    else:
        return False, ip
