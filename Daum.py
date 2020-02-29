import requests
from bs4 import BeautifulSoup
import Main
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time


def daum():
    # 다음뉴스 헤드라인 긁어오기
    http=[]
    httz = 'https://media.daum.net/ranking/popular/'
    res = requests.get(httz)
    soup = BeautifulSoup(res.content, 'html.parser')
    body = soup.select('#mArticle > div.rank_news > ul.list_news2')
    body = body[0].find_all('a')


    for i in range(len(body)):
        t = body[i].get('href')
        http.append(t)

    # 중복제거
    http = list(set(http))

    text2 = []
    for i in range(len(http)):
        res = requests.get(http[i])
        soup = BeautifulSoup(res.content, 'html.parser')
        body = soup.select('.article_view')[0]
        text = " ".join(p.get_text() for p in body.find_all('p'))
        text2.insert(-1,text)


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


    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    tmp_data = dict(data_1)

    wordcloud = WordCloud(font_path='/Library/Fonts/NanumMyeongjo.ttf',
                          background_color='white', max_words=230).generate_from_frequencies(tmp_data)
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    plt.savefig("img/daum/daum_{}.png".format(date), bbox_inces='tight', dpi=400, pad_inches=0)