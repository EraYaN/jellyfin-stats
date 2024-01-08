import logging
import requests
from tqdm import tqdm
from .auth import JellyfinAuth
from ..common import single_item_kinds, DEBUG

if DEBUG:
    from pprint import pprint

class JellyfinRawData():
    def __init__(self, api_key,hostname="http://localhost:8096"):
        self.hostname = hostname
        self.auth = JellyfinAuth(api_key)
        users = requests.get(f'{self.hostname}/Users', auth=self.auth)

        if not users:
            if users.status_code == requests.codes.unauthorized:
                logging.error("Could not get users, please verify API key is correct.")
                raise ValueError("API key is not accepted by server.")
            raise ValueError("Could not reach server.")

        self.user_id = None

        for user in users.json():
            if user['Policy']['IsAdministrator']:
                self.user_id = user['Id']
                logging.info(f"Using administrator account {user['Name']} with id {user['Id']}")
                break

        self.all_items = {}

    def gather(self):
        for itemtype in single_item_kinds:
            start_index = 0
            limit = 1000
            items = []
            
            response = requests.get(f'{self.hostname}/Users/{self.user_id}/Items?IncludeItemTypes={itemtype}&Recursive=True&startIndex={start_index}&limit=0', auth=self.auth)
            if response:
                payload = response.json()
                print("Items payload:\n", payload)
                total = payload['TotalRecordCount']
                if total > 0:
                    pbar = tqdm(total=total, desc=f"Loading {itemtype}", unit='items', unit_scale=True, leave=True, dynamic_ncols=True)
                    pbar.update(0)
                    while total > start_index:
                        pbar.write(f"Getting {itemtype} from {start_index} to {start_index+limit}")
                        response = requests.get(f'{self.hostname}/Users/{self.user_id}/Items?IncludeItemTypes={itemtype}&Recursive=True&Fields=MediaStreams,Path&startIndex={start_index}&limit={limit}&enableTotalRecordCount=false', auth=self.auth)
                        if response:
                            payload = response.json()
                            items.extend(payload['Items'])
                            start_index += len(payload['Items'])
                            pbar.update(len(payload['Items']))
                        else:
                            break

                    pbar.close()
            
            if len(items) > 0:
                self.all_items[itemtype] = items
                if DEBUG:
                    # Print an example
                    pprint(items[0])
