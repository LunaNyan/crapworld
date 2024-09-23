## 서버 구동 방법
> **Windows에서의 구동은 전혀 검증 및 고려되지 않았음.**

전체적인 과정은 해당 환경을 기준으로 한다.
- Ubuntu Server 22.04 (Jammy Jellyfish)
- Apache 2.4.62 `ondrej/apache2`

### 설정 변경
루트 디렉터리의 `conf.py`를 수정하여 변경할 수 있다.

자세한 설명은 파일 안에 쓰여 있다.

### Apache2를 통한 리버스 프록시

```text
<VirtualHost *:80>
        ServerName y2k.erpin.club
        Redirect permanent / https://y2k.erpin.club
</VirtualHost>

<VirtualHost *:443>
        ServerName y2k.erpin.club

        RewriteEngine On
        RewriteCond %{REQUEST_URI} /api/v[0-9]+/(users/)?websocket [NC,OR]
        RewriteCond %{HTTP:UPGRADE} ^WebSocket$ [NC,OR]
        RewriteCond %{HTTP:CONNECTION} ^Upgrade$ [NC]
        RewriteRule .* ws://127.0.0.1:11111%{REQUEST_URI} [P,QSA,L]

        <Location />
                Require all granted
                ProxyPass http://127.0.0.1:11111/
                ProxyPassReverse http://127.0.0.1:11111/
                ProxyPassReverseCookieDomain 127.0.0.1 y2k.erpin.club
        </Location>

        SSLCertificateFile {path to fullchain.pem}
        SSLCertificateKeyFile {path to privkey.pem}
        Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
```

### venv 생성

### systemd 서비스 생성

### 서버 시작
