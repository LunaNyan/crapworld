def check_trait(text, mode=False):
    """
    한글 문장을 검사하여 적절한 조사를 str로 리턴한다.
    text (str) : 조사 판단에 사용될 문장
    mode (bool) : 어떤 형태의 조사를 리턴할지 정한다. 기본값은 False이다.
      - True : 을 / 를
      - False : 이 / 가
    """
    if int((ord(text[-1:]) - 0xAC00) % 28) != 0:
        res = "을" if mode else "이"
    else:
        res = "를" if mode else "가"
    return res
