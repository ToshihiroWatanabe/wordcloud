from django.shortcuts import render
from .models import Form
from django.views.generic import CreateView
from django.urls import reverse_lazy
import requests
from bs4 import BeautifulSoup
import MeCab
import ipadic
import collections
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64


class Create(CreateView):
    template_name = 'home.html'
    model = Form
    fields = ('url',)
    success_url = reverse_lazy('list')


def listfunc(request):
    for post in Form.objects.all():
        url = post.url
    response = requests.get(url)
    bs = BeautifulSoup(response.content, "html.parser")
    bs = bs.get_text(strip=False)
    CHASEN_ARGS = r' -F "%m\t%f[7]\t%f[6]\t%F-[0,1,2,3]\t%f[4]\t%f[5]\n"'
    CHASEN_ARGS += r' -U "%m\t%m\t%m\t%F-[0,1,2,3]\t\t\n"'
    tagger = MeCab.Tagger(ipadic.MECAB_ARGS + CHASEN_ARGS)
    node = tagger.parseToNode(bs)
    meishi_list = []
    while node:
        if node.feature.split(",")[0] == "名詞":
            meishi_list.append(node.surface)
        node = node.next
    c = collections.Counter(meishi_list)
    c.most_common(10)
    wordcloud = WordCloud(font_path='../fonts/NotoSansCJKjp-Regular.otf',
                          background_color="white",
                          width=600,
                          height=400,
                          min_font_size=15,
                          prefer_horizontal=1)
    wordcloud.generate(" ".join(meishi_list))

    plt.figure(figsize=(12, 8))
    plt.axis("off")
    plt.imshow(wordcloud)

    list = []
    list.append([plt2png(), url])
    return render(request, 'list.html', {'list': list})

# png画像形式に変換する関数


def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    s = buf.getvalue()
    s = base64.b64encode(s)
    s = s.decode('utf-8')
    buf.close()
    return s
