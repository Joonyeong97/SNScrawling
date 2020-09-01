from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import Main
from ckonlpy.tag import Twitter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import chromedriver


result = []

def cleanText(readData):
    # 텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》\n_·李永钦타임라인레]', '', readData)
    return text

# 코로나 바이러스
def twitter():
    cr_name = 'twitter'
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


    import time
    import nltk
    keyword = Main.text()

    # 웹 셋팅
    chrome = chromedriver.generate_chrome(
        driver_path=Main.driver_path,
        headless=Main.headless,
        download_path=Main.DOWNLOAD_DIR)

    # 웹접속 - 네이버 이미지 접속
    print("Twitter 접속중")
    # driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    # driver.implicitly_wait(30)

    url = 'https://twitter.com/search?q={}&src=typed_query'.format(keyword)
    chrome.get(url)
    time.sleep(3)


    # text2 = chrome.find_elements_by_css_selector('#react-root > div > div > div > main > div > div > div > div > div > div:nth-child(2) > div')


    # for i in range(15):
    #     for q in range(3):
    #         body = chrome.find_element_by_css_selector('body')
    #         body.send_keys(Keys.PAGE_DOWN)
    #         time.sleep(1)
    #     for ttt in tqdm(text2):
    #         result.append(ttt.text)
    #     time.sleep(1)
    #
    #
    # result2 = []
    # for i in range(len(result)):
    #     if i % 2 == 0:
    #         result2.append(result[i])
    # print(len(result2))
    #
    # result3 = []
    # for i in range(len(result2)):
    #     result3.append(cleanText(result2[i]))

    body = chrome.find_element_by_css_selector('body')
    text2 = chrome.find_elements_by_css_selector('#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > div > section > div')

    for i in range(10):
        for q in range(3):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        for ttt in tqdm(text2):
            result.append(re.sub('\n', '', ttt.text))

    t = Twitter()
    t.add_dictionary(Main.sajun(), 'Noun')

    tokens_ko = []

    for i in range(len(result)):
        tokens_ko.append(t.nouns(result[i]))
    final = []
    for _, q in enumerate(tokens_ko):
        for i in range(len(q)):
            final.insert(-1, q[i])

    ko = nltk.Text(final, name="첫번째")
    data = ko.vocab().most_common(1000)
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    date2 = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))


    # 텍스트파일에 댓글 저장하기
    file = open(text_save_path+'/twitter{}.txt'.format(date2), 'w', encoding='utf-8')

    for review in result:
        file.write(review + '\n')

    file.close()

    tmp_data = dict(data)

    wordcloud = WordCloud(font_path='/Library/Fonts/NanumMyeongjo.ttf',
                          background_color='white', max_words=230).generate_from_frequencies(tmp_data)
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    plt.savefig(save_path+"/twitter_{}.png".format(date), bbox_inces='tight', dpi=400, pad_inches=0)