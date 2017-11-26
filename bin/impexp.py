# -*- coding: cp1251 -*-
# "import<->export" module

import cfg,sys,os,log,time;

def _log(logf,facility,logstr):
    """ Internal log wrapper """
    logf.log(str(__name__),facility,logstr)

def start_ie(logf,args=""):
    """ Start otimpexp.exe """
    _log(logf,log.DEBUG,"В функции start_ie ");        
    try:
        _log(logf,log.INFO,"Запуск "+str(cfg.ot_ie)+" "+str(args));        
        exitcode=os.spawnv(os.P_WAIT,cfg.ot_ie,(cfg.ot_ie,args));
        _log(logf,log.INFO,"Код возврата ["+str(exitcode)+"]");
    except:
        _log(logf,log.ERROR,"Ошибка запуска ["+str(cfg.ot_ie)+" "+str(args));
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
        return -1;
    # БЛЯДЬ! Hу какого хуя в этой винде прут глюки такие?
    # Кто же виноват?
    # time.sleep(10)
    _log(logf,log.DEBUG,"Выход из функции start_ie ");
    return exitcode;
    
def start_export(logf,args=""):
    """ Run export """
    _log(logf,log.DEBUG,"В функции start_export ");    
    exitcode=start_ie(logf,args);
    if ( exitcode!=0 ):
        _log(logf,log.ERROR,"Hевозможно завершить процесс экспорта");
        _log(logf,log.ERROR,str("Код выхода ["+str(exitcode)+"]"));
        return -1;
    _log(logf,log.DEBUG,"Выход из функции start_export ");
    return 0;

def start_import(logf,args=""):
    """ Run import """
    _log(logf,log.DEBUG,"В функции start_import ");
    exitcode=start_ie(logf,args);
    if ( exitcode!=0 ):
        _log(logf,log.ERROR,"Hевозможно завершить процесс импорта");
        _log(logf,log.ERROR,"Код выхода ["+str(exitcode)+"]");
        return -1;
    _log(logf,log.DEBUG,"Выход из функции start_import ");            
    return 0;
