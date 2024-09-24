# 싸구려월드
![thumb.png](_docs/thumb.png)

**테무에서 산 싸이월드**

싸이월드 미니홈피에 모티브를 두고 개발중인 개인 웹사이트 프레임워크(=토이 프로젝트)입니다.

다이어리 기능이 구현되어 있습니다.

## 어떻게 돌립니까?

1. Python venv를 준비합니다. 개발 환경이 3.10이었으며, 3.12에서 테스트 되었습니다.
2. `data/site-settings.json`을 수정합니다.
3. `python3 y2k_server.py`를 실행합니다. 개발 모드로 서버를 실행시키며, 사이트의 기능들을 확인해볼 수 있습니다.
4. [이 가이드](https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/)를 참조하여 `waitress-serve --port=(포트 번호) --call y2k_server:create_site`를 실행합니다. 이 명령어는 프로덕션 모드로 서버를 구동합니다.

## TODO
- [ ] 테마 모딩 기능
- [ ] 방명록
- [ ] 다이어리 댓글 작성
- [ ] 사이트 관리 도구
