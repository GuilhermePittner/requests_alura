from class_aula import someMethods

# instanciar objeto
usuario_um = someMethods('your_user_here')

# chamar métodos do objeto
lista_de_repos = usuario_um.getRepos('company')
lista_um, lista_dois = usuario_um.extractData(lista_de_repos)
usuario_um.createCsv(lista_um, lista_dois, 'csv_name')

# criar e commitar no repositório
usuario_um.createRepo('repo_name', 'description', 'filename')