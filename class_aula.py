import pandas as pd
import requests
import base64


class someMethods():
    def __init__(self, username):
        print('Entrei no __init__')

        self.username = username
        self.api_base_url = 'https://api.github.com'
        self.access_token = 'your_token'
        self.headers = {'Authorization':"Bearer " + self.access_token, 'X-GitHub-Api-Version': '2022-11-28'}
        print(f'Criei o usuário {self.username}')


    def createRepo(self, repoName, repoDesc, csvName):
        print('================')
        print('Entrei no método createRepo!')
        api_new_repo = 'https://api.github.com'
        url_new_repo = f'{api_new_repo}/user/repos'

        data = {
            'name': repoName,
            'description': repoDesc,
            'private': False
        }
        response = requests.post(url_new_repo, json=data, headers=self.headers)
        print(f'Primeira requisição "createRepo" {response.status_code}')

        with open(f'{csvName}.csv', 'rb') as file:
            file_content = file.read()

        encoded = base64.b64encode(file_content)
        data = {
            'message': 'my first commit',
            'content': encoded.decode('utf-8')
        }

        csvName = csvName+'.csv'
        url = f'{self.api_base_url}/repos/{self.username}/{repoName}/contents/{csvName}'
        response = requests.put(url, json=data, headers=self.headers)
        print(f'Segunda requisição "createRepo" {response.status_code}')

    def getRepos(self, owner):
        print('================')
        print('Entrei no método getRepos!')

        repos_list = []

        url_final = f'{self.api_base_url}/users/{owner}'

        response = requests.get(url_final, headers=self.headers)
        print(f'Status da requisição: {response.status_code}')

        paginas = round((response.json()['public_repos']/30) + 0.5)
        for page_num in range(1, paginas+1):
            try:
                url_dados = f'{self.api_base_url}/users/{owner}/repos?page={page_num}'
                response = requests.get(url_dados, headers=self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)

        return repos_list
    

    def extractData(self, reposList):
        print('================')
        print('Entrei no método extractData!')
        repos_name = []
        repos_language = []

        for page in reposList:
            for repo in page:
                repos_name.append(repo['name'])
                repos_language.append(repo['language'])

        return repos_name, repos_language


    def createCsv(self, reposName, reposLanguage, fileName):
        print('================')
        print('Entrei no método createCsv!')
        dados_csv = pd.DataFrame()
        dados_csv['repos'] = reposName
        dados_csv['linguas'] = reposLanguage
        dados_csv.to_csv(f'{fileName}.csv')