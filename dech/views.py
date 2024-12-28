# myapp/views.py
import re
from django.shortcuts import render
import pandas as pd
import os
from django.conf import settings
import json
from collections import Counter
from .models import Location
from wordcloud import WordCloud
from collections import defaultdict, Counter
import jieba


def map_view(request):
    # 读取 CSV 文件中的数据
    file_path = os.path.join(settings.BASE_DIR, 'dech', 'data', '地点人物.csv')
    df = pd.read_csv(file_path, encoding='utf-8-sig')  # 替换为实际路径
    df['经度'] = pd.to_numeric(df['经度'], errors='coerce')
    # 从 DataFrame 中提取需要的列，处理后形成一个字典列表
    locations = df[['地名', '地理位置', '经度', '纬度', '相关人物']].dropna(subset=['经度', '纬度']).to_dict(
        orient='records')
    # 将地点数据传递给模板
    return render(request, 'map_app/map.html', {'locations': json.dumps(locations)})


def name_data(request):
    # 获取 CSV 文件路径
    file_path = os.path.join(settings.BASE_DIR, 'dech', 'data', '金陵历朝诗歌.csv')
    df = pd.read_csv(file_path)
    dynasty_texts = defaultdict(str)  # 存储每个朝代的所有诗句
    poet_count = Counter()  # 统计每个诗人的诗句数量
    dynasty_count = Counter()  # 统计每个朝代的诗句数量

    # 遍历 CSV 数据
    for index, row in df.iterrows():
        dynasty = row['dynasty']
        poet = row['author']
        text = row['content']
        words = jieba.cut(text)
        dynasty_texts[dynasty] += ' '.join(words) + " "
        poet_count[poet] += 1
        dynasty_count[dynasty] += 1
    wordcloud_data = {}
    for dynasty, text in dynasty_texts.items():
        wordcloud = WordCloud(width=600, height=600, background_color="white").generate(text)
        wordcloud_words = wordcloud.words_
        wordcloud_data[dynasty] = wordcloud_words
    top_poets = poet_count.most_common(10)
    return render(request, 'dech/name_data.html', {
        'word_freq': json.dumps(wordcloud_data),
        'top_poets': top_poets,
        'dynasty_count': json.dumps(dynasty_count)
    })


def index_view(request):
    return render(request, 'index.html')


def barChart_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'dech', 'data', '金陵历朝诗歌.csv')
    df = pd.read_csv(file_path)
    poet_count = Counter()
    for index, row in df.iterrows():
        dynasty = row['dynasty']
        poet = row['author']
        poet_count[poet] += 1
    top_poets = [{"name": poet, "quantity": count} for poet, count in poet_count.most_common(10)]
    return render(request, 'barchart.html', {
        'top_poets': top_poets,
    })


def chaodai_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'dech', 'data', '金陵历朝诗歌.csv')
    df = pd.read_csv(file_path)
    dynasty_count = Counter()
    for index, row in df.iterrows():
        dynasty = row['dynasty']
        dynasty_count[dynasty] += 1
    dynasties = [{"name": dynasty, "quantity": count} for dynasty, count in dynasty_count.items()]
    return render(request, 'chaodai.html', {
        'dynasties': dynasties,
    })
