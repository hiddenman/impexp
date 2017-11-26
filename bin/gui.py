# -*- coding: cp1251 -*-
# GUI модуль для запуска всех модулей.
# Грузить надо только .py, иначе оно подгружает и .pyc !
import os,sys,cfg,log,reports,imp,inspect,anygui,date,thread,threading,string

__desc__='ЦУП'
__runmodes__=[cfg.runmodes[cfg.GUI]]
__version__='0.1'

class gui(reports.reports):
    
    def __init__(self):
        reports.reports.__init__(self)        
        self.__desc__=__desc__
        self.__runmodes__=__runmodes__
        self.__name__=__name__
        self.__version__=__version__
        self.modules=[]
        self.modules_full=[]

    def load_modules(self):
        """ Load all modules """
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));        
        try:
            files=os.listdir(cfg.modules)
        except:
            self._log(log.ERROR,"Ошибка загрузки модулей")
            self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return 0
        for file_ in files:
            # BUG. Files like fuck.py.fuck.exe match this ;-)
            if ((string.count(file_,'.pyc')>=1) or (string.count(file_,'.py')==0)):
                continue
            file=string.split(file_,'.py')[0]
            (modfile,modname,moddesc)=imp.find_module(file)
            module=imp.load_module(file,modfile,modname,moddesc)
            # module_=eval('module.'+file+'()')            
            try:
                _desc=module.__desc__.decode(cfg.charset).encode(cfg.guicharset)
                _runmodes=module.__runmodes__
                _version=module.__version__
            except:
                self._log(log.ERROR,"Ошибка загрузки модуля [%s]"% str(file))
                self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
                continue
            else:
                entry={
                    __name__:file,
                    __desc__:_desc,
                    # __runmodes__:_runmodes,
                    __version__:_version
                    }
                self._log(log.INFO,"Загружен модуль [%s]" % str(module.__desc__))
                
            self.modules.append(_desc)
            self.modules_full.append(entry)
            
        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return 1

    def _gui(self):
        # WORKAROUND
        self.auto=-1
        self.runmode=-1
        self.module=''

        # if (self.runmode==cfg.GUI_IMPORT):
        #    self.runmode=cfg.IMPORT
        # else:
        #     self.runmode=cfg.EXPORT

        def start_pressed(event):
            if (self.module==''):
                label_error.text='Hе выбран модуль для запуска'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=1
                return 0
            if (self.src_shop==None):
                label_error.text='Hе задан магазин-источник'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=1
                return 0
            if (self.dst_shop==None):
                label_error.text='Hе задан магазин назначения'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=1
                return 0                
            if (self.auto==-1):
                label_error.text='Hе задан режим запуска'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=1
                return 0
            if (self.runmode==-1):
                label_error.text='Hе задана операция'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=1
                return 0                
            self.dates=text_dates.text
            if (self.dates==''):
                label_error.text='Hе задана ни одна дата'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=1
                return 0
            label_error.text=''
            label_error.visible=0

            self.oldlogf=self.logf
            self.oldloglevel=self.loglevel
            self.oldrunmode=self.runmode
            self.oldupload=self.upload
            self.oldauto=self.auto
            self.oldargs=self.args
            self.oldsrc_shop=self.src_shop
            self.olddst_shop=self.dst_shop


            (modfile,modname,moddesc)=imp.find_module(self.module)
            module=imp.load_module(self.module,modfile,modname,moddesc)                
            # thread_=threading.Thread()
            name=self.module
            module_=eval('module.'+name+'()')
            
            if (self.runmode==cfg.IMPORT):
                self._log(log.INFO,"Запуск новой нити импорта модуля ["+str(module.__desc__)+"] из магазина "+str(self.src_shop)+' в магазин '+str(self.dst_shop)+', даты '+str(self.dates)+' с аргументами '+str(self.args)+'')                                
                newthread=thread.start_new_thread(module_.start_import,(self.auto,self.runmode,self.upload,self.src_shop,self.dst_shop,self.dates,self.loglevel,self.args))                                            
            else:
                self._log(log.INFO,"Запуск новой нити экспорта модуля ["+str(module.__desc__)+"] из магазина "+str(self.src_shop)+' в магазин '+str(self.dst_shop)+', даты '+str(self.dates)+' с аргументами '+str(self.args)+'')                                
                newthread=thread.start_new_thread(module_.start_export,(self.auto,self.runmode,self.upload,self.src_shop,self.dst_shop,self.dates,self.loglevel,self.args))
                
            self.logf=self.oldlogf
            self.loglevel=self.oldloglevel
            self.runmode=self.oldrunmode
            self.upload=self.oldupload
            self.auto=self.oldauto
            self.args=self.oldargs
                
        def exit_pressed(event):
            gui.remove(window_main)
            gui._running=0
            return 0

        def dates_entered(event):
            # BUG
            # Почему-то не работает этот хандлер ;-(
            self.dates=text_dates.text

        def module_selected(event):
            for module_ in self.modules_full:
                if (self.modules[list_modules.selection]==module_[__desc__]):
                    self.module=module_[__name__]
                    break
            
        def shop_from_selected(event):
            self.src_shop=[]
            self.src_shop.append(cfg.shops.items()[list_shops_from.selection][0])
            
        def shop_to_selected(event):
            self.dst_shop=[]            
            self.dst_shop.append(cfg.shops.items()[list_shops_to.selection][0])

        def auto_selected(event):
            self.auto=1
            
        def export_selected(event):
            self.runmode=cfg.EXPORT
            
        def import_selected(event):
            self.runmode=cfg.IMPORT


        def manual_selected(event):
            self.auto=0
            
        gui = anygui.Application()
        window_main = anygui.Window(text=(self.__desc__.decode(cfg.charset).encode(cfg.guicharset)))            
            
        button_start = anygui.Button(text='Старт'.decode(cfg.charset).encode(cfg.guicharset))
        button_exit = anygui.Button(text='Выход'.decode(cfg.charset).encode(cfg.guicharset))

        group_auto=anygui.RadioGroup()
        
        group_runmode=anygui.RadioGroup()        

        radio_auto=anygui.RadioButton(text='Автоматически'.decode(cfg.charset).encode(cfg.guicharset))
        radio_manual=anygui.RadioButton(text='Вручную'.decode(cfg.charset).encode(cfg.guicharset))

        radio_export=anygui.RadioButton(text='Экспорт'.decode(cfg.charset).encode(cfg.guicharset))
        radio_import=anygui.RadioButton(text='Импорт'.decode(cfg.charset).encode(cfg.guicharset))

        group_auto.add([radio_auto,radio_manual])
        group_auto.selection=1
        self.auto=1

        group_runmode.add([radio_export,radio_import])
        group_runmode.selection=1
        self.runmode=cfg.EXPORT


        text_dates=anygui.TextField()
        text_dates.text=date.get_cur_date(self.logf)

        label_dates=anygui.Label(text='Даты'.decode(cfg.charset).encode(cfg.guicharset))
        label_direction=anygui.Label(text='из                          в'.decode(cfg.charset).encode(cfg.guicharset))        
        label_error=anygui.Label(text=''.decode(cfg.charset).encode(cfg.guicharset))
        label_error.visible=0

        list_shops_from=anygui.ListBox(items=cfg.shops)
        list_shops_to=anygui.ListBox(items=cfg.shops)        

        self.load_modules()

        list_modules=anygui.ListBox(items=self.modules)
        
        # window_main.add(label_runmode,left=10,top=5,hmove=0)

        # Список модулей
        window_main.add(list_modules,left=10,top=10)
        # Hадпись 'из в'
        window_main.add(label_direction,left=(list_modules,50),top=10,hmove=0)

        # Списки магазинов 'из' и 'в'
        window_main.add((list_shops_from,list_shops_to),direction='right',left=(list_modules,10),top=(label_direction,5),space=10)
        list_shops_from.height=list_modules.height
        list_shops_to.height=list_modules.height
        
        # Радиокнопки 'Автоматически' и 'Вручную'
        window_main.add((radio_auto,radio_manual),direction='down',left=(list_shops_to,10),top=10)
        

        # Радиокнопки 'Экспорт' и 'Импорт'        
        window_main.add((radio_export,radio_import),direction='down',left=10,top=(list_modules,20))


        window_main.add(label_dates,left=(radio_export,50),top=(list_shops_from,5))
        
        window_main.add(text_dates,left=(radio_export,10),top=(label_dates,10),hstretch=1)
        text_dates.width=list_shops_from.width+list_shops_to.width+10
        
        ## text_dates.width=(list_shops_to.right-10)
        
        window_main.add(button_start,left=10,top=(text_dates,10))
        window_main.add(button_exit,left=(button_start,10),top=(text_dates,10))

        window_main.add(label_error,left=(button_exit,10),top=(text_dates,15))


        
        window_main.width=radio_manual.right+20
        label_error.width=window_main.width
        label_direction.width=window_main.width        
        window_main.height=(button_exit.bottom+10)
        # label_runmode.left=int((window_main.width-len(label_runmode.text)-50)/2)
        
        anygui.link(button_start,'click',start_pressed)
        anygui.link(button_exit,'click',exit_pressed)
        anygui.link(list_modules,'select',module_selected)        
        anygui.link(list_shops_from,'select',shop_from_selected)
        anygui.link(list_shops_to,'select',shop_to_selected)        
        anygui.link(text_dates,'enterkey',dates_entered)
        anygui.link(radio_auto,auto_selected)
        anygui.link(radio_manual,manual_selected)
        anygui.link(radio_export,export_selected)
        anygui.link(radio_import,import_selected)        

        gui.add(window_main)
        gui.run()

        return 1


    

    def start_gui(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        self.loglevel=loglevel
        self.runmode=runmode
        self.upload=upload
        self.auto=auto
        self.args=args
        self.src_shop=src_shops
        self.dst_shop=dst_shops
        self.dates=dates
        self.do_archive=1        
        self.logf=self.init_module_log()        
        result=self._gui()
        self.send_module_log()            
        self.done_module_log()
        return result

    
    def start_module(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        """ Start current module """
        result=eval('self.start_'+cfg.runmodes[runmode])(auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args)
        return result
