# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import re
from main_gmail import gmail_send_message
from chatwork import chatwork_send_message
import config

driver = webdriver.Chrome()
driver.maximize_window()

# ログイン・パスワード
# username = 'catw_bull'
# password = 'rn4eQhCu'
username = config.TWITTER_ID
password = config.TWITTER_PW

# 各アカウントの結果値
account_datas = {}

# アカウントの数が入る
account_count = 1
# 参照アカウントの現在値
account_target_position = 1

# アカウント参照先のID
account_id = ''

# メール本文
msg_format = u""

# 各ページ
url_page_login          = 'https://twitter.com/'                # ログインページ
url_page_account        = 'https://ads.twitter.com/accounts/'   # アカウント一覧ページ

# ログインページ
path_username_box       = "//*[@id='doc']/div/div[1]/div[1]/div[1]/form/div[1]/input"   # ID入力テキストボックス
path_password_box       = "//*[@id='doc']/div/div[1]/div[1]/div[1]/form/div[2]/input"   # PW入力テキストボックス
path_login_btn          = "//*[@id='doc']/div/div[1]/div[1]/div[1]/form/input[1]"       # ログインボタン

# アカウント情報ページ
path_between_day_btn    = "//*[@id='root']/div/div[1]/div[1]/div[1]/div[2]/div[3]/button"           # 日付指定ボタン
path_between_day_today  = "//*[@id='feather-dropdown-1']/ul/li/div/div[1]/div[1]/div/button"        # 日付指定ボタンから今日のボタン
path_payment_btn        = "//*[@id='root']/div/div[1]/div[4]/div[1]/ul/li[1]/button"                # お支払い方法のタブ
path_payment_text       = "//*[@id='root']/div/div[1]/div[4]/div[1]/ul/li[1]/button/span[2]"        # お支払い方法の文字
path_data_btn           = "//*[@class='src-views-ActionsBar-styles-module--right']/div[1]/button"   # 詳細ソートのデータボタン
path_data_list          = "//*[@id='feather-dropdown-8-menu-item-content-0']/div/div[2]/div/div"    # 詳細ソートの概要項目

# アカウントのお支払いアイテム数
path_account_itemcount  = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[2]/table/tbody/tr"

# レンダリングされるまでの最高待機時間
implicitly_wait_time = 30

# アラートのチェックをする金額
check_maney = 1000000

# Gmail情報
to           = config.GMAIL_TO
subject      = config.GMAIL_SUBJECT

# Chatwork情報
# room_id = config.CHATWORK_ROOMID
room_id = config.CHATWORK_TESTROOMID

# ログイン処理
def login():
  driver.get(url_page_login)
  driver.implicitly_wait(implicitly_wait_time)

  username_box = driver.find_element_by_xpath(path_username_box)
  password_box = driver.find_element_by_xpath(path_password_box)

  username_box.send_keys(username)
  password_box.send_keys(password)

  login_btn = driver.find_element_by_xpath(path_login_btn)
  login_btn.click()


# ログイン処理
def accountCount():
  accounts = driver.find_elements_by_class_name("AccountSelector-accountId")
  return len(accounts)


# アカウント一覧から遷移
def accountListsTarget(num=1):
  global account_count
  global account_target_position
  global account_id
  driver.get(url_page_account)
  driver.implicitly_wait(implicitly_wait_time)

  if account_count <= 1:
    account_count = accountCount()

  url = "//*[@class='AccountSelector-accounts']/li[" + str(num) + "]"
  account_id = driver.find_element_by_xpath("//*[@id='account-selector-form']/ul/li[" + str(num) + "]/div/div[2]/div").text
  account_id = account_id.strip("ID: ")
  accout_list = driver.find_element_by_xpath(url)
  accout_list.click()
  account_target_position += 1


# アカウントページの詳細情報の中にお支払い方法のヘッダーが存在しているか
def isPriceTextExistence():
  is_payment_text = False
  payment_text_pattern = u'支払'
  payment_text = driver.find_element_by_xpath(path_payment_text).text
  result = re.search(payment_text_pattern, payment_text)

  if result:
    is_payment_text = True

  return is_payment_text


# アカウントのお支払い参照
def priceLimitCheck():
  actions = ActionChains(driver)

  # 日指定ボタン押下
  between_day_btn = driver.find_element_by_xpath(path_between_day_btn)
  between_day_btn.click()
  sleep(2)

  # 今日を指定
  between_day_today = driver.find_element_by_xpath(path_between_day_today)
  actions.click_and_hold(between_day_today)
  actions.move_to_element(between_day_today)
  actions.click(between_day_today)
  actions.perform()
  sleep(3)

  # お支払い方法を押下
  payment_btn = driver.find_element_by_xpath(path_payment_btn)
  payment_btn.click()
  sleep(2)

  # ソート用のデータを押下
  data_btn = driver.find_element_by_xpath(path_data_btn)
  data_btn.click()
  sleep(2)

  # データのプルダウンを選択
  actions = ActionChains(driver)
  data_list = driver.find_element_by_xpath(path_data_list)
  actions.click_and_hold(data_list)
  actions.move_to_element(data_list)
  actions.click(data_list)
  actions.perform()
  sleep(3)


# お支払い方法のアイテムの数
def getPriceItemsCount():
  count = driver.find_elements_by_xpath(path_account_itemcount)
  return len(count)


# お支払い方法のステータスを確認して情報取得
def priceStatusCheck(count=1):
  global account_id
  global account_datas

  # アカウント情報ページ（table情報）
  path_price_title        = "//*[@id='root']/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/div/span[1]/span"
  path_price_item_name    = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[2]/table/tbody/tr[" + str(count) + "]/td[1]"
  path_price_status       = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[1]/table/tbody/tr[" + str(count) + "]/td[2]"
  path_price_start_date   = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[1]/table/tbody/tr[" + str(count) + "]/td[3]"
  path_price_end_date     = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[1]/table/tbody/tr[" + str(count) + "]/td[4]"
  path_price_paging       = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[1]/table/tbody/tr[" + str(count) + "]/td[5]"
  path_price_budget       = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[1]/table/tbody/tr[" + str(count) + "]/td[6]"
  path_price_usage_amount = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[1]/table/tbody/tr[" + str(count) + "]/td[7]"
  path_price_limit        = "//*[@id='root']/div/div[1]/span/div/div/div/div/div[1]/table/tbody/tr[" + str(count) + "]/td[8]"

  price_title        = driver.find_element_by_xpath(path_price_title).text
  price_item_name    = driver.find_element_by_xpath(path_price_item_name).text
  price_status       = driver.find_element_by_xpath(path_price_status).text
  price_start_date   = driver.find_element_by_xpath(path_price_start_date).text
  price_end_date     = driver.find_element_by_xpath(path_price_end_date).text
  price_paging       = driver.find_element_by_xpath(path_price_paging).text
  price_budget       = driver.find_element_by_xpath(path_price_budget).text
  price_usage_amount = driver.find_element_by_xpath(path_price_usage_amount).text
  price_limit        = driver.find_element_by_xpath(path_price_limit).text

  data_list = {
    'title' : price_title,
    'item_name' : price_item_name,
    'status' : price_status,
    'start_date' : price_start_date,
    'end_date' : price_end_date,
    'paging' : price_paging,
    'budget' : price_budget,
    'usage_amount' : price_usage_amount,
    'limit' : price_limit,
  }

  account_datas[account_id][count] = data_list

# メール本文用に文言成形
def mailModlMessageFormat(account_datas):
  global msg_format
  global check_maney

  # メール用の本文
  for account_id, lists in account_datas.items():
    is_msg = False
    is_few_balance = False
    msg_subject = u""
    msg_text = u""
    msg_format = u""
    for key, data in lists.items():
      item      = data['item_name']
      status    = data['status']
      start_day = data['start_date'].replace('\n',' ')
      end_day   = data['end_date'].replace('\n',' ')
      paging    = data['paging']
      budget    = data['budget']
      money     = data['usage_amount']
      balance   = data['limit']
      if status == u'実行中':
        msg_text += u'アイテム名：%s\nステータス：%s\n開始：%s\n終了：%s\nページング：%s\n予算：%s\nご利用金額：%s\n予算残高：%s\n\n' % (item, status, start_day, end_day, paging, budget, money, balance)
        is_msg = True
      if balance:
        maney = balance.replace(u'￥', '').replace(u',', '')
        if int(maney) < int(check_maney):
          is_few_balance = True
    if is_msg:
      if is_few_balance:
        msg_subject = u'★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★\n'
      msg_subject += u'【 ' + lists[1]['title'] + u' 】\n'
      msg_format += msg_subject + msg_text + u'\n'
      chatwork_send_message(room_id, msg_format)

# 実行
if __name__ == "__main__":
  login()
  while account_target_position <= account_count:
    accountListsTarget(account_target_position)
    is_payment_existence = isPriceTextExistence()
    if is_payment_existence:
      priceLimitCheck()
      item_count = getPriceItemsCount()
      account_datas[account_id] = {}
      for i in range(1, item_count + 1):
        priceStatusCheck(i)
  mailModlMessageFormat(account_datas)
  # print msg_format
  # msg_format = str(msg_format.encode('utf-8'))
  # gmail_send_message(to, subject, msg_format)

driver.quit()
