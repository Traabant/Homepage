import requests
import json
import datetime

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
        :parm" new_id - int, id to chek
        Gets list with users from DB
        each entry is in tuple (Id, git_id, node_id, login)
        return True if users is not DB 
        """
        users_from_db = self.db.get_data_github_authors()

        isIn = list(filter(lambda id: id['git_id'] == new_id, users_from_db))  
        if len(isIn) != 0 :
            return False
        return True


    def get_repos(self, username):
        """
        :parm: username - string, usersname of user to get repos
        downloads repos info from github api, if new, repos are saved in DB 
        """
        today = datetime.datetime.now()
        url = 'https://api.github.com/users/' + username + '/repos'
        resp = requests.get(url)        
        if resp.status_code == 200: 
            repos = json.loads(resp.text)
            for repo in repos:
                if self.is_new_repo(repo['id']):
                    self.db.dump_data_github_repos(today, repo['id'], repo['node_id'], \
                        repo['owner']['id'], repo['name'], repo['full_name'], \
                            repo['html_url'], repo['description'])
                    print('saving new repo to db')


    def is_new_repo(self, repo_id):
        """
        :parm" repo_id - int, id to chek
        Gets list with repos from DB
        each entry is in dict
        return True if users is not DB 
        """
        repos = self.db.get_data_github_repos()
        isIn= list(filter(lambda id: id['git_id'] == repo_id, repos))
        if len(isIn) != 0 :
            return False        
        return True
    
    def repos_form_db(self):
        
        repos = self.db.get_data_github_repos()
        print(repos)
    
if __name__ == "__main__":
    pass
    # GitHub().get_repos('traabant')
    # print(GitHub().is_new_user(16059893))
    # GitHub().repos_form_db()
    # GitHub().is_new_repo(176527851)
    