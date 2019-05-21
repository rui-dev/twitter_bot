# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
import requests
import pprint
import config

APIKEY = config.CHATWORK_APIKEY
ENDPOINT = 'https://api.chatwork.com/v2'

# target_id = '[toall]\n'
target_id = ''

def chatwork_send_message(room_id=config.CHATWORK_TESTROOMID, msg=""):
  global target_id
  post_message_url = '{}/rooms/{}/messages'.format(ENDPOINT, room_id)

  headers = { 'X-ChatWorkToken': APIKEY }
  params = { 'body': target_id + msg }

  resp = requests.post(post_message_url, headers=headers, params=params)

  pprint.pprint(resp.content)
