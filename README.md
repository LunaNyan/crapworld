# 싸구려월드
![title01.png](_docs/title01.png)

**테무에서 산 싸이월드**

싸이월드 미니홈피를 재구현한 [Flask](https://flask.palletsprojects.com/en/3.0.x/) 웹 애플리케이션입니다.

## 어떻게 돌립니까?
### 직접 구성하기
1. Python venv를 준비합니다. 개발 환경이 3.11이었으며, 3.12에서 테스트 되었습니다.
2. `pip install -r requirements.txt`를 실행합니다. 앱 동작에 필요한 PyPI 디펜던시를 설치합니다.
3. `conf.py`를 수정합니다.
4. `python3 y2k_server.py`를 실행합니다.
5. data 디렉터리가 초기화되었습니다. `site_settings.yaml`을 포함한 사이트 구성을 취향에 맞게 변경합니다.

### Docker
> **Rocky Linux 9.4(x86_64), podman 4.9**를 기준으로 합니다. 배포판 및 Docker 설치 형태에 따라 일부 내용에 차이가 있을 수 있습니다.
```shell
# 이미지 빌드
docker build -t crapworld .
# 컨테이너를 만들고 실행
docker run -v [data가 저장될 장소]:/app/data -p [원하는 포트]:11111 --name [컨테이너 이름] crapworld
```

## 라이센스
싸구려월드는 오픈 소스 프로젝트이며, [BSD 3-Clause](https://www.olis.or.kr/license/Detailselect.do?lId=1092) 라이센스로 제공됩니다.

해당 프로젝트를 사용하고자 하는 경우, 라이센스를 준수해야 합니다.

자세한 내용은 `LICENSE`를 참조하십시오.

## TODO
### 만들 것들
- [x] 커스텀 테마
- [x] (홈) 오늘의 기분
- [x] 사진첩 / 갤러리 (= Instagram / X 피드)
- [x] 방명록 / 게시판 (= Quesdon@Planet)
- [x] 프로필
- [x] 사진첩
- [x] 동영상 (= YouTube)
- [ ] 사이트 관리 도구
### 만들 것들 (후순위)
- [ ] 쥬크박스
- [ ] 일촌평
- [ ] 자체 방명록
- [ ] 다이어리 댓글 작성
- [x] Dockerfile
### 개선할 것들
- [ ] (상시 퀘스트) 성능 개선이 가능한 로직을 [정상화](https://youtu.be/cYRkZmBuDqI)
  - [ ] 캐싱 루틴 도입
- [ ] 사진첩 이미지를 썸네일화하여 트래픽 및 로딩 시간 절감
- [ ] 방명록을 Quesdon@Planet으로 대체하는건 좋은 방법이 아닌 것 같음
- [ ] 테마를 css-only화
- [ ] docs가 필요함
