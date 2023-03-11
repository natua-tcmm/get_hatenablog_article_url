#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
あるはてなブログの全記事のURLと記事タイトルを取得しcsvに出力するプログラム
"""

__author__ = 'natua_tcmm'
__version__ = '1.0.0'
__date__ = '2023/03/07'

# ---------------------------

import sys
import csv
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# ---------------------------

def main():
	"""
	メインの関数
	あるはてなブログの全記事のURLと記事タイトルを取得しcsvに出力する
	"""

	# 取得するはてなブログを選ぶ
	base_url = get_base_url_by_stdin()

	print(f"{base_url}の全記事タイトル・URLを取得します。")

	# 記事のリストを取得
	article_list = get_all_article_url(base_url)

	# csvに出力
	with open("articles.csv","w",newline='',encoding="utf-8") as a_file:
		writer = csv.writer(a_file)
		writer.writerows(article_list)

	# 正常終了する。
	return 0

# ---------------------------

def get_base_url_by_stdin():
	"""
	取得するブログのベースURLを取得する関数
	"""

	default_url="https://keionkakimasen.hatenadiary.com/archive"
	input_description_str = \
		"取得したいブログの任意の記事のURLを入力してね。\n" + \
		"何も入力しなかったら「京音メンバーの日記(https://keionkakimasen.hatenadiary.com/)」の記事を取得するよ。\n" + \
		"はてなブログ以外だとバグるから入力しないでね\n> "

	# ユーザに入力してもらう
	input_url = input(input_description_str)
	if len(input_url)==0:
		input_url = default_url

	return extracting_up_to_domain_by_url(input_url)

def extracting_up_to_domain_by_url(input_url):
	"""
	入力したURLの先頭からドメインまでを抜き出す関数
	"""

	uri = urlparse(input_url)
	url = f'{uri.scheme}://{uri.netloc}/'
	return url

def add_article_url_by_url_to_list(url,article_list):
	"""
	入力したURLのページ内にある記事のURLとタイトルをリストに追加する
	"""

	html = requests.get(url,timeout=5)
	soup = BeautifulSoup(html.text,features="html.parser")
	alinks = soup.select('a')

	# 記事のURLのみ抽出(関係ないものをよける)
	url_list = [ a_link for a_link in alinks if ( (a_link.get("class") is not None) and ('entry-title-link' in a_link.get("class")) ) ]

	# 必要な情報をリストに追加
	for a_url in url_list:
		article_list.append([a_url.getText(),a_url.get('href')])

	return len(url_list)

def get_all_article_url(base_url):
	"""
	はてなブログのブログトップURLから、そのブログの全記事のURLとタイトルをリストにして返す関数
	"""

	article_list = []

	# 1ページ目
	adding_url_count = add_article_url_by_url_to_list(f'{base_url}archive',article_list)

	# 2ページ目以降
	page_count = 2
	while adding_url_count!=0:
		adding_url_count = add_article_url_by_url_to_list(f'{base_url}archive?page={page_count}',article_list)
		page_count += 1
		# print(page_count,adding_url_count)

	return article_list

# ---------------------------

if __name__ == '__main__':
	# main()を呼び出して結果を得て、Pythonシステムに終わりを告げる。
	sys.exit(main())
