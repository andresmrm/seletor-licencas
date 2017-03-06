#!/usr/bin/env python3
# coding: utf-8

from collections import OrderedDict

from bs4 import BeautifulSoup
from mako.template import Template
import plim


def carregar_modelo(nome, ext='html'):
    with open('modelos/%s.%s' % (nome, ext), 'r') as arq_modelo:
        texto = arq_modelo.read()
    return texto


def aplicar_plim(modelo, dados):
    return Template(carregar_modelo(modelo, 'slim'),
                    preprocessor=plim.preprocessor).render(**dados)


def carregar_itens():
    with open('itens', 'r') as arq_itens:
        texto = arq_itens.read()
        # tipos = OrderedDict()
        linhas = []
        for bloco in texto.split('\n\n'):
            partes = bloco.split('\n')
            tipo = partes[0].lower().strip()
            prods = partes[1].lower()
            # meio = partes[2].lower().strip()
            licencas = partes[3]
            # tipos[tipo] = (prods, licencas)
            linhas.append({
                'id': str(len(linhas)),
                'tipo': tipo,
                'produtos': [prod.strip() for prod in prods.split(',')],
                'licencas': [[x.strip() for x in lic.strip().partition(' ')]
                             for lic in licencas.split(',')]
            })
    return linhas


def carregar_licencas():
    with open('licencas', 'r') as arq_licencas:
        texto = arq_licencas.read()
        licencas = OrderedDict()
        for bloco in texto.split('\n\n'):
            partes = bloco.split('\n')
            codigo = partes[0].strip()
            link = partes[1].strip()
            sem_traducao = False
            if link.endswith(' *'):
                sem_traducao = True
                link = link[:-2].strip()
            explicacao = ''
            if len(partes) > 3:
                explicacao = partes[3].strip()
            licencas[codigo] = {
                'titulo': partes[2].strip(),
                'link': link,
                'sem_traducao': sem_traducao,
                'explicacao': explicacao,
                'sumario': 'sumario blah blah',
            }
    return licencas


def gravar_arq(arq, dados, modelos):
    itens_formatados = ''.join([aplicar_plim(modelo, dados)
                                for modelo in modelos])
    subs = carregar_modelo('base').format(texto=itens_formatados)
    soup = BeautifulSoup(subs, 'html.parser')
    with open(arq+'.html', 'w') as arq_index:
        arq_index.write(soup.prettify())


if __name__ == '__main__':
    licencas = carregar_licencas()
    tipos = carregar_itens()
    dados = {
        'tipos': tipos,
        'licencas': licencas,
    }

    gravar_arq('index', dados,
               ['intro2', 'lista', 'licencas', 'tabela', 'sobre'])
    gravar_arq('prefeitura', dados,
               ['intro', 'lista', 'licencas', 'tabela', 'sobre'])
