import requests
from bs4 import BeautifulSoup
import Main



def naver():
    # 네이버 헤드라인 가져오는소스
    text2 = []
    http = []
    httz = 'https://news.naver.com'
    res = requests.get(httz)
    soup = BeautifulSoup(res.content, 'html.parser')
    body = soup.select('#today_main_news > div.hdline_news > ul')
    body = body[0].find_all('a')
    for i in range(len(body)):
        t = body[i].get('href')
        http.append(t)


    # 헤드라인중 링크소스만 뽑아서 다시 들어가서 텍스트만 뽑아옴
    for i in range(len(http)):
        res = requests.get(httz + http[i])
        soup = BeautifulSoup(res.content, 'html.parser')
        body = soup.select('._article_body_contents')
        for t in body:
            text = t.get_text() # for p in body.find_all('div'))
            text2.insert(-1,text)

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

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    import time
    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    tmp_data = dict(data)

    wordcloud = WordCloud( font_path = '/Library/Fonts/NanumMyeongjo.ttf',
                           background_color='white',max_words=230).generate_from_frequencies(tmp_data)
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    plt.savefig("img/naver/naver_{}.png".format(date), bbox_inces='tight', dpi=400, pad_inches=0)