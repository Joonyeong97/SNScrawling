import requests
from bs4 import BeautifulSoup
import Main
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import os
import pandas as pd


def daum():
    cr_name = 'daum'
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


    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    date2 = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
    # 다음뉴스 헤드라인 긁어오기
    http=[]
    httz = 'https://media.daum.net/ranking/popular/?regDate={}'.format(date)
    res = requests.get(httz)
    soup = BeautifulSoup(res.content, 'html.parser')
    body = soup.select('#mArticle > div.rank_news > ul.list_news2')
    body = body[0].find_all('a')


    for i in range(len(body)):
        t = body[i].get('href')
        http.append(t)

    # 중복제거
    http = list(set(http))

    files = pd.DataFrame()
    for i in range(len(http)):
        res = requests.get(http[i])
        soup = BeautifulSoup(res.content, 'html.parser')
        body = soup.select('.article_view')[0]

        files = files.append(pd.DataFrame({
            'Title': soup.find('div', attrs={'class': 'head_view'}).h3.text,
            'Contents': " ".join(p.get_text() for p in body.find_all('p')),
            'link': http[i]
        }, index=[i]))
    text2 = files.Contents

    # 텍스트파일에 댓글 저장하기
    files.to_csv(text_save_path+'/다음뉴스종합_{}.csv'.format(date2),index=False,encoding='utf-8')



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


    # 다음뉴스는 50페이지 긁어오는거라서 1글자는 삭제했음. 필요한건 바로바로 보고서 사전에 추가해서 태깅 다시해야함.
    data_1 = []
    for i in range(len(data)):
        for q in range(0,1,1):
            if len(data[i][0]) >= 2 :
                data_1.append(data[i])





    tmp_data = dict(data_1)

    wordcloud = WordCloud(font_path='/Library/Fonts/NanumMyeongjo.ttf',
                          background_color='white', max_words=230).generate_from_frequencies(tmp_data)
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    plt.savefig(save_path+"/daum_{}.png".format(date), bbox_inces='tight', dpi=400, pad_inches=0)