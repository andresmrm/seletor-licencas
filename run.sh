#!/bin/env bash

ls css/main.css js/main.js modelos/* *.py licencas itens | entr bash -c '. env/bin/activate; python tratar_dados.py; midori -e Reload' &
cd css; ls main.scss | entr sass --scss main.scss main.css
