#!/usr/bin/python
# -*- coding: cp1251 -*-
# Основной модуль программы
#
# Управление импортом/экспортом GMS OfficeTools
# TODO:
# + Support range of dates (01-05, Now-Now-1, etc)
# + How to implement multiple tasks? Per shops/dates or per modules?
# + Auto switching all of INI-file parameters, one default INI for one module
# + Split reports to orders, inventarization, zakaz, etc
# How to sync files?
# + Move file transfer to module?
# + Переделать названия переменных shop and firm на source and dest, а ключи на in/to and from
# Сделать поддержку usage в каждом модуле
import cfg, impexp,log,ini,getopt, sys,os,thread,imp,date,string,mailIO,inspect;

__desc__='Основной'

logf=None

def startup_init():
    """ Startup initialization """
    global logf
    logf=log.LogFile()
    logf.open(str(__name__),__name__,str(__name__))
    sys.path.append(cfg.modules)

def shutdown_done():
    """ Shutdown  post-runs """
    global logf
    mailIO.send_message(logf,logf.errqueue,'Список ошибок модуля ['+str(__desc__)+']')
    logf.close(str(__name__))

def _log(logf,facility,logstr):
    """ Internal log wrapper"""
    logf.log(str(__name__),facility,logstr)


def display_usage():
    print """ Использование:\r
    impexp -a|--action <режим> -m|--module <модуль> -f|--from <магазины> -t|--to <магазины> -d|--date <даты> --noauto \r
    где:\r
    <режим> - режим запуска, один из: import, export, gui_import, gui_export\r
    <модуль> - название модуля для запуска, например: reports, orders, inventories\r
    <магазины> - список магазинов, от одного до бесконечности, через запятую, например: eva1,eva2,eva7\r
    <даты> - даты, от одной до бесконечности, можно указывать периоды, макросы, сокращения, например:\n
    30  - тридцатое число текущего месяца\r
    30.07.2003 - 30-ое июля 2003 года\r
    29:31 - начальная дата: 29-ое число текущего месяца; конечная дата: 31-ое число текущего месяца\r
    now:now-1 - начальная дата: текущее число текущего месяца; конечная дата: текущее число текущего месяца минус один день\r
    30,29,30.07.2003:now,now-5:now-2\n
    --noauto - запускать программу GMS Import/Export в ручном режиме

    """

def start_modules():
    """ Parse command line and start modules """
    global logf
    # BUG.
    # this log-string will never be in the log file, because loglevel is low than DEBUG ;(
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    # 
    dates=date.get_cur_date(logf)
    runmode=None
    module=None
    auto=1
    wait=1
    upload=1
    do_archive=1
    src_shops=None
    dst_shops=None
    try:
        options,args=getopt.getopt(sys.argv[1:],'a:t:f:m:d:l:u:s:g:p:wn',['action=','to=','from=','module=','date=','loglevel=','shop=','get=','put=','wait','noauto'])
        if (len(options)==0):
            display_usage()
            return 0
    except getopt.GetoptError:
        _log(logf,log.ERROR,"Неизвестная опция или опция без параметра");
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        display_usage()
        return -1;
    except:
        _log(logf,log.ERROR,"Ошибка разбора командной строки");
        _log(logf,log.ERROR,"Сообщение системы: [%s.%s]" % str(sys.exc_info()[0],str(sys.exc_info()[1])));
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        display_usage()
        return -1;
    for option,value in options:
        value=string.lower(value)
        if (option in ('-a','--action')):
            runmodes=[]
            for mode in cfg.runmodes:
                runmodes.append(cfg.runmodes[mode])
            if (value not in runmodes):
                _log(logf,log.ERROR,"Неизвестный режим запуска [%s]" % str(value));
                _log(logf,log.ERROR,"Доступны только "+str(runmodes));
                _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
                return -1
            else:
                for mode_ in cfg.runmodes.items():
                    if (value==mode_[1]):
                        runmode=mode_[0]
                        break

        elif (option in ('-t','--to') or (option in ('-s','--shop'))):
            wo_shops=''
            if (string.count(value,'-')>0):
                value_=string.split(value,'-')
                value=value_[0]
                wo_shops=string.split(value_[1],',')
            if (value=='*'):
                dst_shops=[]
                for counter in cfg.shops:
                    dst_shops.append(counter)
            else:
                dst_shops=string.split(value,',')
            for shop_ in dst_shops:
                try:
                    shop=cfg.shops[shop_]
                except:
                    _log(logf,log.ERROR,"Неизвестный магазин (назначения) ["+str(shop_)+"]");
                    _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                    _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
                    return -1
            if (wo_shops!=''):
                for wo_shop_ in wo_shops:
                    try:
                        dst_shops.remove(wo_shop_)
                    except:
                        _log(logf,log.ERROR,"Неизвестный магазин (назначения), который необходимо пропустить ["+str(wo_shop_)+"]");
                        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
                        return -1

        elif (option in ('-f','--from')):
            wo_shops=''
            if (string.count(value,'-')>0):
                value_=string.split(value,'-')
                value=value_[0]
                wo_shops=string.split(value_[1],',')

            if (value=='*'):
                src_shops=[]
                for counter in cfg.shops:
                    src_shops.append(counter)
            else:
                src_shops=string.split(value,',')
            for shop_ in src_shops:
                try:
                    shop=cfg.shops[shop_]
                except:
                    _log(logf,log.ERROR,"Неизвестный магазин (источника) ["+str(shop_)+"]");
                    _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                    _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
                    return -1
            if (wo_shops!=''):
                for wo_shop_ in wo_shops:
                    try:
                        src_shops.remove(wo_shop_)
                    except:
                        _log(logf,log.ERROR,"Неизвестный магазин (источника), который необходимо пропустить ["+str(wo_shop_)+"]");
                        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
                        return -1

        elif (option in ('-m','--module')):
            try:
                (modfile,modname,moddesc)=imp.find_module(value)
            except:
                _log(logf,log.ERROR,"Hе могу найти модуль  ["+str(value)+"]");
                _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
                return -1
            try:
                module=imp.load_module(value,modfile,modname,moddesc)
            except:
                _log(logf,log.ERROR,"Hе могу загрузить модуль  ["+str(value)+"]");
                _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
                return -1
        elif (option in ('-d','--dates')):
            # move dates parse to module
            #dates=date.get_dates(value);
            dates=value;
        elif (option in ('-l','--loglevel')):
            logf.setlevel(int(value));
        elif (option in ('-n','--noauto')):
            # if (value=='yes'):
            #   auto=1
            #elif (value=='no'):
            #   auto=0
            auto=0
        elif ((option in ('-g','--get')) or (option in ('-p','--put')) ):
            if (value=='yes'):
                upload=1
            elif (value=='no'):
                upload=0
        elif (option in ('-w','--wait')):
            if (value=='yes'):
                wait=1
            elif (value=='no'):
                wait=0

    if (runmode==None):
        _log(logf,log.ERROR,"Hе задан режим запуска ["+cfg.runmodes[cfg.IMPORT]+" или "+cfg.runmodes[cfg.EXPORT]+" или "+cfg.runmodes[cfg.GUI_IMPORT]+" или "+cfg.runmodes[cfg.GUI_EXPORT]+"]");
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
        return -1
    if (module==None):
        _log(logf,log.ERROR,"Hе задан модуль для запуска");
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));                                    
        return -1
    if (runmode!=cfg.GUI_IMPORT) and (runmode!=cfg.GUI_EXPORT) and (runmode!=cfg.GUI):
        if (dst_shops==None):
            _log(logf,log.ERROR,"Hе задан ни один магазин назначения");
            _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return -1
        if (src_shops==None):
            _log(logf,log.ERROR,"Hе задан ни один магазин-источник");
            _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return -1


    if (module.__runmodes__.count(cfg.runmodes[runmode])==0):
        _log(logf,log.ERROR,"Модуль ["+(module.__name__)+"] не поддерживает режим запуска ["+cfg.runmodes[runmode]+"]");
        return -1
    _log(logf,log.INFO,"Запуск модуля %s" % str(module.__name__))
    try:
        module_=eval('module.'+module.__name__+'()')
    except:
        _log(logf,log.ERROR,"Ошибка инициализации модуля [%s]"% str(module.__name__));
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
        return -1

    try:
        result=module_.start_module(auto,runmode,upload,src_shops,dst_shops,dates,logf.loglevel,args);
        _log(logf,log.INFO,"Завершение работы модуля [%s] с кодом выхода [%s]" % (str(module.__name__),str(cfg.errors[result])));
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    except:
        _log(logf,log.ERROR,"Ошибка запуска модуля [%s]" % str(module.__name__));
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));        
        return -1

    return result


# main
if (__name__=='__main__'):
    __name__='kernel'
    startup_init()
    result=start_modules()
    shutdown_done()
    sys.exit(result)
