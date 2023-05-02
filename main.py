from Pyrus_client import Pyrus
from datetime import datetime
from pathlib import Path
from loguru import logger


def main():
    pyrus_client = Pyrus(r"C:\Users\tuzle\Desktop\creds.txt")
    tickets = pyrus_client.collect_tickets(1203495)

    id_and_name_list: list[dict] = list()
    for ticket in tickets:
        if 'value' not in ticket['task']['fields'][5]:
            continue
        for value in ticket['task']['fields'][5]['value']:
            my_dict = dict()
            my_dict['name'] = value['name']
            my_dict['id'] = value['id']
            id_and_name_list.append(my_dict)
        logger.info(f"Get value from task {ticket['task']['id']}")

    timestamp = datetime.now().strftime('%d.%m.%Y_%H.%M')
    DIR_NAME = "photos_" + timestamp

    dir = Path.cwd() / DIR_NAME

    if not dir.exists():
        dir.mkdir()
    for value in id_and_name_list:
        photo = pyrus_client.get_file(value['id'])
        file_path = dir / value['name']
        with open(file_path, "wb") as fp:
            fp.write(photo['_content'])
    logger.info("make dir and save fields")

    my_file = open("last_upload.txt", "w+")
    my_file.write(f"{timestamp}")
    my_file.close()


if __name__ == "__main__":
    main()