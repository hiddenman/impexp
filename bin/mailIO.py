# -*- coding: cp1251 -*-
# mail I/O module
# модуль для сообщения об ошибках по e-mail
# при сборке py2exe выдает, что неизвестная кодировка cp1251 ;-/
import os,sys,cfg,log,string,smtplib,fileIO,email
from email import MIMEText,Charset,Encoders,MIMENonMultipart


def _log(logf,facility,logstr):
    """ Internal log wrapper """
    logf.log(str(__name__),facility,logstr)


def send_file(logf,path,subject=''):
    """ Send file to recepients from config file """
    (fd,result)=fileIO.open_file_read_bin(logf,path)
    if (result!=1):
        _log(logf,log.ERROR,"Ошибка отправки файла ["+str(path)+"] по e-mail")
        return -1
    try:
        text=fd.readlines()
        fd.close()
    except:
        pass
    send_message(logf,text,subject,'cp1251')
    return 1

def send_message(logf,text,subject='',codepage=cfg.wincharset):
    """ Send message to recepients from config file """
    # Hадо перекодировать сообщение в нужную кодировку из текущей
    email.Charset.CHARSETS['koi8-r']=(None,None,None)
    #email.Charset.CHARSETS['cp1251']=(None,None,None)    
    # BUG
    # надо тоже все на врапперы переносить
    if (len(text)==0):
        #_log(logf,log.ERROR,"Текст сообщения отсутствует: "+str(text))
        return 0
    # BUG
    # так и не работает правильно charset cp1251....fuck!
    msg=MIMEText.MIMEText(None,_charset=cfg.unixcharset)
    if (os.name=='nt'):
        try:
            msg['Subject']=subject.decode(cfg.wincharset).encode(cfg.unixcharset)
        except:
            msg['Subject']='['+str(__name__)+']: Ошибка перекодировки'
    else:
        msg['Subject']=subject
    msg['From']=cfg.emails['from']
    msg['To']=cfg.emails['to'][0]
    if (len(cfg.emails['to'])>=1):
        rcpts=''
        rcpts_=[]
        rcpts_.append(cfg.emails['to'][0])
        for rcpt in cfg.emails['to'][1:]:
            if (rcpts==''):
                rcpts=str(rcpt)
            else:
                rcpts=rcpts+','+str(rcpt)
            rcpts_.append(rcpt)
        msg['Cc']=rcpts
    if (os.name=='nt'):
        try:
            msg.set_payload(str(text[0].decode(codepage).encode(cfg.unixcharset)))
        except:
            msg.set_payload(str('['+str(__name__)+']: Ошибка перекодировки строки'.decode(codepage).encode(cfg.unixcharset)))
            
        for line in text[1:]:
            try:
                msg._payload=msg._payload+str(line).decode(codepage).encode(cfg.unixcharset)
            except:
                msg._payload=msg._payload+str('['+str(__name__)+']: Ошибка перекодировки строки'.decode(codepage).encode(cfg.unixcharset))
    else:
        msg.set_payload(str(text[0]))
        for line in text[1:]:
            msg._payload=msg._payload+str(line)
    srv=smtplib.SMTP()
    try:
        srv.connect(cfg.smtpserver)
    except:
        _log(logf,log.ERROR,"Ошибка соединения с smtp-сервером ["+str(cfg.smtpserver)+"]")
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return -1
    try:
        srv.sendmail(cfg.emails['from'],rcpts_,msg.as_string())
    except:
        _log(logf,log.ERROR,"Ошибка отправки сообщения через smtp-сервер ["+str(cfg.smtpserver)+"]")
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
    else:
        _log(logf,log.INFO,"Успешно отправлено сообщение для "+str(cfg.emails['to']))        
    srv.close()

