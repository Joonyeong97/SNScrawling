import Daum
import Naver
import time
import Twitter

def text():
    text = '코로나19'
    return text

# 사전을 추가해야함.
def sajun():
    sajun = ['트와이스', 'kf94', 'KF94', 'Kf94', 'kF94', '타임라인', '확진자', '예방수칙', '코로나19', 'corona19', 'Corona19',
             '개소리', '판매', '제품', '쿠팡', 'kf94마스크', 'KF94마스크', 'Kf94마스크', 'kF94마스크',
             '우한폐렴', '신종코로나', '신종코로나바이러스', 'coronavirus', 'Coronavirus', '사재기',
             '복지부장관', '바이러스', '피해복구', '이만희', '문재인', '이재갑', '한림대',
             '감염내과', '교수님', '정치인', '입국금지', '대변인', '청와대', '문대통령', '황기자', '신천지']
    return sajun


if __name__ == '__main__':
    Naver.naver()
    time.sleep(2)
    Daum.daum()
    time.sleep(2)
    Twitter.twitter()