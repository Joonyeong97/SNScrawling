import requests
from bs4 import BeautifulSoup
import Main
import os
import pandas as pd
import re
import chromedriver


def cleanText(readData):
    # 텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》\n_·李永钦▶]', '', readData)
    return text

def naver():
    from selenium import webdriver
    import re
    from selenium.webdriver.common.keys import Keys
    import time
    cr_name = 'naver'
    # 이미지파일 저장 장소 확인
    save_path = os.path.join(Main.img_path, cr_name)
    if os.path.isdir(save_path):
        print(cr_name + ' 이미지 경로 확인 완료')
    elif os.path.isdir(Main.img_path):
        os.mkdir(save_path)
    else:
        os.mkdir(Main.img_path)
        os.mkdir(save_path)

    text_save_path = os.path.join(Main.text_path, cr_name)
    if os.path.isdir(text_save_path):
        print(cr_name + ' 텍스트 경로 확인 완료')
    elif os.path.isdir(Main.text_path):
        os.mkdir(text_save_path)
    else:
        os.mkdir(Main.text_path)
        os.mkdir(text_save_path)


    # 네이버 헤드라인 가져오는소스


    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    date2 = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))

    result = []
    res = []

    # 웹 셋팅
    chrome = chromedriver.generate_chrome(
        driver_path=Main.driver_path,
        headless=Main.headless,
        download_path=Main.DOWNLOAD_DIR)

    # 웹접속 - 네이버 이미지 접속
    print("Naver 접속중")
    # driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    # driver.implicitly_wait(30)

    url = 'https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&date={}'.format(date)
    chrome.get(url)
    time.sleep(2)

    # scroll(3)
    for sun in range(4, 10):
        pr = chrome.find_elements_by_xpath('//*[@id="wrap"]/table/tbody/tr/td[2]/div/div[{}]'.format(sun))
        for p in pr:
            result.append(p.find_elements_by_tag_name('a'))
        # print(result)

        for i, q in enumerate(result):
            for e in q:
                res.append(e.get_attribute('href'))
    http = list(set(res))
    len(http)
    https = []

    for idx in range(len(http)):
        if http[idx].find('popularDay') >= 0:
            continue
        else:
            https.append(http[idx])

    files = pd.DataFrame()

    for i in range(len(https)):
        res = requests.get(https[i])
        soup = BeautifulSoup(res.content, 'html.parser')
        body = soup.select('._article_body_contents')
        files = files.append(pd.DataFrame({
            'Title': soup.find('div', attrs={'class': 'article_info'}).h3.text,
            'Contents': re.sub('   ', '', re.sub('    ', '', re.sub('\t', '',cleanText(body[0].text)[(cleanText(body[0].text)).find('{}') + 2:]))),
            'link': https[i]},
            index=[i]))

    text2 = files.Contents
    # 텍스트파일에 저장 csv
    files.to_csv(text_save_path+'/네이버종합뉴스_{}.csv'.format(date2),index=False,encoding='utf-8')

 # -------------------------------------

    # 사전만들기
    from ckonlpy.tag import Twitter
    t = Twitter()
    t.add_dictionary(Main.sajun(), 'Noun')

    import nltk
    tokens_ko = []

    for i in range(len(text2)):
        tokens_ko.append(t.nouns(text2[i]))

    final = []
    for _,q in enumerate(tokens_ko):
        for i in range(len(q)):
            final.insert(-1,q[i])


    ko = nltk.Text(final, name="첫번째")
    data = ko.vocab().most_common(1000)

    data_1 = []
    for i in range(len(data)):
        for q in range(0,1,1):
            if len(data[i][0]) >= 2 :
                data_1.append(data[i])

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    import time
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    date2 = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))


    tmp_data = dict(data_1)

    wordcloud = WordCloud( font_path = '/Library/Fonts/NanumMyeongjo.ttf',
                           background_color='white',max_words=230).generate_from_frequencies(tmp_data)
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    plt.savefig(save_path+"/naver_{}.png".format(date), bbox_inces='tight', dpi=400, pad_inches=0)