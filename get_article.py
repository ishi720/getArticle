import requests
import csv
import json
from datetime import datetime

def fetch_zenn_articles(username):
    """
    指定されたZennユーザーの公開記事を取得

    Args:
        username (str): Zennのユーザー名

    Returns:
        list: ユーザーが公開した記事の情報が含まれる辞書のリスト
              取得できなかった場合は空のリストを返す
    """
    if not username:
        print("Zenn username is empty. Skipping fetch.")
        return []

    url = f"https://zenn.dev/api/articles?username={username}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch Zenn articles: {response.status_code}")
        return []

    # レスポンスJSONをパースし、記事データを抽出
    data = response.json()
    articles = data.get("articles", [])
    
    return articles

def fetch_qiita_articles(username):
    """
    指定されたQiitaユーザーの公開記事を取得

    Args:
        username (str): Qiitaのユーザー名

    Returns:
        list: ユーザーが公開した記事の情報が含まれる辞書のリスト
              取得できなかった場合は空のリストを返す
    """
    if not username:
        print("Qiita username is empty. Skipping fetch.")
        return []

    url = f"https://qiita.com/api/v2/items?page=1&per_page=100&query=user:{username}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch Qiita articles: {response.status_code}")
        return []

    # レスポンスJSONをパースし、記事データを抽出
    articles = response.json()
    
    return articles

def save_combined_articles_to_csv(zenn_articles, qiita_articles):
    """
    ZennとQiitaの記事データを結合する

    Args:
        zenn_articles (list): Zennの記事情報リスト
        qiita_articles (list): Qiitaの記事情報リスト
    Returns:
        list of dict: 結合された記事データのリスト
    """
    all_articles = []

    # Zennの記事を処理
    for article in zenn_articles:
        all_articles.append({
            "published_at": article["published_at"],
            "url": f"https://zenn.dev{article['path']}",
            "title": article["title"],
            "tags": "",
            "source": "Zenn"
        })
    
    # Qiitaの記事を処理
    for article in qiita_articles:
        tags = ', '.join([tag["name"] for tag in article.get("tags", [])])  # タグをカンマ区切りで取得
        all_articles.append({
            "published_at": article["created_at"],
            "url": article["url"],
            "title": article["title"],
            "tags": tags,
            "source": "Qiita"
        })

    # 作成日時で降順にソート
    all_articles.sort(key=lambda x: datetime.fromisoformat(x["published_at"]), reverse=True)

    return all_articles

def save_to_csv(data, filename="combined_articles.csv"):
    """
    データをCSVファイルに保存

    Args:
        data (list of dict): 保存するデータ
        filename (str): 保存するCSVファイル名
        fieldnames (list of str): CSVファイルのヘッダとして使用するフィールド名
    """

    # CSVに保存
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["published_at", "url", "title", "tags", "source"])
        writer.writeheader()

        for article in data:
            writer.writerow(article)

    print(f"Combined articles have been saved to {filename}")

def save_to_json(data, filename="combined_articles.json"):
    """
    データをJSONファイルに保存

    Args:
        data (list of dict): 保存するデータ
        filename (str): 保存するJSONファイル名
    """
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Combined articles have been saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving JSON: {e}")

def load_config(filename="config.json"):
    """
    設定ファイルから設定情報を読み込む関数。

    Args:
        filename (str): 設定ファイル名。デフォルトは "config.json"。

    Returns:
        dict: 設定情報を格納した辞書。
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return None

# 設定ファイルから情報を読み込む
config = load_config()

if config:
    # ユーザー名を指定して記事を取得
    zenn_username = config["zenn_username"]
    qiita_username = config["qiita_username"]

    # Zennの記事を取得
    zenn_articles = fetch_zenn_articles(zenn_username)

    # Qiitaの記事を取得
    qiita_articles = fetch_qiita_articles(qiita_username)

    # 記事データが存在すればCSVに保存
    if zenn_articles or qiita_articles:
        all_articles = save_combined_articles_to_csv(zenn_articles, qiita_articles)
        if config["output_format"] == "json":
            save_to_json(all_articles)
        elif config["output_format"] == "csv":
            save_to_csv(all_articles)
        else:
            print("No output method specified.")
    else:
        print("No articles found.")
else:
    print("Configuration file could not be loaded.")