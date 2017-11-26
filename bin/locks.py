# -*- coding: cp1251 -*-
# locks module
# Убрать "лишние" сообщения об ошибках, когда блокировки проверяются
import log,os,sys,cfg, portalocker,fileIO

def _log(logf,facility,logstr):
    """ Internal log wrapper """
    logf.log(str(__name__),facility,logstr)

def set_file_lock(logf,lockf):
    """ Set file lock """
    try:
        portalocker.lock(lockf,portalocker.LOCK_EX|portalocker.LOCK_NB)
    except:
        _log(logf,log.ERROR,"Ошибка эксклюзивной блокировки файла ["+str(lockf.name)+']')
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return -1
    return 1


def check_file_lock(logf,path):
    """ Set locking """
    if (fileIO.file_exists(path)==cfg.err_FALSE):
        return cfg.err_FALSE
    else:
        try:
            lockf=open(path,"a+")
        except:
            _log(logf,log.ERROR,"Ошибка открытия файла ["+str(path)+']')
            _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
            # Что возвращать? Hадо нечто типа ошибки, чтобы обрабатывать дальше. Может -1? ;-)
            return cfg.err_TRUE
        if (set_file_lock(logf,lockf)!=cfg.err_SUCCESS):
            _log(logf,log.WARNING,"Обнаружен блокированный файл ["+str(path)+']')
            return cfg.err_TRUE
        else:
            lockf.close()
            _log(logf,log.DEBUG,"Файл ["+str(path)+"] существует, но не блокирован")
            return cfg.err_FALSE
        

def unset_file_lock(logf,lockf):
    """ Set locking """
    try:
        portalocker.unlock(lockf)
    except:        
        _log(logf,log.ERROR,"Ошибка разблокировки файла ["+str(lockf.name)+']')
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return 0
    
    return 1

