import requests
import json

from DbOperations import DbOperations
from credentials import Credentials

class GitHub():
    def __init__(self):
        self.creds = Credentials()
        self.db = DbOperations(self.creds.db_file_name)

    def get_user_info(self, username):
        """
        :parm: username - string, usersname of user to get data
        downloads users info from github api, if new, user is saved in DB 
        """
        url = 'https://api.github.com/users/' + username
        resp = requests.get(url)
        # creds = Credentials()
        if resp.status_code == 200:            
            user_info = json.loads(resp.text)
            print(user_info)
            if self.is_new_user(user_info['id']):
                print(f'saving new user to DB')                
                self.db.dump_data_github_authors(user_info['id'], user_info['node_id'], user_info['login'])

    def is_new_user(self, new_id):
        """
        :parm" new_it - int, id to chek
        Gets list with users from DB
        each entry is in tuple (Id, git_id, node_id, login)
        return True if users is not DB 
        """
        users_from_db = self.db.get_data_github_authors()
             
        isIn = list(filter(lambda x:new_id in x, users_from_db))  
        if len(isIn) != 0 :
            print('is not')
            return False
        
        return True

    
if __name__ == "__main__":
    GitHub().get_user_info('traabant')
    # GitHub().is_new_user(16059893)
    