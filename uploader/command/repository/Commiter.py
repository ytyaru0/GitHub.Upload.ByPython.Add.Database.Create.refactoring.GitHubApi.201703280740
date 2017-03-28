#!python3
#encoding:utf-8
import subprocess
import shlex
import time
import requests
import json
#import web.http.Response

class Commiter:
    def __init__(self, data, client):
        self.data = data
        self.client = client
#        self.response = web.http.Response.Response()

    def ShowCommitFiles(self):
        subprocess.call(shlex.split("git add -n ."))

    def AddCommitPush(self, commit_message):
        subprocess.call(shlex.split("git add ."))
        subprocess.call(shlex.split("git commit -m '{0}'".format(commit_message)))
        subprocess.call(shlex.split("git push origin master"))
        time.sleep(3)
        self.__InsertLanguages(self.client.repo.list_languages())
#        self.__InsertLanguages(self.client.repo.list_languages(self.data.get_username(), self.data.get_repo_name()))
#        self.__InsertLanguages(self.__GetLanguages())

    """
    def __GetLanguages(self):
        url = 'https://api.github.com/repos/{0}/{1}/languages'.format(self.data.get_username(), self.data.get_repo_name())
        r = requests.get(url)
#        if 300 <= r.status_code:
#            print(r.status_code)
#            print(r.text)
#            print(url)
#            raise Exception("HTTP Error {0}".format(r.status_code))
#            return None
#        else:
#            print(r.text)
#            return json.loads(r.text)
        return self.response.Get(r, type='json')
    """
    def __InsertLanguages(self, j):
        self.data.db_repo.begin()
        repo_id = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())['Id']
        self.data.db_repo['Languages'].delete(RepositoryId=repo_id)
        for key in j.keys():
            self.data.db_repo['Languages'].insert(dict(
                RepositoryId=repo_id,
                Language=key,
                Size=j[key]
            ))
        self.data.db_repo.commit()

