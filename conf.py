# 웹 서버 설정
# 사이트 설정은 data에 있다.

# Flask dev mode가 켜지고 디버그 탭이 활성화된다.
# !! : 해당 변수와 관계없이 터미널에 표출되는 로그의 레벨은 DEBUG로 설정된다.
debug = False

# 사이트 렌더링 시마다 site_settings.yaml을 다시 로드할 지의 여부
# 개발 환경이 아닌 경우 False로 놓는 것을 권장한다.
dynamically_reload_site_settings = True

# 서버 호스트
listen_host = "0.0.0.0"
# 서버 포트
# Docker 환경에서는 11111로 둔다.
listen_port = 11111
