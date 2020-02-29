# conda install nltk
# conda install gensim
# pip install Pyro4
# pip install jpype1==0.7.1
# pip install konlpy
# pip install simplejson
# pip install pygame
# pip install pytagcloud
# pip install bs4
# pip install wordcloud
# pip install JPype1-0.7.1-cp37-cp37m-win_amd64.whl
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype
# jpype는 파이썬 버전따라서 해야함/ JAVA환경 갖추고서 진행


import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from konlpy.tag import Twitter
import numpy as np
from PIL import Image




def daumcrol():
    res = requests.get('https://sports.v.daum.net/v/20200211093546295')

    soup = BeautifulSoup(res.content, 'html.parser')
    body = soup.select('.article_view')[0]
    text = " ".join(p.get_text() for p in body.find_all('p'))
    t = Twitter()
    tokens_ko = t.nouns(text)
    ko = nltk.Text(tokens_ko, name="스포츠")
    ko.vocab().most_common(10)
    data = ko.vocab().most_common(500)
    tmp_data = dict(data)

    mask = np.array(Image.open("korea.jpg"))
    wordcloud = WordCloud( font_path = '/Library/Fonts/NanumMyeongjo.ttf',
                           background_color='white',mask=mask).generate_from_frequencies(tmp_data)
    plt.figure(figsize=(16,8))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

def naver_crol():
    res = requests.get('https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=374&aid=0000205683')

    soup = BeautifulSoup(res.content, 'html.parser')
    body = soup.select('._article_body_contents')[0]
    text = body.get_text() # for p in body.find_all('div'))
    t = Twitter()
    tokens_ko = t.nouns(text)
    ko = nltk.Text(tokens_ko, name="비상")
    ko.vocab().most_common(10)
    data = ko.vocab().most_common(1000)

    data_1 = []
    for i in range(len(data)):
        for q in range(0,1,1):
            if len(data[i][0]) >= 2 :
                data_1.append(data[i])

    tmp_data = dict(data_1)
    mask = np.array(Image.open("korea.jpg"))
    wordcloud = WordCloud( font_path = '/Library/Fonts/NanumMyeongjo.ttf',
                           background_color='white',mask=mask,max_font_size=40).generate_from_frequencies(tmp_data)
    plt.figure(figsize=(16,8))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

naver_crol()