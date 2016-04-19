#!/usr/bin/env python3
# coding: utf-8

from collections import OrderedDict

from mako.template import Template
# from mako.lookup import TemplateLookup
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
            licencas[codigo] = {
                'titulo': codigo,
                'link': partes[1].strip(),
                'sumario': 'sumario blah blah',
            }
    return licencas


def gravar_index(itens_formatados):
    with open('index.html', 'w') as arq_index:
        arq_index.write(carregar_modelo('base').format(texto=itens_formatados))


# def formatar_em_divs(tipos):
#     modelo_item = carregar_modelo('item')
#     itens_formatados = ''
#     for tipo, dados in tipos.items():
#         prods_formatados = ''.join(
#             ['<span class="produto">%s</span>' % prod.strip()
#              for prod in dados[0].split(',')])
#         itens_formatados += modelo_item.format(
#             tipo=tipo, produtos=prods_formatados, licencas=dados[1])
#     return itens_formatados


# def formatar_em_tabela(tipos):
#     modelo_item = carregar_modelo('item-tabela')

#     for tipo, dados in tipos.items():
#         prods_formatados = ''.join(
#             ['<span class="produto">%s</span>' % prod.strip()
#              for prod in dados[0].split(',')])
#         itens_formatados += modelo_item.format(
#             tipo=tipo, produtos=prods_formatados, licencas=dados[1])

#     return carregar_modelo('tabela').format(linhas=itens_formatados)


if __name__ == '__main__':
    licencas = carregar_licencas()
    tipos = carregar_itens()
    dados = {
        'tipos': tipos,
        'licencas': licencas,
    }
    gravar_index(''.join([
        aplicar_plim(modelo, dados)
        for modelo in ['intro', 'lista', 'licencas', 'tabela', 'sobre']
    ]))
