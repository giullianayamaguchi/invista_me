from django.shortcuts import render, HttpResponse, redirect 
from .models import Investimento
from .forms import InvestimentoForm
from django.contrib.auth.decorators import login_required

def pagina_inicial(request):
    return HttpResponse('Pronto para investir')

def contato(request):
    return HttpResponse('Para dúvidas, enviar um e-mail explicando o seu caso')

def historia(request):
    pessoa = {
        'nome' :'jeff',
        'idade' : 19,
        'hobby' : 'ler'
    } 
    return render(request, 'investimento/historia.html')

def investimento_registrado(request):
    investimento = {
        'tipo_investimento': request.POST.get('tipoInvestimento')
    }
    return render(request, 'investimento/investimento_registrado.html', investimento)

def investimentos(request):
    dados = {
        'dados' :Investimento.objects.all()
    }
    return render( request, 'investimento/investimentos.html', context=dados)

def detalhe(request, id_investimento):
    dados = {
        'dados' : Investimento.objects.get(pk=id_investimento) 
    }
        
    return render(request, 'investimento/detalhe.html', dados)

@login_required
def criar(request):
    if request.method == 'POST':
        Investimento_Form = InvestimentoForm(request.POST)
        if Investimento_Form.is_valid():
            Investimento_Form.save()
        return redirect('investimentos')
    else:
        Investimento_Form = InvestimentoForm()
        formulario = {
            'formulario' : Investimento_Form
        }
    return render( request, 'investimento/novo.html', context=formulario)

@login_required
def editar(request, id_investimento):
    investimento = Investimento.objects.get(pk= id_investimento)
    #novo_investimento/1 -> GET
    if request.method == 'GET':
        formulario = InvestimentoForm(instance=investimento)
        return render(request, 'investimento/novo.html', {'formulario': formulario})
    #caso seja POST
    else: 
        formulario = InvestimentoForm(request.POST, instance=investimento)
        if formulario.is_valid():
            formulario.save()
        return redirect('investimentos')

@login_required    
def excluir(request, id_investimento):
    investimento = Investimento.objects.get(pk= id_investimento)
    if request.method == 'POST':
        investimento.delete()
        return redirect('investimentos')
    return render(request, 'investimento/confirmar_exclusao.html', {'item': investimento} )