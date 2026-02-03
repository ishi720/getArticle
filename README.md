# getArticle

特定ユーザーのQiita、Zenn、noteの記事を取得するツール

## 機能

- Qiita、Zenn、Noteの記事を一括取得
- 記事のタイトル、URL、投稿日時、タグ、いいね数を取得
- CSV または JSON 形式で出力
- 投稿日時の降順でソート

## 実行手順

1. `config.json` に各サービスのユーザー名と出力形式を設定

    ```json
    {
        "zenn_username": "zenn_username",
        "qiita_username": "qiita_username",
        "note_username": "note_username",
        "output_format": "json"
    }
    ```

    - `output_format`: `"json"` または `"csv"` を指定

2. 下記コマンドを実行

    ```bash
    python get_article.py
    ```

3. `combined_articles.json` または `combined_articles.csv` が出力される

## 出力項目

| 項目 | 説明 |
|------|------|
| published_at | 投稿日時 |
| url | 記事URL |
| title | 記事タイトル |
| tags | タグ（カンマ区切り） |
| source | 取得元（Qiita/Zenn/note） |
| likes | いいね数 |

## 必要なライブラリ

```bash
pip install requests
```
