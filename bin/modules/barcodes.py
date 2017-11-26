# -*- coding: cp1251 -*-
# Модуль штрихкодов
# Proposal: вид sql-файлов: imp-1-isql.sql, imp-2-bcp.sql imp-eva1-1-bcp.sql, exp-eva3-5-isql.sql
import cfg,os,sys,log,ini,impexp,threading,date,time,fileIO,string,misc,mailIO,reports

__desc__='Штрихкоды'
__runmodes__=[cfg.runmodes[cfg.IMPORT],cfg.runmodes[cfg.EXPORT],cfg.runmodes[cfg.GUI_IMPORT],cfg.runmodes[cfg.GUI_EXPORT]]
__version__='0.1'


class barcodes(reports.reports):
    
    def __init__(self):
        reports.reports.__init__(self)
        self.threads=[]
        self.__desc__=__desc__
        self.__runmodes__=__runmodes__
        self.__name__=__name__
        self.__version__=__version__        
        self.runmode=0
        self.date=''
        self.loglevel=3
        self.args=[]
        self.upload=0
        self.logf=None
        self.inif=None
        self.src_shop=''
        self.dst_shop=''        
        
    def prepare_ini(self):
        pass
    
    def _export(self,files):
        pass
    
    def _import(self,files):
        pass
    
    def start_import(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        pass
    
    def start_export(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        pass    
