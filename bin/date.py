# -*- coding: cp1251 -*-
# module for parse date and return valid full date
# TODO:
# + Check if last date in period is greater than first date in period (get_dates->split_period_date?)
# + А есть ли поддержка даты без года?
import os, sys, string, log,cfg,time,inspect


def _log(logf,facility,logstr):
    """ Internal log wrapper """
    logf.log(str(__name__),facility,logstr)
    
def is_valid_date(date,logf):
    """ Check date for valid format """
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    dates=string.split(date,'.')
    try:
        if (int(dates[0]) in (range(1,32)) and  int(dates[1]) in (range(1,13))
            and (int(dates[2]) in (range(00,100)) or int(dates[2]) in (range(0001,10000))) and len(dates)==3):
            _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return 1
    except:
        _log(logf,log.ERROR,"Ошибочная дата  ["+str(date)+"]");
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return -1
    else:
        _log(logf,log.ERROR,"Ошибочная дата  ["+str(date)+"]");
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return -0

def is_good_period_date(begin,end,logf):
    """ Check begin date less than end date """
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    # Черт! В долбанной винде нет такой возможности ;-(
    # Поэтому пока выходим
    return 1
    if (time.mktime(time.strptime(begin,'%d.%m.%Y')) >time.mktime(time.strptime(end,'%d.%m.%Y')) ):
        _log(logf,log.ERROR,"Hачальная дата  ["+str(begin)+"] больше конечной ["+str(end)+"]");
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return -1
    else:
        return 1
    _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    
def is_period_date(date,logf):
    """ Check date for period """
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    if (string.count(date,':')==1):
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return 1
    elif (string.count(date,':')==0):
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return 0
    elif (string.count(date,':')>1):
        _log(logf,log.ERROR,"Ошибочная дата  ["+str(date)+"]");
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return -1
    _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));

def split_period_date(date,logf):
    """ Split period to two dates """
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    if (is_period_date(date,logf)==1):
        dates=string.split(date,':');
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return dates[0],dates[1]
    else:
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return date,date

def process_macros_date(date,logf):
    """ Replace macroses in dates """
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    date=string.lower(date)                
    dates=string.split(date,'-')
    if (len(dates)==2):
        if (dates[0]=='now'):
            dates[0]=time.time()
            try:
                dates[1]=str(int(dates[1])*86400)
            except:
                _log(logf,log.ERROR,"Ошибочная дата  ["+str(date)+"]");
                _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
                return date
            return time.strftime('%d.%m.%Y',time.localtime(int(dates[0])-int(dates[1])));
        else:
            _log(logf,log.ERROR,"Ошибочная дата  ["+str(date)+"]");
            _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return date
    elif (dates[0]=='now'):
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return get_cur_date(logf)
    _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    return date
    
def normalize_date(date,logf):
    """ Normalize date to full """
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    day=time.strftime('%d')
    month=time.strftime('%m')
    year=time.strftime('%Y')
    if (string.count(date,'/')==0):
        if (string.count(date,'.')==0):
            _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return (str(date)+'.'+str(month)+'.'+str(year))
        else:
            date=string.split(date,'.')
    else:
        date=string.split(date,'/')
        
    if (len(date)==2):
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return (str(date[0])+'.'+str(date[1])+'.'+str(year))
    elif (len(date)==3):
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return (str(date[0])+'.'+str(date[1])+'.'+str(date[2]))
    else:
        _log(logf,log.ERROR,"Ошибочная дата  ["+str(date)+"]");
        _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return (str(day)+'.'+str(month)+'.'+str(year))

def get_cur_date(logf):
    """ Get current date """
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    day=time.strftime('%d')
    month=time.strftime('%m')
    year=time.strftime('%Y')
    _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    #return [(str(day)+'.'+str(month)+'.'+str(year))]
    return (str(day)+'.'+str(month)+'.'+str(year))
    
def get_dates(dates,logf):
    """ Parse string, normalize all dates and return list of  """
    _log(logf,log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    valid_dates=[];
    dates=string.split(dates,',');
    for _date in dates:
        (begin,end)=split_period_date(_date,logf)
        begin=normalize_date(process_macros_date(begin,logf),logf)
        end=normalize_date(process_macros_date(end,logf),logf)
        if (is_valid_date(begin,logf)==1) and (is_valid_date(end,logf)==1) and (is_good_period_date(begin,end,logf)==1):
            valid_dates.append([begin,end])
    _log(logf,log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
    return valid_dates
