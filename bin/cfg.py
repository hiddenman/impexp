# -*- coding: cp1251 -*-
#  -*- coding: cp1251 -*-
# Модуль конфигурации
# TODO
# Hадо перенести опции, которые будут менять, в ini-файл, чтобы редактировать обычным редактором
# хотя тогда непонятно, как делать словари ;(

import sys,os

# Корень (root), где лежит программа и все остальное
#
if (os.name=='nt'):
    # для M$ Windows (слэши указывать двойные!)
    # для сетевого пути тоже самое, если \\server, то надо писать \\\\server
    root="d:\\robot\\impexp"
elif (os.name=='posix'):
    # для POSIX-систем
    root="/home/andy/devel/rush/impexp"

######################
# Секция каталогов, где будет все располагаться
#
# Каталог с исполняемыми файлами
bin=os.path.join("%s","bin") % root
# Каталог с модулями
modules=os.path.join("%s","modules") % bin
# Каталог с настроками
etc=os.path.join("%s","etc") % root
# Каталог с INI-файлами
ini=os.path.join("%s","ini") % etc
# Временный каталог для работы
tmp=os.path.join("%s","tmp") % root
# Каталог верхнего уровня с данными
var=os.path.join("%s","var") % root
# Каталог для хранения lock-файлов выполнения
run=os.path.join("%s","run") % var
# Каталог лог-файлов
log=os.path.join("%s","log") % var
# Каталог промежуточного уровня с данными
lib=os.path.join("%s","lib") % var
# Каталог низшего уровня с данными
data=os.path.join("%s","data") % lib


if (os.name=='nt'):
    # для M$ Windows
    # Каталог для файлов импорта
    improot=os.path.join("%s","import") % data
    # Каталог для файлов экспорта
    exproot=os.path.join("%s","export") % data
    # Каталог для архивов
    arcroot=os.path.join("%s","archive") % data
    # Путь к исполняемому файлу OfficeTools Import/Export
    ot_ie=os.path.join("%s","impexp.exe") % bin;
    # Каталог к утилите MSSQL - isql
    ms_isql=os.path.join("%s","isql.exe") % bin;
    # Каталог к утилите MSSQL - bcp
    ms_bcp=os.path.join("%s","bcp.exe") % bin;

    charset='cp1251'
    guicharset='cp1251'

elif (os.name=='posix'):
    # для POSIX-систем
    improot=os.path.join("%s","import") % data
    exproot=os.path.join("%s","export") % data
    arcroot=os.path.join("%s","archive") % data
    ot_ie="/bin/true"
    ms_isql="/bin/true"
    ms_bcp="/bin/true"
    charset='koi8-r'
    guicharset='cp1251'

unixcharset='koi8-r'
wincharset='cp1251'
wincharset2='cp1251'


# Адреса, на  которые посылать e-mail-ы об успешном выполнении задачи и об ошибках
# Адрес, с которого посылать
emails={
    'from':'hiddenman@tpway.com',
    # 'to':['andy@eva.dp.ua','aid@eva.dp.ua','vpiv@eva.dp.ua']
    'to':['hiddenman@tpway.com']
    }

# Адрес smtp-сервера
smtpserver='192.168.242.1'
# remote_opcode=

###########################
# Секция настроек для магазинов


# Коды магазинов в базе
shops={
    'office':1,
    'eva1':2,
    'eva2':12,
    'eva3':13,
    'eva4':14,
    'eva5':15,
    'eva6':16,
    'eva7':17,
    'eva8':18,
    'eva9':19,
    'eva10':20,
    'eva11':21,
    'eva12':22
    }

# Имя сервера для каждого магазина
# раздельно для импорта и экспорта
servers={
    'export':{
    'office':'192.168.1.223',
    # 'office':'192.168.1.222',
    'eva1':'192.168.2.253',
    'eva2':'192.168.4.253',
    'eva3':'192.168.5.253',
    'eva4':'192.168.6.2',
    'eva5':'192.168.11.2',
    'eva6':'192.168.7.253',
    'eva7':'192.168.8.253',
    'eva8':'192.168.9.2',
    'eva9':'192.168.10.2',
    'eva10':'192.168.14.2',
    'eva11':'192.168.15.2',
    'eva12':'192.168.16.2'
    },
    'import':{
    'office':'192.168.1.223',
    # 'office':'192.168.1.222',
    'eva1':'192.168.2.253',
    'eva2':'192.168.4.253',
    'eva3':'192.168.5.253',
    'eva4':'192.168.6.2',
    'eva5':'192.168.11.2',
    'eva6':'192.168.7.253',
    'eva7':'192.168.8.253',
    'eva8':'192.168.9.2',
    'eva9':'192.168.11.2',
    'eva10':'192.168.14.2',
    'eva11':'192.168.15.2',
    'eva12':'192.168.16.2'
    }
    }

# Hомер TCP/IP порта, на котором MSSQL слушает запросы
sqlport=1433

# Имя базы данных для каждого магазина
# раздельно для импорта и экспорта
dbnames={
    'export':{
    'office':'OTData',
    'eva1':'OTData',
    'eva2':'OTData',
    'eva3':'OTData',
    'eva4':'OTData',
    'eva5':'OTData',
    'eva6':'OTData',
    'eva7':'OTData',
    'eva8':'OTData',
    'eva9':'OTData',
    'eva10':'OTData',
    'eva11':'OTData',
    'eva12':'OTDATA'
    },
    'import':{
    'office':'OTData',
    'eva1':'OTData',
    'eva2':'OTData',
    'eva3':'OTData',
    'eva4':'OTData',
    'eva5':'OTEva5',
    'eva6':'OTData',
    'eva7':'OTData',
    'eva8':'OTData',
    'eva9':'OTData',
    'eva10':'OTData',
    'eva11':'OTData',
    'eva12':'OTDATA'
    }
    }

# Имя пользователя для каждого магазина
# раздельно для импорта и экспорта
users={
    'export':{
    'office':'sa',
    'eva1':'sa',
    'eva2':'sa',
    'eva3':'sa',
    'eva4':'sa',
    'eva5':'sa',
    'eva6':'sa',
    'eva7':'sa',
    'eva8':'sa',
    'eva9':'sa',
    'eva10':'sa',
    'eva11':'sa',
    'eva12':'sa'
    },
    'import':{
    'office':'sa',
    'eva1':'sa',
    'eva2':'sa',
    'eva3':'sa',
    'eva4':'sa',
    'eva5':'sa',
    'eva6':'sa',
    'eva7':'sa',
    'eva8':'sa',
    'eva9':'sa',
    'eva10':'sa',
    'eva11':'sa',
    'eva12':'sa'
    }
    }

# Пароль пользователя для каждого магазина
# раздельно для импорта и экспорта
# Раздельно зашифрованный и незашифрованный
pwds={
    'export':{

    'office':
    {
    'crypt':'',
    'raw':''
    },

    # Это пароль к moon
    # 'office':
    # {
    # 'crypt':'',
    # 'raw':''
    # },

    'eva1':
    {
    'crypt':'',
    'raw':''
    },

    'eva2':
    {
    'crypt':'',
    'raw':''
    },

    'eva3':
    {
    'crypt':'',
    'raw':''
    },

    'eva4':
    {
    'crypt':'',
    'raw':''
    },

    'eva5':
    {
    'crypt':'',
    'raw':''
    },

    'eva6':
    {
    'crypt': '',
    'raw':''
    },

    'eva7':
    {
    'crypt':'',
    'raw':''
    },

    'eva8':
    {
    'crypt':'',
    'raw':''
    },

    'eva9':
    {
    'crypt':'',
    'raw':''
    },

    'eva10':
    {
    'crypt':'',
    'raw':''
    },

    'eva11':
    {
    'crypt':'',
    'raw':''
    },

    'eva12':
    {
    'crypt':'',
    'raw':''
    }


    },

    'import':{

    'office':
    {
    'crypt':'',
    'raw':''
    },

    # Это пароль к moon
    # 'office':
    # {
    # 'crypt':'',
    # 'raw':''
    # },

    'eva1':
    {
    'crypt':'',
    'raw':''
    },

    'eva2':
    {
    'crypt':'',
    'raw':''
    },

    'eva3':
    {
    'crypt':'',
    'raw':''
    },

    'eva4':
    {
    'crypt':'',
    'raw':''
    },

    'eva5':
    {
    'crypt':'',
    'raw':''
    },

    'eva6':
    {
    'crypt': '',
    'raw':''
    },

    'eva7':
    {
    'crypt':'',
    'raw':''
    },

    'eva8':
    {
    'crypt':'',
    'raw':''
    },

    'eva9':
    {
    'crypt':'',
    'raw':''
    },

    'eva10':
    {
    'crypt':'',
    'raw':''
    },

    'eva11':
    {
    'crypt':'',
    'raw':''
    },

    'eva12':
    {
    'crypt':'',
    'raw':''
    }

    }

}

#
IMPORT=1
EXPORT=2
GUI_IMPORT=3
GUI_EXPORT=4
GUI=5


err_UNKNOWN=-1
err_SYSERROR=-2
err_ERRORS=0
err_SUCCESS=1
err_RESTART=5
err_MULTISRCDST=6
err_NOCONNECT=7
err_NOFILES=8

err_TRUE=1
err_FALSE=0

errors={
    err_UNKNOWN:'Hеизвестная ошибка',
    err_ERRORS:'Ошибки при выполнении',
    err_SUCCESS:'Успешное завершение',
    err_RESTART:'Перезапуск выполнения',
    err_MULTISRCDST:'Hесколько источников и назначений',
    err_NOCONNECT:'MSSQL не запущен или нет связи',
    err_SYSERROR:'Системная ошибка',
    err_NOFILES:'Нет файлов с данными'
    }

runmodes={
    IMPORT:'import',
    EXPORT:'export',
    GUI_IMPORT:'gui_import',
    GUI_EXPORT:'gui_export',
    GUI:'gui'
    }

sections={
    'otexpimp':'OTExpImp',
    'import':'Import',
    'export':'Export'
    }

options={
    'shop':'OurList',
    'date_begin':'BeginDate',
    'date_end':'EndDate',
    'is_export':'IsExport',
    'date_from_ini':'ExportDates',
    'improot':'TempPath',
    'exproot':'TempPath',
    'sqlserver':'SQLServer',
    'sqldbname':'SQLDatabase',
    'sqlpwd':'SQLPwd',
    'sqluser':'SQLUser',
    'impfile':'ExportFile',
    'expfile':'ExportFile',
    'raiseerror':'RaiseError'
    }

erroractions={
    'Hевозможно':
    {
    'err_text': 'Ошибка при добавлении данных в базу',
    'err_send': err_TRUE,
    'err': err_ERRORS},
    'Прервано':
    {
    'err_text': 'Выполнение операции было остановлено вручную',
    'err_send': err_FALSE,
    'err': err_ERRORS},
    'Timeout':
    {
    'err_text': 'Выполнение операции было остановлено из-за истечения времения ожидания и будет перезапущено',
    'err_send': err_FALSE,
    'err': err_RESTART},
    'network':
    {
    'err_text': 'Выполнение операции было прервано из-за сетевой ошибки и будет перезапущено',
    'err_send': err_TRUE,
    'err': err_RESTART}
    }


_oldthreads=1

# Количество секунд "спячки" процесса для следующей проверки, если обнаружен блокированный файл
sleeptime=30

# Максимальное количество секунд "спячки" процесса, если обнаружен блокированный файл. После
# этого времение процесс завершит работу
maxsleeptime=1800
