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
        
        ids = {}
        ref = {}
        for itemtype in single_item_kinds:
            start_index = 0
            limit = 1000
            items = []
            
            response = requests.get(f'{self.hostname}/Users/{self.user_id}/Items?IncludeItemTypes={itemtype}&Recursive=True&startIndex={start_index}&limit=0', auth=self.auth)
            if response:
                payload = response.json()
                logging.debug("Items payload:\n%s", payload)
                total = payload['TotalRecordCount']
                if total > 0:
                    pbar = tqdm(total=total, desc=f"Loading {itemtype}", unit='items', unit_scale=True, leave=True, dynamic_ncols=True)
                    pbar.update(0)
                    while total > start_index:
                        #pbar.write(f"Getting {itemtype} from {start_index} to {start_index+limit}")
                        response = requests.get(f'{self.hostname}/Users/{self.user_id}/Items?IncludeItemTypes={itemtype}&Recursive=True&Fields=MediaStreams,Path&startIndex={start_index}&limit={limit}&enableTotalRecordCount=false', auth=self.auth)
                        if response:
                            payload = response.json()
                            
                            items.extend(payload['Items'])
                            start_index += len(payload['Items'])
                            pbar.update(len(payload['Items']))
                        else:
                            break

                    pbar.close()
            for item in items:
                itemid = item['Id']
                prev = ids.get(itemid, 0)
                
                if itemid not in ref:
                    ref[itemid] = []
                item['_itemtype'] = itemtype
                ref[itemid].append(item)
                ids[itemid] = prev + 1
            
            
            
            if len(items) > 0:
                self.all_items[itemtype] = items
                if DEBUG:
                    # Print an example
                    pprint(items[0])
        logging.info("Items: %d Uniques: %d",len(items),len(ids))
        for itemid in ids:
            if ids[itemid] > 1:
                logging.info(f"Duplicate id %s found %d times",itemid, ids[itemid])
                for refitem in ref[itemid]:
                    logging.info("ItemType: %s, MediaType: %s, Path: %s", refitem['_itemtype'],refitem['MediaType'],refitem['Path'])
                break
