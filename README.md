# Twitterスクレイピング仕様書

自身のPCから自動的にChromeブラウザを立ち上げて、Twitterログインをして全アカウントに対してスクレイピングを用いて
データを取得していきchatworkに通知します。

【ディレクトリ構成】  
**twitter**  
  ┣ chatwork.py（ChatWork APIを利用して送信）  
  ┣ credentuals.json（Gmail APIを利用する上での資格情報）  
  ┣ gmail_auth.py（OAuth通信の為、token生成）  
  ┣ main_gmail.py（Gmail APIを利用して送信）  
  ┣ README.md  
  ┣ token.json（Gmail APIのOAuth用に生成されたファイル）  
  ┗ twitter_scraping.py（Twitterスクレイピングのメイン実行ファイル）


### 開発環境
* python 2.7
* webdriverのselenium  
`pip install selenium`  
コマンドがない場合は入れて下さい  
参考：https://qiita.com/suzuki_y/items/3261ffa9b67410803443）


### Gmail API利用
参考：https://thinkami.hatenablog.com/entry/2016/06/10/065731#Google-Developers-Console-%E3%81%A7-Gmail-API-%E3%82%92%E6%9C%89%E5%8A%B9%E5%8C%96


### Google Developers Console で Gmail API を有効化
1. Gmail APIを有効にする
2. OverviewでPythonを選択  
https://developers.google.com/gmail/api/quickstart/python  
3. ENABLE THE GMAIL APIを押下
4. Client IDとClient Secretが生成されるのでDOWNLOAD CLIENT CONFIGURATIONを押下してファイル取得
5. twitter_scraping.pyのディレクトリにcredentials.jsonを配置
6. 下記のコマンドを実行してパッケージ取得  
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`  
`pip install --upgrade oauth2client`  
`pip install requests`


### 処理の流れ
  1. ログイン画面でID・PWを入れてログインボタンを押下
  2. アカウント一覧画面に遷移して全アカウントの数を取得
  3. アカウント一覧画面にあるアカウントを順番に押下
  4. アカウント詳細画面にある最初のタブの文言が「支払」と含まれているか確認
      * 含まれていれば 5へ
      * 含まれていなければ 3へ
  5. アカウント詳細画面にある日指定ボタン押下して今日を押下指定
  6. アカウント詳細画面にあるお支払い方法タブを押下
  7. アカウント詳細画面にあるソート用のデータを押下して概要を押下指定
  8. お支払い方法のアイテム数を取得
  9. お支払い方法のアイテムごとにある行のデータを取得する
      * お支払い方法名
      * お支払い方法のステータス
      * お支払い方法の開始
      * お支払い方法の終了
      * お支払い方法の全期間のページング
      * お支払い方法の全期間の予算
      * お支払い方法の全期間のご利用金額
      * お支払い方法の全期間の予算残高
  10. 3から9を繰り返し全アカウントのデータを舐めまわして、全カウントの9の情報取得
  11. 通知する為の文面を生成する
      * お支払い方法のステータスが実行中のみ文面を生成（左記の条件により停止、終了はない）
  12. APIを利用して11で生成した文面を通知する


### プログラム実行コマンド
* 実行コマンド  
`python twitter_scraping.py`


### エラーになると考えられる事項を下記に記載
* TwitterがアップデートしてBot対策を入れられた
  * ログインの時に画像選択などが必要になった
  * 決まった秒数でもアクセスがあったのでBotと認知された
* Twitterの画面レイアウトが変更された場合


### Twitterの画面レイアウトが変更して配置が変わった場合
* プログラムで指定されているpathを変更する必要があります。
* 下記で変更する為の方法を記載します。
    1. Chromeのデベロッパーツールを開きます。
    2. 左上にある矢印を押下
    3. 対処にしたいレイアウトの箇所をクリック
    4. デベロッパーツールのElementsのHTMLの行が指定されるので、その行に対して右クリックしてCopy矢印Copy XPathを選択
    5. 指定のXpathを指定いているプログラムの変数に代入


### Gmail APIを利用してメールで結果を送信
**※ 希望はchatworkだがAPI申請がもたついているので一旦Gmailで作成**  
* 下記の2行のコメントアウトをとる  
`msg_format = str(msg_format.encode('utf-8'))`  
`gmail_send_message(to, subject, msg_format)`


### Chatwork APIを利用してchatで結果を報告
* 下記の関数を利用  
`chatwork_send_message(room_id, msg_format)`
