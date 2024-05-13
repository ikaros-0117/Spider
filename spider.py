# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# File Name:        spider.py
# Author:           ikaros
# Description:      Main Function:    爬取大众点评商家评论
# ------------------------------------------------------------------


import requests
from bs4 import BeautifulSoup
import pandas as pd

def process(review: str) -> list:
    """
    处理评论文本之中的空格、换行符和制表符等杂乱信息
    params: 获取的原始评论文本
    return: 包含多段文本的列表
    """
    # 去除首尾多余空格
    cleaned_review = review.strip()

    # 去除中间的空白行
    cleaned_review = '\n'.join(line.strip() for line in cleaned_review.splitlines() if line.strip())

    # 去除字符串中的制表符
    cleaned_review = cleaned_review.replace('\t', '')

    # 按照每行进行分割
    res = cleaned_review.split('\n')
    
    # 去除 “收起评价” 这一项
    if res[-1] == "收起评价":
        res.pop()
    
    return res

# 请求头
# Cookie要设置成自己的Cookie
# Accept建议也设置成自己的Accept
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", 
    "Cookie": "fspop=test; _lxsdk_cuid=18f6841e7f5c8-01b06ff06e35ba-4c657b58-144000-18f6841e7f5c8; _lxsdk=18f6841e7f5c8-01b06ff06e35ba-4c657b58-144000-18f6841e7f5c8; _hc.v=81a47d99-dd65-7cb4-6145-fd28e7301ded.1715441101; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1715441102; WEBDFPID=z70w13vzx7415y0414367z9z72uy8y6981u31576x7497958zw473934-2030801120473-1715441120473SUOGWSKfd79fef3d01d5e9aadc18ccd4d0c95074166; dper=02029623d2a8ccb5a8b328b6274deffe93dfd379a23ce3d90b8385bca807276a960428d98de3b07d01e37ace3c28c3c3f6b5d55581d6ace0f1fc00000000fc1f0000ea7537a6261b00f02121bfcd56c3dc5be07c277839b416a2351cd67d0f71c2fbf2762f70e128c86524b231172abd3113; qruuid=5b950ac5-0233-45e1-8349-272090cc171a; ll=7fd06e815b796be3df069dec7836c3df; s_ViewType=10; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; cy=344; cye=changsha; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1715449705; _lxsdk_s=18f68aecda0-82c-568-792%7C%7C810",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

# 基本url
# 根据想要爬取的商家，大众点评上打开其评论页面首页获取基本url
# 这里以 坛宗剁椒鱼头(中心印象城店) 为例
base_url = "https://www.dianping.com/shop/k1tagpzVilDNuSsp/review_all"
k = 1

# 收集所有评论段
all_reviews = []

# 爬取前五页的评论
while k <= 5:
    # 通过 k 实现评论页面下一页url的获取
    path = "/p" + str(k)
    url = base_url + path
    print(url)

    # 获取网页html
    con = requests.get(url, headers=headers)
    html_doc = con.text
    # print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')

    # 获取当前页面所有评论信息
    # 通过分析html代码可知，评论文字都包含在具有 class = "review-words" 的 div 标签下
    reviews = soup.find_all('div', class_="review-words")


    for i in range(len(reviews)):
        review = reviews[i].text.strip()
        s = process(review)
        # for x in s:
        #     if x == "收起评价":
        #         break
        #     print(x)
        # print('\n')
        all_reviews.extend(s)
    
    # 获取下一页
    k += 1

# 将评论数据转换为DataFrame
df = pd.DataFrame(all_reviews, columns=['Review'])

# 将DataFrame保存到CSV文件
df.to_csv('./reviews.csv', index=False, encoding='utf-8-sig')