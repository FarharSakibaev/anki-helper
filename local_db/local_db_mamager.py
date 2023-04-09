import json
import re
import time

import requests


class LocalDbManager:
    local_address = 'http://localhost:8765'

    def __init__(self) -> None:
        self._set_tag_list()

    def _set_tag_list(self) -> None:
        url = 'http://localhost:8765'
        headers = {'Content-Type': 'application/json'}
        payload = {
            "action": "getTags",
            "version": 6
        }

        response = requests.get(url, headers=headers, data=json.dumps(payload)).json()

        self._tag_list = response['result']

    def get_cart_list(self) -> list:
        russian_pattern = re.compile("[а-яА-ЯёЁ]+")

        for tag in self._tag_list:

            headers = {'Content-Type': 'application/json'}
            payload = {
                "action": "findCards",
                "version": 6,
                "params": {
                    "query": f"tag:{tag}"
                }
            }
            response = requests.get(self.local_address, headers=headers, data=json.dumps(payload)).json()
            card_list = response['result']

            payload = {
                "action": "cardsInfo",
                "version": 6,
                "params": {
                    "cards": card_list
                }
            }
            response = requests.post(self.local_address, headers=headers, data=json.dumps(payload)).json()

            cards = response['result']

            for card in cards:
                fields = card['fields']
                front_value: str = fields['Front']['value']
                back_value = fields['Back']['value']

                for value in back_value.split('.'):
                    matches: list[str] = russian_pattern.findall(value)

                    if matches:
                        for match in matches:
                            payload = {
                                "action": "addNote",
                                "version": 6,
                                "params": {
                                    "note": {
                                        "deckName": card['deckName'],
                                        "modelName": card['modelName'],
                                        "fields": {
                                            "Front": match.capitalize(),
                                            "Back": front_value.capitalize()
                                        },
                                        "tags": [
                                            tag
                                        ]
                                    }
                                }
                            }

                            response = requests.post(self.local_address, headers=headers, data=json.dumps(payload)).json()
                            if response['error']:
                                print(response['error'])
                            time.sleep(0.1)
                        break


if __name__ == '__main__':
    manager = LocalDbManager()
    test = manager.get_cart_list()
    print(test)
