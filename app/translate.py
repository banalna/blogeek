# -*- coding: utf-8 -*-

import json
import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')

    url = "https://microsoft-translator-text.p.rapidapi.com/translate"

    querystring = {"profanityAction": "NoAction",
                   "textType": "plain", "api-version": "3.0",
                   "from": source_language,
                   "to": dest_language
                   }
    headers = {
        'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
        'x-rapidapi-key': current_app.config['MS_TRANSLATOR_KEY'],
        'content-type': "application/json",
        'accept': "application/json"
    }
    payload = json.dumps([{"Text":text}])

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    if response.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(response.content.decode('utf-8-sig'))[0]['translations'][0]['text']
