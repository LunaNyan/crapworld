import conf
from flask import request


def if_local(req: request):
    ip = req.remote_addr
    # if localhost
    if ip.startswith("127."):
        if conf.cloudflare:
            cf_ip = req.headers.get('CF-Connecting-IP')
            return False, cf_ip
        else:
            return True, ip

    if ip.startswith("192.168.") or ip.startswith("10."):
        # Private IP A or C Class
        return True, ip
    elif ip.startswith("172."):
        ip2 = int(ip.split(".")[1])
        if 16 <= ip2 <= 31:
            return True, ip
        else:
            return False, ip
    else:
        return False, ip
