import requests

from pathlib import Path
from loguru import logger
from pprint import pprint
from datetime import datetime


class Pyrus:
    def __init__(self, url: Path):
        with open(url, "r") as fp:
            creds = fp.readlines()
        self.token = Pyrus.__auth(creds[0].strip(), creds[1])
        self.default_headers = {"Content-Type": "application/json",
                                "Authorization": self.token}

    @staticmethod
    def __auth(login: str, security_key: str):
        response = requests.post('https://api.pyrus.com/v4/auth',
                                 headers={'Content-Type': 'application/json'},
                                 json={'login': login,
                                       'security_key': security_key})

        if response.ok:
            token = f'Bearer {response.json()["access_token"]}'
            return token

        else:
            logger.debug(f"pyrus doesn't auth status code = {response.text}")

    def get_register(self, form_id: int):
        response = requests.post(f"https://api.pyrus.com/v4/forms/{form_id}/register",
                                 headers=self.default_headers,
                                 json={"include_archived": "y",
                                       "field_ids": "3"},
                                 timeout=1)
        if response.ok:
            logger.info(f"register {form_id} got")
            return response
        else:
            logger.debug("get_register didn't_work")

    def get_task(self, ticket_id: int):
        response = requests.get(f"https://api.pyrus.com/v4/tasks/{ticket_id}",
                                headers=self.default_headers)
        return response

    def get_file(self, file_id: int):
        response = requests.get(f"https://api.pyrus.com/v4/files/download/{file_id}",
                                headers=self.default_headers)
        if response.ok:
            return response.__dict__
        else:
            logger.error("get_file don't work")
            pprint(response.__dict__)

    def get_id_and_name(self, register_id):
        ticket_list: list[dict] = list()
        register = self.get_register(register_id).json()['tasks']
        id_value = list()
        count = 1
        for field in register:
            if 'value' not in field['fields'][0]:
                continue
            for value in field['fields'][0]['value']:
                value_dict = dict()
                value_dict['id'] = value['id']
                value_dict['name'] = f"{count}{value['name']}"
                count += 1
                ticket_list.append(value_dict)
        logger.info("get id and name list")
        return ticket_list

    def save_files(self, register_id):
        id_and_name_list = self.get_id_and_name(register_id)
        timestamp = datetime.now().strftime('%d.%m.%Y_%H.%M')
        DIR_NAME = "photos_" + timestamp
        dir = Path.cwd() / DIR_NAME

        if not dir.exists():
            dir.mkdir()
            logger.info("make dir")
        for value in id_and_name_list:
            photo = self.get_file(value['id'])
            file_path = dir / value['name']
            with open(file_path, "wb") as fp:
                fp.write(photo['_content'])
                logger.info(f"save photo {value['name']}")

        my_file = open("last_upload.txt", "w+")
        my_file.write(f"{timestamp}")
        my_file.close()
        logger.info("make last upload info")










