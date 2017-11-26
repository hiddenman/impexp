# -*- coding: cp1251 -*-
# log module
# TODO:
# Check for free space and switch to stdout(?)
# Сделать LOCK_EX и создавать временный лог, если занят
import sys,os,cfg,time,fileIO,tempfile,string,log,mailIO;


#__name__=['LogFile']

# const
ERROR=1
WARNING=2
INFO=3
DEBUG=4

errnames={
    1:'E',
    2:'W',
    3:'I',
    4:'D'
    }

class LogFile:
    def __init__(self):
        """ Init class """
        self.logfd=None
        self.loglevel=3
        self.errqueue=[]
    
    def _log(self,logstr):
        """ Internal put """
        self.logfd.writelines(str(time.strftime('%d/%m/%y %H:%M:%S '))+logstr+'\n')

    def _open(self):
        """ Temp log to stdout before opening real file """
        self.logfd=sys.stdout
        self.loglevel=3
        
    def open(self,fname,runmode,module):
        """ Open log file """
        #self.logfd=open(cfg.log+'/'+fname,'a+')
        #return 0
        self.logf_=LogFile()
        self.logf_._open()
        if (fileIO.dir_exists(os.path.join(cfg.log,runmode))==0):
            try:
                os.makedirs(os.path.join(cfg.log,runmode))
            except:
                self.logf_.log(str(__name__),ERROR,'Ошибка создания директорий ['+os.path.join(cfg.log,runmode)+']')
                self.logf_.log(str(__name__),ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
                sys.exit(-1)

        tmplog=0
        fname_=fname
        (self.logfd,self.result)=fileIO.open_file_lock(self.logf_,os.path.join(cfg.log,runmode,fname))
        if (self.result!=1):
            fname=fname+str('.')+str((string.split(tempfile.gettempprefix(),'.')[0]));
            (self.logfd,self.result)=fileIO.open_file_lock(self.logf_,os.path.join(cfg.log,runmode,fname))
            tmplog=1
        if (self.result!=1):
            self.logf_.log(str(__name__),ERROR,'Ошибка создания лог-файла ['+os.path.join(cfg.log,runmode,fname)+']')
            sys.exit(-1)
        self._log('I ['+str(__name__)+'.py]: Hачало работы '+str(module))
        self.logfd.flush()
        if (tmplog==1):
            self.log(str(__name__),ERROR,'Был обнаружен заблокированный лог-файл ['+str(os.path.join(cfg.log,runmode,fname_))+']')
            self.log(str(__name__),ERROR,'Создан временный лог-файл ['+str(os.path.join(cfg.log,runmode,fname))+']')
            
    def log(self,module,facility,logstr):
        """ Put string to logfile """
        if (facility==WARNING) or (facility==ERROR):
            self.errqueue.append(str(time.strftime('%d/%m/%y %H:%M:%S '))+str(errnames[facility])+' ['+module+'.py]: '+logstr+'\n')
        if (facility<=self.loglevel):
            self._log(str(errnames[facility])+' ['+module+'.py]: '+logstr)
            
    def setlevel(self,level):
        """ Set loglevel """
        self.loglevel=int(level)
        
    def close(self,module):
        """ Close log file """
        self._log('I ['+str(__name__)+'.py]: Завершение работы '+str(module))
        fileIO.close_file_lock(self.logf_,self.logfd)
        #self.logfd.close()
        # BUG
        # Трапаемся здесь. Хотя это же другой объект ;-/
        #self.logf_.logfd.close()
    

