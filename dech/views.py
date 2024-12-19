# myapp/views.py
import re
from django.shortcuts import render
import pandas as pd
import os
from django.conf import settings
import json
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
    file_path = os.path.join(settings.BASE_DIR, 'dech', 'data', '金陵历朝诗歌.csv')
    df = pd.read_csv(file_path)
    dynasty_texts = defaultdict(str)
    for index, row in df.iterrows():
        dynasty = row['dynasty']
        text = row['content']
        words = jieba.cut(text)
        dynasty_texts[dynasty] += ' '.join(words) + " "
    wordcloud_data = {}
    for dynasty, text in dynasty_texts.items():
        wordcloud = WordCloud(width=600, height=600, background_color="white").generate(text)
        wordcloud_words = wordcloud.words_
        wordcloud_data[dynasty] = wordcloud_words
    return render(request, 'dech/name_data.html', {'word_freq': json.dumps(wordcloud_data)})
