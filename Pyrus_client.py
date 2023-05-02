import requests

from loguru import logger


class Pyrus:
    def __init__(self, url: str):
        with open(url, "r") as fp:
            creds = fp.readlines()
        self.token =Pyrus.__auth(creds[0].strip(), creds[1])
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
                                 headers=self.default_headers)
        if response.ok:
            logger.info(f"register {form_id} got")
            return response
        else:
            logger.debug("get_register didn't_work")

    def get_task(self, ticket_id: int):
        response = requests.get(f"https://api.pyrus.com/v4/tasks/{ticket_id}",
                                headers=self.default_headers)
        return response

    def collect_tickets(self, register_id: int):
        ticket_list: list[dict] = list()

        register = self.get_register(register_id).json()
        tickets_ids = (x['id'] for x in register['tasks'])

        for ticket in tickets_ids:
            ticket_list.append(self.get_task(ticket).json())
            logger.info(f"{ticket} got")

        logger.info(f"collect tickets performed")

        return ticket_list

    def get_file(self, file_id: int):
        response = requests.get(f"https://api.pyrus.com/v4/files/download/{file_id}",
                                headers=self.default_headers)
        if response.ok:
            return response.__dict__
        else:
            logger.debug("get_file don't work")






