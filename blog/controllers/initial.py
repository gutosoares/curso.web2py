#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Anotações da aula 1:

Toda função que apresenta parâmetros não é exposta:
Ex:
    def soma(x, y):
        return x + y

Existe no objeto request variáveis vars, post_vars e get_vars separadas.

Utilize redirect('http://www.google.com') para redirecionar para outra página

Retorno deve ser serializável(pode ser convertido para string).

Para renderizar uma página:
return response.render("blah.html", {"nome": "Bruno"})

Anotações aula 2:
SQLFORM recebe Table ou Query

check_reserved pode ser utilizado somente com um banco específico
ex: check_reserved = ['mysql']
deve ser utilizado somente em desenvolvimento

default do field pode ser função que retorna um valor

Anotações da aula 3:

query = db.blog.id == 1  # virará objeto query
query2 = db.blog.title.startswith('meu') # like meu%
query & query2 # retorna query AND query2
query | query2 # retorna query OR query2
query &= query2 # realiza and e guarda retorno em query

db(queryset).operation()
db(queryset)._operation() # verifica sql gerada

db(queryset).operation() retorna lista de rows
rows tem metodo json e xml do resultado, assim como exporta csv
row = rows[0]
cada row representa tupla retornada e caso seja alterada sua mudança
será refletida no banco de dados.

Anotações da aula 4:
Exemplo de logging está na raiz e como utilizar é só ler o arquivo.
No model está a instância do logger.

Nome Handler - Saída
consoleHandler - console
rotatingFileHandler - arquivo
messageBoxHandler - sysnotify

http://127.0.0.1:8000/user/<item>
login - autenticar
register - cadastrar
retrieve_password - esqueci a senha
profile - perfil do usuário editável
logout - saída do sitema


auth é callable que retorna formulário de autenticação

auth.user ou session.auth.user para informações do usuário autenticado
auth.user_id e auth.user_groups também estão disponíveis

response.download(request, db) - media não fica no banco de dados
mas seu caminho sim

Para adicionar campos extras ao usuário
auth.settings.extra_fields['auth_user'] = [lista de campos extras]
Exemplo de desabilitar registro
auth.settings.actions_disabled = ['register']

Anotações da aula 5:

Template do web2py de forma isolada.
from gluon.template import render

Utilize template com cautela. Não coloque código de controle na view.

Idéia legal: cria página email nas views para emails com html.

response.render para renderizar um template, só passar caminho e
variáveis do contexto.
response.render(path,**args)

mudar response.view no controller para mudar o template.

Anotações da aula 6:

action do form como URL para garantir caminho correto.

do gluon.tools tem o prettydate que é função de datas para exibir ao estilo "7 minutos atrás"

Anotações da aula 7:

sqlite quando entra em modo shell realiza lock do arquivo.

proccess das classes Form tem função onvalidation e onaccept

onvalidation = executa após os requires validarem os campos,
 pode ser útil para uma nova validação
 ocorre ainda na etapa de validação.

onaccept = momento após formulário ter sido aceito.

Evite HELPERS a todo custo!

Modificar representação em tela de algum campo do banco de dados.
Post.created_on.represent = lambda valor: prettydate(valor)

SQLFORM.factory - fbrica de formulários customizados
SQLFORM.grid - grid completo de um model
SQLFORM.smartgrid -semelhante a grid mas com referencia entra tabelas(references)

Anotações da aula 8:

Requests por segundo tem mais a ver com servidor web  que o framework utilizado

Instalar plugins é só dar upload no w2p.
Links interessantes:

http://dev.s-cubism.com/web2py_plugins
http://web2py.com/plugins

Web2py é convention over configuration, mas para algo personalizado sempre tem alguma configuração.

Criação de plugins:
- Cria módulo com funções e classes no padrão plugin_*
- cria controller para expor funcionalidade do plugin no padrão plugin_*
- cria pasta em views plugin_*, cria arquivo dentro com nome da action exposta no controller
por ultimo vá em plugin e empacotar plugin

LOAD() para utilizar plugin, para ser chamado via ajax...passe parametro ajax = True

db(...).select(cache=(sistema_de_cache, tempo)) para fazer cache de consultas
ex:
db(...).select(cache=(cache.ram, tempo))
cache.ram - guarda na memória
cache.disk - guarda em disco

outro tipo de cache cache.<ram,disk>(chave, callable, time_expire)
ex:
t = cache.ram('time',time.ctime,10)

ou para cada user um cache isolado

t = cache.ram('%s_time'%user.id,time.ctime,10)


mais uma maneira de fazer cache com decorador:
@cache('templatecache',cache_model=cache.ram, time_expire=10)
def templatecache():
    ...

session.connect(request, response, db) para colocar sessão em cache
session.connect(request, response, cookie_key='chave_secreta') para colocar sessão no cookie

'''


def home():
    posts = db(Post.is_draft==False).select(orderby=~Post.created_on)
    return {
        'posts': posts
    }
    # return dict(
    #     nome="Cássio",
    #     lista=[
    #         'item1',
    #         'item2'
    #     ],
    #     curso="computação"
    # )


def contact():
    if request.env.request_method == "POST":
        if IS_EMAIL()(request.vars.email)[1]:
            response.flash = 'Email invalido'
            redirect(URL('home'))
        message = request.vars.mensagem
        mail.send(
            to=mail.settings.sender,
            subject="Contato",
            message=message
        )
    return "Email enviado com sucesso!"
    # redirect(URL('initial','home'))

def about():
    return "sobre o autor"


def user():
    logger.info(request.args)
    if request.args(0) == 'register':
        fields = ['bio', 'photo', 'gender']
        for field in fields:
            db.auth_user[field].readable = False
            db.auth_user[field].writable = False
    return auth()


def register():
    return auth.register()


def login():
    return auth.login()


def account():
    '''Cuidado pois suário já autenticado irá sofrer redirecionamento'''
    return{
        'login': auth.login(),
        'register': auth.register()
    }


def download():
    return response.download(request, db)
