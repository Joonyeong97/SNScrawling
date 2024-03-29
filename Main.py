import Daum
import Naver
import time
import Twitter
import os
import sys



# 필수 확인
# 84.0.4147.30 / chrome version
# 현재 설치되어 있는 크롬 드라이버 확인 후 적용바람
# https://chromedriver.chromium.org/downloads

# 필수 라이브러리
# pip install customized_konlpy
# pip install wordcloud
# pip install selenium

PROJECT_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(PROJECT_DIR,'download')
driver_path = os.path.join(PROJECT_DIR, 'lib/webDriver')

# GUI 창 설정 (True = GUI 안함, False = GUI)
headless = True

# OS 확인
platform = sys.platform
if platform == 'darwin':
    print('System platform : Darwin')
    driver_path = os.path.join(driver_path, 'chromedriver_mac')
elif platform == 'linux':
    print('System platform : Linux')
    driver_path = os.path.join(driver_path, 'chromedriver_linux')
elif platform == 'win32':
    print('System platform : Window')
    driver_path = os.path.join(driver_path,'chromedriver_win.exe')
else:
    print(f'[{sys.platform}] 지원하지 않는 운영체제입니다. 확인 바랍니다.')
    raise Exception()


# 저장을 원하는 경로 설정 / 현재 경로
img_save_path = os.getcwd()


# 변경금지
output_path = os.path.join(img_save_path,'OutPut_File')
img_path = os.path.join(output_path,'img')
text_path = os.path.join(output_path,'text')

if os.path.isdir(output_path):
    pass
else:
    os.mkdir(output_path)

def text():
    # 트위터 검색어
    text = '재난지원금'
    return text

# 단어사전을 추가해야함. / 워드클라우드 사용시 사용됩니다.
def sajun():
    sajun = ['트와이스', 'kf94', 'KF94', 'Kf94', 'kF94', '타임라인', '확진자', '예방수칙', '코로나19', 'corona19', 'Corona19',
             '개소리', '판매', '제품', '쿠팡', 'kf94마스크', 'KF94마스크', 'Kf94마스크', 'kF94마스크',
             '우한폐렴', '신종코로나', '신종코로나바이러스', 'coronavirus', 'Coronavirus', '사재기',
             '복지부장관', '바이러스', '피해복구', '이만희', '문재인', '이재갑', '한림대',
             '감염내과', '교수님', '정치인', '입국금지', '대변인', '청와대', '문대통령', '황기자', '신천지', '근로장려금',
             '까페', '배달', '페미', '항체', '에휴', '미래통합당', '자유한국당', '민주통합당', '3사',
             '이동통신', '갤럭시', '갤럭시S20', '감염병', '난리', '순방', '신천지','신천지사이트','쿠팡',
             '쿠팡플렉스', 'coupang flex', '배급제', '1인2매','마스크','이덴트','수출길','마스크5부제',
             '신천지연예인명단','신천지연예인','세계여성의날','식약처','양금희','시진핑','주석',
             '보건당국','구로콜센터','실거래','공적마스크','WHO','사무총장','큐넷','팬데믹','펜대믹','팬대믹',
             'pandemic','Pandemic','1800선','코스피','코스피하락','최악','급락','트럼프','cospi','cosdac','사이드카',
             '망했다','10년전','IMF','거품','금융버블','금융위기','붕괴','순매수','순매도','공매도','공매도금지법',
             '금융위원회', '한국거래소', '주지훈', '하이에나','은혜의강교회','사이비종교','집단감염','신도','카톡','카톡에러',
             '개학연기','신형아반떼','현대자동차','아반떼','Avante','1500선붕괴','1400선','n번방','n번방사건','텔레그램',
             '소신발언','벗방','그것이알고싶다','카르텔','사이버성폭력','강력처벌','BJ','그알','셀트리온','코로나항체','항체개발',
             '7월내','조주빈','N번방박사','한타바이러스','중국바이러스','설치류','중국','초중고','EBS특강','EBS','온라인강의',
             '포털서비스','네이버','카카오','라이브특강','라이브특강','접속자폭주','피파온라인4','상반기','로스터업데이트',
             '넥슨','후베이성','우한폭동','봉쇄풀린','두달만에','손석희','JTBC','삼성','긴급재난지원금','복지로',
             '중산층','소득분위','70%','150%','중위소득','재난지원금']
    return sajun


if __name__ == '__main__':
    Naver.naver()
    time.sleep(2)
    Daum.daum()
    time.sleep(2)
    Twitter.twitter()