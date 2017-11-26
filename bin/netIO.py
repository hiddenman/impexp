# -*- coding: cp1251 -*-
# Модуль для сетевых операций
import os,sys,cfg,log,ini,telnetlib

def is_host_alive(logf,server):
    """ Check is host alive  """
    pass

def is_mssql_alive(server,port=cfg.sqlport):
    """ Check is MSSQL listen on specified port  """
    try:
        conn=telnetlib.Telnet()
        conn.open(server,port)
    except:
        return 0
    else:
        try:
            conn.close()
            return 1
        except:
            pass
