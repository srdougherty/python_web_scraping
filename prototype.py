import requests
from bs4 import BeautifulSoup
import shutil
import os


# ---------------------------------------------------------
#  映画.comから今週公開される映画のポスターをスクレイピングする
# ---------------------------------------------------------
def get_this_weeks_movies():
    # ウェブページを取得する
    url = "https://eiga.com/movie/"
    get_page_respone = requests.get(url)
    if get_page_respone.status_code != 200:
        print("ページ取得が失敗しました")
        return

    # 取得したウェブページを解析する
    soup = BeautifulSoup(get_page_respone.content, "html.parser")

    # 特定のデータを抽出する
    # 第１の .slide-menu
    first_list = soup.find(class_="slide-menu")
    first_movie_date = soup.find(class_="published").text
    os.mkdir(first_movie_date)

    # .slide-menu の中の各img要素をループする
    for img in first_list.find_all('img'):
        # 画像リソースへのパス
        img_src = img.get('src')
        # 映画のタイトルがimgのaltテキストに設定される
        movie_title = img.get('alt')

        # 画像ファイルを取得する
        img_response = requests.get(img_src, stream=True)
        if img_response.status_code != 200:
            print(movie_title + "の画像取得が失敗しました")
            continue

        # 画像ファイルを保存する
        file_extension = get_img_file_extenstion(img_src)
        filename = os.path.join(first_movie_date, movie_title + file_extension)
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(img_response.raw, out_file)

        # レスポンスをクリーンアップする
        del img_response


def get_img_file_extenstion(filename):
    # ファイルのパスと拡張子を分割して後者を取得する
    file_extension = os.path.splitext(filename)[1]
    # クエリーテキストが付いていれば削る
    file_extension = file_extension.split("?")[0]
    return file_extension


get_this_weeks_movies()
