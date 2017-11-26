# -*- coding: cp1251 -*-
# module for parsing and setting .INI files for stupid GMS OfficeTools

import os, sys, ConfigParser, log, cfg;

#__all__ =["IniFile"];

class IniFile(ConfigParser.ConfigParser):

    def __init__(self,logf):
        """ Init class """
        ConfigParser.ConfigParser.__init__(self)
        self.logf=logf
        
    def _log(self,logf,facility,logstr):
        """ Internal log wrapper"""
        self.logf.log(str(__name__),facility,logstr)
    
    def read_defaults(self,logf,defini=os.path.join(cfg.ini,'defaults.ini')):
        """ Read INI-file with defaults """
        self._log(self.logf,log.DEBUG,"В функции read_defaults ");        
        try:
            self.readfp(open(defini));
        except:
            self._log(self.logf,log.ERROR,"Ошибка чтения ["+os.path.join(cfg.ini,defini)+"]");
            self._log(self.logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
            self._log(self.logf,log.DEBUG,"Выход из функции read_defaults ");                        
            return 0;
        self._log(self.logf,log.DEBUG,"Выход из функции read_defaults ");            
        return 1;

    def read_ini(self,inifn=""):
        """ Read provided INI-file and get all options """
        self._log(self.logf,log.DEBUG,"В функции read_ini ");
        #self.read_defaults();
        self.inifn=inifn;
        try:
            self.read(self.inifn);
        except:
            self._log(self.logf,log.ERROR,"Ошибка чтения ["+self.inifn+"]");
            self._log(self.logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
            self._log(self.logf,log.DEBUG,"Выход из функции read_ini ");                        
            return -1;
        self._log(self.logf,log.DEBUG,"Выход из функции read_ini ");            
        return 0;
    
    def is_good_ini(self):
        """ Check is INI file is really from GMS Import/Export """
        self._log(self.logf,log.DEBUG,"В функции is_good_ini ");
        if ((self.has_section(cfg.sections['otexpimp'])==1)   and (self.has_section(cfg.sections['export'])==1)
            and (self.has_section(cfg.sections['import'])==1)):
            self._log(self.logf,log.DEBUG,"Выход из функции is_good_ini ");                                
            return 1
        else:
            self._log(self.logf,log.ERROR,"Ошибка структуры INI-файла ["+self.inifn+"]")
            self._log(self.logf,log.DEBUG,"Выход из функции is_good_ini ");                                
            return 0
                 
    def is_import_ini(self):
        """ Check is INI file is really for import """
        self._log(self.logf,log.DEBUG,"В функции is_import_ini ");                            
        if (self.is_good_ini()==1):
            result=self.getint(cfg.sections['otexpimp'],cfg.options['is_export'])
        else:
            self._log(self.logf,log.DEBUG,"Выход из функции is_import_ini ");                                        
            return -1
        if (result==1):
            self._log(self.logf,log.DEBUG,"Выход из функции is_import_ini ");                                                    
            return 1
        elif (result==0):
            self._log(self.logf,log.DEBUG,"Выход из функции is_import_ini ");                                                    
            return 0
        else:
            self._log(self.logf,log.ERROR,"Ошибка структуры INI-файла ["+self.inifn+"]. Hеизвестное значение IsExport: ["+str(result)+"]")
            self._log(self.logf,log.DEBUG,"Выход из функции is_import_ini ");                                                    
            return -2;
        
    def  is_export_ini(self):
        """ Check is INI file is really for export """
        self._log(self.logf,log.DEBUG,"В функции is_export_ini ");                            
        result=self.is_import_ini()
        if (result==1):
            self._log(self.logf,log.DEBUG,"Выход из функции is_export_ini ");                                                    
            return 0
        else:
            self._log(self.logf,log.DEBUG,"Выход из функции is_export_ini ");                                                    
            return 1
        
    def set_export(self):
        """ Set we are exporting """
        self._log(self.logf,log.DEBUG,"В функции set_export ");                                    
        self.set(cfg.sections['otexpimp'],cfg.options['is_export'],1)
        self._log(self.logf,log.DEBUG,"Выход из функции set_export ");
        
    def set_import(self):
        """ Set we are exporting """
        self._log(self.logf,log.DEBUG,"В функции set_import ");                                    
        self.set(cfg.sections['otexpimp'],cfg.options['is_export'],0)        
        self._log(self.logf,log.DEBUG,"Выход из функции set_import ");
        
    def set_shop(self,shop):
        """ Set shop code in option """
        self._log(self.logf,log.DEBUG,"В функции set_shop ");                                    
        try:
            self.set(cfg.sections['export'],cfg.options['shop'],shop)
            self.set(cfg.sections['import'],cfg.options['shop'],shop)
            # self.set(cfg.sections['export'],cfg.options['shops'],shop)
            # self.set(cfg.sections['import'],cfg.options['shops'],shop)            
        except:
            self._log(self.logf,log.ERROR,"Ошибка установки магазина ["+str(shop)+"]");
            self._log(self.logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
            self._log(self.logf,log.DEBUG,"Выход из функции set_shop ");                        
            return -1;
        self._log(self.logf,log.DEBUG,"Выход из функции set_shop ");
        return 0;

    def set_date_begin(self,date):
        """ Set begin date in option """
        self._log(self.logf,log.DEBUG,"В функции set_date_begin ");                                    
        try:
            self.set(cfg.sections['export'],cfg.options['date_begin'],date)
            self.set(cfg.sections['import'],cfg.options['date_begin'],date)
            self.set(cfg.sections['export'],cfg.options['date_from_ini'],0)
            self.set(cfg.sections['import'],cfg.options['date_from_ini'],1)                                    
        except:
            self._log(self.logf,log.ERROR,"Ошибка установки начальной даты ["+str(date)+"]");
            self._log(self.logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
            self._log(self.logf,log.DEBUG,"Выход из функции set_date_begin ");                        
            return -1;
        self._log(self.logf,log.DEBUG,"Выход из функции set_date_begin ");
        return 0;
    
    def set_date_end(self,date):
        """ Set end date  in option """
        self._log(self.logf,log.DEBUG,"В функции set_date_end ");                                    
        try:
            self.set(cfg.sections['export'],cfg.options['date_end'],str(date))
            self.set(cfg.sections['import'],cfg.options['date_end'],str(date))
            self.set(cfg.sections['export'],cfg.options['date_from_ini'],0)                                                
            self.set(cfg.sections['import'],cfg.options['date_from_ini'],1)                                                
        except:
            self._log(self.logf,log.ERROR,"Ошибка установки конечной даты ["+str(date)+"]");
            self._log(self.logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
            self._log(self.logf,log.DEBUG,"Выход из функции set_date_end ");                        
            return -1;
        self._log(self.logf,log.DEBUG,"Выход из функции set_date_end ");
        return 0;
