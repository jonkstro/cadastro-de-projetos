from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .utils import email_html, password_is_valid
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
import os
from django.conf import settings
from .models import Ativacao
from hashlib import sha256


# Create your views here.
# criar a view da tela de cadastro do projeto:
def cadastro(request):
    #return render(request, 'cadastro.html')

#caso o metodo seja GET (pela url), irá redirecionar
    if(request.method == 'GET'):
       if(request.user.is_authenticated):
           return redirect('/')
       return render(request, 'cadastro.html')


#  TÁ DANDO ERRO AO TENTAR CADASTRAR NOME COMPLETO E TELEFONE !!!!!!!

#caso o metodo seja POST (pelo formulario), irá cadastrar a conta
    elif (request.method == "POST"):
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

#se a senha não for válida será redirecionado:
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')

        try:
            user = User.objects.create_user(first_name=nome, last_name=sobrenome ,username=usuario, email=email, password=senha, is_active=False)
            user.save()

# TÁ DANDO ERRO AO TENTAR CADASTRAR NOME COMPLETO E TELEFONE !!!!!!!
        # p1 = Pessoa(nome_completo = nome_completo, telefone = telefone)
        # p1.save()
            #criação de token para ativação de conta do usuario:
            token = sha256(f"{usuario}{email}".encode()).hexdigest()
            ativacao = Ativacao(token = token, user = user)
            ativacao.save()


# enviar email para confirmação de usuário:
            # criar pagina html para envio de email
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=usuario, link_ativacao="127.0.0.1:8000/auth/ativar_conta/{token}")            


            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
        
            return redirect('/auth/logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')

# Criar a view de logar:
def logar(request):
    if (request.method == 'GET'):
        # caso já esteja autenticado será redirecionado a pagina inicial, 
        # senão será redirecionado para a pagina de login
        if (request.user.is_authenticated):
            return redirect('/')
        return render(request, 'logar.html')
    # caso seja o metodo POST (por meio do formulario), será realizado a validação
    # do usuario e senha para login
    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        usuario = auth.authenticate(username=username, password=senha)
        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            return redirect('/pacientes')


# Criar a view para sair da aplicação:
def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')


# Criar função para ativação da conta por e-mail
def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/logar')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/logar')