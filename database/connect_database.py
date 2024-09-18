#!/usr/bin/python
# -*- coding: latin-1 -*-

import mysql.connector
import mysql.connector.errors
import socket


def busca_ip(nome_maquina):
    try:
        return socket.gethostbyname(nome_maquina)
    except socket.error as erro:
        raise NameError(f"Verifique o nome do host informado: {erro}")


def conecta_banco(nome_host='servidorBalcao'):
    config = {'host': f'{busca_ip(nome_host)}',
              'database': 'clarionerp',
              'user': 'burite',
              'password': 'burite123',
              'port': '3307'}
    try:
        return mysql.connector.connect(**config)
    except:
        raise Exception('Erro de comunica??o com o servidor',
                        mysql.connector.errors)


if __name__ == '__main__':
    con = conecta_banco()
    print('Conexão bem sucedida')
    con.close()
    