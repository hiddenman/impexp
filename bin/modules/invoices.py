# -*- coding: cp1251 -*-
# Модуль накладных
import cfg,reports

__desc__='Hакладные'
__runmodes__=[cfg.runmodes[cfg.IMPORT],cfg.runmodes[cfg.EXPORT],cfg.runmodes[cfg.GUI_IMPORT],cfg.runmodes[cfg.GUI_EXPORT]]
__version__='0.1'


class invoices(reports.reports):
    
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
