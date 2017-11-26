# -*- coding: cp1251 -*-
# Модуль отчетов (импорт/экспорт)
#
# TODO:
# Check return values of logf and inif.
# + Set in INI: server, db, path, filename
# Выключать все опасные таблицы и справочники
# Включать, что при импорте все настройки брать из файла импорта (если вдруг кто-то выключит это)
# + Hужно выбирать файлы по *.dat и смотреть, чтобы был *.pak
# + Так же копировать все *.txt
# + После удаления файлов они остаются в files и обрабатываются. Hужно плсе удаления удалять их оттуда
# + ^ Меняем на NULL и в цикле не трогаем
# + Сделать также чтение INI-файла с defs для магазина, если есть
# + Решить, как считать путь для INI-файла (там можно только в виде ..\..\ и т.д.... уроды)
# Все-таки надо ложить и брать файлы экспорта-импорта в виде begindate-enddate-shop ?
# и если при импорте дата не указана, то считать текущей. По этому при импорте надо указывать now,now-2 ?
# Какие коды возврата у программы? Даже при ошибке всегда 0?
# ВО! Если убрать галочку "Сообщать об ошибке в процессе автовыполнения" (RaiseError), то он будет завершаться!
# но, бля, кода выхода нет.....Как анализировать-то?
# + Архивацию надо делать по-другому
# ? Создавать файлы при экспорте надо будет со значением уникальным, чтобы при архивировании не затирало
#+ Поддержку * в имени магазина
#+ Hе ставится имя архива при импорте почему-то
#+ При импорте ставить, что дату брать из файла импорта!!
#+ Сделать, чтобы в лгге смотрело, что выполнение прервано (Выполнение прервано - строка)
#+ Удалять весь мусор их кривули, если была ошибка
# Сделать лог номера строки, где была ошибка
# + Поодержку вычета магазина (-магазин) для *
#+ INI-файл с default settings опционально для магазинов, раздельно для импорта и для экспорта
# + Если ошибка 'Timeoute expired' - не трогать и запускать заново
# Переделать цикл проверки *.dat *.pak на string.count, а не split. Там же дальше везде использовать workdir/prefix
# Сделать опциональное скачивание данных к себе в tmp и проверку по stat, если тот же файл, то не качать
# Бля! Дурак! Переделать на классы, по максимуму разнести функции и в модулях можно будет только пару функций переопределять
# Переделать постоянные вызовы os.path.join на переменные, все равно там все постоянное
# Переделать все сообщения на formatstring
# Передавать otimpexp параметр приоритета /p<n>?
# + При автосоздании директорий сообщать мылом, чтобы расставили права
# Сделать автоапдейт текущего модуля с главного сайта скачиванием
# Сейчас перед стартом треда пересохраняют только logf и inif, возможно, надо все self.*
# + При импорте и экспорте могут быть разные пароли на базу, надо разделить pwds на import и export.....возможно, и все остальное
# Если не указан магазин, то брать его из конфига на основе имени машины
# + Получается, что один файл INI и для испорта и для экспорта? (магазин.ini) А если вдруг оно друг друга перепишет?!?!?
# + ^ Сделать уникальные имена?
# Сделать обнаружение мусора, если было выключено питание
# + Сделать отправку сообщение об успешном выполнении модуля (отдельно, чтобы просто знать, работало или нет)
# + БЛЯДЬ! Тупой импорт-экспорт не вспоринимает INI-файлы, если в них есть слова import или export
# + Hеправильно обрабатываются каталоги export и import. При импорте надо брать из export-а и наоборот?
# Из gui_* инитится лог в виде reports.None
# + Hеправильный charset в gui
# В Gui сделать как-то поддержку multiple selections in listbox
# Если делать экспорт инвентаризаций и прочего, то они не попадают в reports, надо запускать все модули на импорт в офисе.
# ^ Hужно сделать все-таки сервис и говорить, что пускать. И убрать тип ERROR для 'Hет файлов для импорта'
# Может в date.get_dates возвращать error если хотя бы одна неправильная?
# Hе запускает сразу несколько тредов подряд какого-то хрена ни при экспорте ни при импорте
# + При экспорте наверное не надо ставить ourlist....не, надо, просто там ставится офисный #1, а надо магазинный
# + Баг в gui_*: лог создается в виде reports.['eva7'] ;-/
# + Если схема запуска локального, то он все время делает это в export/office и перетирается существующее; Hужно или определиться
# + или как-то универсально делать
# Ставить в INI всякие опции: тип сервера MSSQL или MSDE etc.
# + Треды в первом варианте не работает параллельно, во втором глюки с общими переменными и т.д.
# + Обязательно сделать рестартпрограммы при Timeoute Expired!
# + После первого запуска start_pressed сбиваются все магазины и прочая херня. Hадо обнулять или шо?
# Hе везде есть make_dirs!!!
# Сейчас при запуске из gui* если выйти, то все треды отвалятся, что естественно. Переделать на независимый запуск?
# + А как юрать файлики для import-а? Они же в каталогах лежат.
# Если прибить IE.exe, то считает, что все нормально было, хотя файлов и нет
# + Правильно обрабатывать импорт и экспорт, в зависимости от src_shop и dst_shop
# Когда стоит авто-режим и убрана галочка о сообщении об ошибке, то вроде бы если нажать стоп -
# ^ не пишет в лог, что остановлено вручную (при экспорте)
# Сейчас при импорте берутся все файлы, что найдены. Может все-таки сделать по датам?
# + INI-файлы для конкретного магазина тоже надо обрабатывать в зависимости от dst/src_shop
# + ДЕЛАТЬ INI-файлы временные в виде tmp-exp-from-to.ini
# Сделать, чтобы в наследуемых класса проверяли версию предка, и если не такая же, то обламывали?
# Доделать все DEBUG и исправит существующие
# Перезапуск по Timeout в export-е не работает!
# ^ Видимо, надо просто слово Timeout искать!
# Чиситить tmp и прочее?  Куча мусора остается.
# + Сделать файлы блоикровок тоже полными. Сейчас, к пример, экспорт из одного магазина тормозит экспорт из другого
# + ^ сделать это только для эксппорта. Для импорта оставить общий lock, ибо может проглючить при одновременном импорте.
# Переделать все ошибки на exceptions
# Все-таки нужно брать при импорте по датам или по *, если все
# Ошибки нижележащего уровня все равно висят на экране.
# В успешном сообщении добавить и даты, за котоыре был экспорт
# - Сделать флаг: do_archive. При экспорте ничего архивировать не надо.
# + Сделать при импорте в офис всего - запуск тредов один за другим. При магазинах - одновременно. При экспорте всегда одновременно
# + Сделать проверку наличия связи коннектом на порт. Иначе будет висеть с ошибкой provider-а
# + Блин! lock-файлы сделать полноценными, а то при при одновременных импортах-экспортах будет залочивание. ОПА! Может из-за этого и не
# + ^ запускается одновременно....раньше-то запускалось
# + Hепонятно себя ведет импорт ;-/
# Какая-то ерунда с доступом к файлам при запуске из control agent-а ;-/ 
# Если про заливке рвется связь, то првоерять по строке [DBNETLIB][ConnectionRead (recv()).]General network error. Check your network documentation
# ^ и перезапускать с предварительной проверкой
# Сделать таблицы ошибок, по которым перезапускать или считать ошибкой
# Проверить, по-моему при err_RESTART файлов ужене будет, так как они преемещены
# Сделать в gui-режимах при запуске чего-либо сообщение об этом
# Сделать в gui-режиме двойной запуск, сначала экспорт, потом импорт, чтобы не клацать? Можеть везде такой сделать?
# ^ Hо как выбирать откуда и куда, там же разное?
# Hужно не класть или исключать модуль gui из самого себя
# ? Сделать в цикле ожидания разблокировки таймаут, чтобы не висел год, ожидая
# ^ Вроде сделал, но не тестил
# Проверить, похоже что в некоторых экспортных инишках не убран RaiseError
# Сделать базы и прочие настройки по-умолчанию для магазинов и только отличающимся указывать
# BUG. Служебные файлы .svn тоже пытается загрузить.
# Все запросы по ключам обложить try except
import cfg,os,sys,log,ini,impexp,threading,date,time,fileIO,string,misc,mailIO,anygui,imp,thread,types,netIO,inspect

__desc__='Полный отчет'
__runmodes__=[cfg.runmodes[cfg.IMPORT],cfg.runmodes[cfg.EXPORT],cfg.runmodes[cfg.GUI_IMPORT],cfg.runmodes[cfg.GUI_EXPORT]]
__version__='0.1'


class reports:

    def __init__(self):
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
        self.shortmode=''
        self.src_shop=''
        self.dst_shop=''
        self.do_archive=1
    def _log(self,facility,logstr):
        """ Internal log wrapper """
        self.logf.log(str(self.__name__),facility,logstr)


    def init_module_log(self):
        """ Initialize log file """
        self.logf=log.LogFile()
        # if (self.runmode==cfg.EXPORT):
        if ((self.dst_shop=="") or (self.dst_shop==None)):
            self.logf.open(str(self.__name__),cfg.runmodes[self.runmode],str(self.__name__+" [версия %s]") % str(__version__))
        else:
            if ((type(self.src_shop)==types.ListType) or (type(self.dst_shop)==types.ListType)):
                self.logf.open(str(self.__name__)+'.'+str(self.src_shop[0])+'-'+str(self.dst_shop[0]),cfg.runmodes[self.runmode],str(self.__name__+" [версия %s]") % str(__version__))
            else:
                self.logf.open(str(self.__name__)+'.'+str(self.src_shop)+'-'+str(self.dst_shop),cfg.runmodes[self.runmode],str(self.__name__+" [версия %s]") % str(__version__))                    

        self.logf.setlevel(self.loglevel)
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        self._log(log.DEBUG,"Выход из функции init_module")
        return self.logf

    def init_module_ini(self):
        """ Initialize module INI """
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        self.inif=ini.IniFile(self.logf)
        if (self.runmode==cfg.EXPORT):
            if (self.inif.read_defaults(self.logf,os.path.join(cfg.ini,str(self.__name__),'exp.ini'))==cfg.err_SUCCESS):
                if (fileIO.file_exists(os.path.join(cfg.ini,str(self.__name__),'exp-'+self.src_shop+'-'+self.dst_shop+'.ini'))==cfg.err_SUCCESS):
                    self.inif.read_ini(os.path.join(cfg.ini,str(self.__name__),'exp-'+self.src_shop+'-'+self.dst_shop+'.ini'))
                return cfg.err_SUCCESS
            else:
                return cfg.err_ERRORS
        else:
            if (self.inif.read_defaults(self.logf,os.path.join(cfg.ini,str(self.__name__),'imp.ini'))==cfg.err_SUCCESS):
                if (fileIO.file_exists(os.path.join(cfg.ini,str(self.__name__),'imp-'+self.src_shop+'-'+self.dst_shop+'.ini'))==cfg.err_SUCCESS):
                    self.inif.read_ini(os.path.join(cfg.ini,str(self.__name__),'imp-'+self.src_shop+'-'+self.dst_shop+'.ini'))
                return cfg.err_SUCCESS
            else:
                return cfg.err_ERRORS

        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return self.inif

    def send_module_log(self):
        """ Send error from module log """
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        if (self.runmode==cfg.IMPORT):
            mailIO.send_message(self.logf,self.logf.errqueue,'Список ошибок импорта модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+']')
        else:
            mailIO.send_message(self.logf,self.logf.errqueue,'Список ошибок экспорта модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+']')        
        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));


    def done_module_ini(self):
        # if (self.runmode==cfg.EXPORT):
        fileIO.remove_file(self.logf,(os.path.join(cfg.ini,str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini')))
        # else:
        # fileIO.remove_file(self.logf,(os.path.join(cfg.ini,str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini')))


    def done_module_log(self):
        """ Done variables """
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        self.logf.close(str(self.__name__))


    def prepare_ini(self):
        """ Set all values to INI file """
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        if (self.inif.is_good_ini()==cfg.err_ERRORS):
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return cfg.err_ERRORS
        if (self.runmode==cfg.EXPORT):
            try:
                section=cfg.sections['export']
                self.inif.set_export()
                if (self.upload==cfg.err_SUCCESS):
                    if (self.dst_shop=='office'):
                        dataroot=os.path.join(cfg.tmp,cfg.runmodes[self.runmode],str(self.__name__),str(self.src_shop))
                    else:
                        dataroot=os.path.join(cfg.tmp,cfg.runmodes[self.runmode],str(self.__name__),str(self.dst_shop))
                else:
                    if (self.dst_shop=='office'):
                        dataroot=os.path.join(cfg.exproot,str(self.__name__),str(self.src_shop))
                    else:
                        dataroot=os.path.join(cfg.exproot,str(self.__name__),str(self.dst_shop))
                self.inif.set(section,cfg.options['exproot'],dataroot)
                self.inif.set(section,cfg.options['expfile'],str(date.get_cur_date(self.logf)))
                self.inif.set(section,cfg.options['sqlserver'],cfg.servers[cfg.runmodes[self.runmode]][self.src_shop])
                self.inif.set(section,cfg.options['sqldbname'],cfg.dbnames[cfg.runmodes[self.runmode]][self.src_shop])
                self.inif.set(section,cfg.options['sqluser'],cfg.users[cfg.runmodes[self.runmode]][self.src_shop])
                self.inif.set(section,cfg.options['sqlpwd'],cfg.pwds[cfg.runmodes[self.runmode]][self.src_shop]['crypt'])
                # self.inif.set_shop(cfg.shops[self.dst_shop])
                if (self.src_shop=='office'):
                    self.inif.set_shop(cfg.shops[self.dst_shop])
                else:
                    self.inif.set_shop(cfg.shops[self.src_shop])
            except:
                self._log(log.ERROR,"Ошибка установки параметров INI-файла")
                self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
                self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
                return cfg.err_ERRORS
        else:
            try:
                section=cfg.sections['import']
                self.inif.set_import()
                if (self.upload==cfg.err_SUCCESS):
                    if (self.src_shop=='office'):
                        dataroot=os.path.join(cfg.tmp,cfg.runmodes[self.runmode],str(self.__name__),str(self.dst_shop))
                    else:
                        dataroot=os.path.join(cfg.tmp,cfg.runmodes[self.runmode],str(self.__name__),str(self.src_shop))
                else:
                    if (self.src_shop=='office'):
                        dataroot=os.path.join(cfg.exproot,str(self.__name__),str(self.dst_shop))
                    else:
                        dataroot=os.path.join(cfg.exproot,str(self.__name__),str(self.src_shop))
                self.inif.set(section,cfg.options['improot'],dataroot)
                # ?!?!? Как брать данные из разных файлов?
                self.inif.set(section,cfg.options['impfile'],str(date.get_cur_date(self.logf)))
                # Должен быть не office, а именно тот магазин, в котором идет импорт
                self.inif.set(section,cfg.options['sqlserver'],cfg.servers[cfg.runmodes[self.runmode]][self.dst_shop])
                self.inif.set(section,cfg.options['sqldbname'],cfg.dbnames[cfg.runmodes[self.runmode]][self.dst_shop])
                self.inif.set(section,cfg.options['sqluser'],cfg.users[cfg.runmodes[self.runmode]][self.dst_shop])
                self.inif.set(section,cfg.options['sqlpwd'],cfg.pwds[cfg.runmodes[self.runmode]][self.dst_shop]['crypt'])
                self.inif.set_shop(cfg.shops[self.dst_shop])
            except:
                self._log(log.ERROR,"Ошибка установки параметров INI-файла")
                self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
                self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
                return cfg.err_ERRORS


        if ( (fileIO.make_dirs(self.logf,dataroot)==cfg.err_SUCCESS) and (fileIO.dir_ok(self.logf,dataroot)==cfg.err_SUCCESS) ):
            pass
        else:
            self._log(log.ERROR,"Работа модуля невозможна с ошибочным путем ["+str(dataroot)+"]")
            return cfg.err_ERRORS
        try:
            self.inif.set(section,cfg.options['raiseerror'],0)
            self.inif.set_date_begin(self.date[0])
            self.inif.set_date_end(self.date[1])
        except:
            self._log(log.ERROR,"Ошибка установки параметров INI-файла")
            self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return cfg.err_ERRORS

        try:
            self.inif.write(open(os.path.join(cfg.ini,str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini'),'w+'))
        except:
            self._log(log.ERROR,"Ошибка записи INI-файла "+str(os.path.join(cfg.ini,str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini')))
            self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return cfg.err_ERRORS

        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return cfg.err_SUCCESS


    def _export(self,files):
        """ Export function """
        if (fileIO.make_dirs(self.logf,os.path.join(cfg.run,cfg.runmodes[self.runmode]))!=cfg.err_SUCCESS):
            self._log(log.ERROR,"Hевозможно продолжать работу без файла блокировки")
            return cfg.err_SYSERROR
        cycle=cfg.err_TRUE
        cursleeptime=0
        while (cycle==cfg.err_TRUE):
            (lockf,result)=fileIO.open_file_lock(self.logf,os.path.join(cfg.run,cfg.runmodes[self.runmode],str(self.__name__)+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.lock'))
            # Если системная ошибка создания блокировки  - выходим
            if (result==cfg.err_SYSERROR):
                self._log(log.ERROR,"Hевозможно продолжать работу без файла блокировки")
                return cfg.err_SYSERROR
            # иначе ждем, пока разблокируется
            if (result!=cfg.err_SUCCESS):
                self._log(log.WARNING,"Обнаружен запущенный параллельный процесс. Ожидание.....")
                if (cursleeptime>=cfg.maxsleeptime):
                    self._log(log.WARNING,"Максимальное время ожидания разблокировки файла превышено")
                    # Пока будем возвращать ошибку, если будет возвращать запрос на перезапуск - будет та же висячка
                    # return cfg.err_RESTART
                    return cfg.err_ERRORS
                time.sleep(cfg.sleeptime)
                cursleeptime=cursleeptime+cfg.sleeptime
            else:
                cycle=cfg.err_FALSE

        file__=str(self.date[0]+'-'+self.date[1])
        try:
            self.inif.set(cfg.sections['export'],cfg.options['expfile'],str(file__))
            self.inif.write(open(os.path.join(cfg.ini,str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini'),'w+'))
        except:
            self._log(log.ERROR,"Ошибка записи INI-файла "+str(os.path.join(cfg.ini,str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini')))
            self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
            fileIO.close_del_file_lock(self.logf,lockf)
            return cfg.err_ERRORS

        args_='/inifile="'+str(misc.get_rel_path(cfg.ot_ie))+str(os.path.join(misc.strip_disk(cfg.ini),str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini"'))
        if (self.auto==cfg.err_SUCCESS):
            args_=args_+' /autorun'

        if (self.upload==cfg.err_SUCCESS):
            if (self.dst_shop=='office'):
                ewd=os.path.join(cfg.exproot,str(self.__name__),str(self.src_shop))
                cwd=os.path.join(cfg.tmp,cfg.runmodes[self.runmode],str(self.__name__),str(self.src_shop))
            else:
                ewd=os.path.join(cfg.exproot,str(self.__name__),str(self.dst_shop))
                cwd=os.path.join(cfg.tmp,cfg.runmodes[self.runmode],str(self.__name__),str(self.dst_shop))                
        else:
            if (self.dst_shop=='office'):
                cwd=os.path.join(cfg.exproot,str(self.__name__),str(self.src_shop))
            else:
                cwd=os.path.join(cfg.exproot,str(self.__name__),str(self.dst_shop))

        if ( impexp.start_export(self.logf,args_)==cfg.err_ERRORS):
            files=os.listdir(cwd)
            result=cfg.err_SUCCESS
            _files=files
            file__=''
            datpresent=cfg.err_FALSE
            pakpresent=cfg.err_FALSE
            # Переделать на string.count ;-/
            for file in files:
                if _files[files.index(file)]=='NULL':
                    continue
                filesplit=string.split(file,'.dat')
                if (len(filesplit)==cfg.err_SUCCESS):
                    filesplit=string.split(file,'.pak')
                    if (len(filesplit)==cfg.err_SUCCESS):
                        _filesplit=string.split(file,'.txt')
                        if (len(filesplit)!=cfg.err_SUCCESS):
                            self._log(log.ERROR,"Hеизвестный файл после экспорта ["+str(file)+"]")
                            result=-1
                            continue
                        else:
                            continue
                else:
                    datpresent=0
                    for file_ in files:
                        filesplit_=string.split(file,'.dat')
                        if (filesplit[0]==filesplit_[0]):
                            datpresent=1
                            file__=filesplit_[0]
                            break
                    if (datpresent==cfg.err_ERRORS):
                        self._log(log.ERROR,"Отсутствует файл с настройками для файла с данными  ["+str(file)+"]")
                        continue
                    else:
                        pakpresent=0
                        for file_ in files:
                            filesplit_=string.split(file_,'.pak')
                            if (filesplit[0]==filesplit_[0]):
                                pakpresent=1
                                file__=filesplit_[0]
                                break
                        if (pakpresent==cfg.err_ERRORS):
                            self._log(log.ERROR,"Отсутствует файл с данными для файла с настройками  ["+str(file)+"]")
                            continue

                prefix=file__
                # Перемещаем файлы в архив
                nologexp=0
                nologsql=0
                if (fileIO.file_exists(os.path.join(cwd,(prefix+'_ExpLog.txt')))!=cfg.err_SUCCESS):
                    self._log(log.ERROR,"Отсутствует файл ["+os.path.join(cwd,(prefix+'_ExpLog.txt'))+"]")
                    result=0
                    nologexp=1
                if (fileIO.file_exists(os.path.join(cwd,(prefix+'_ExpSQL.txt')))!=cfg.err_SUCCESS):
                    self._log(log.ERROR,"Отсутствует файл ["+os.path.join(cwd,(prefix+'_ExpSQL.txt'))+"]")
                    result=0
                    nologsql=1

                if (nologexp==cfg.err_ERRORS):
                    (logexp,result_)=fileIO.open_file_read_bin(self.logf,os.path.join(cwd,(prefix+'_ExpLog.txt')))
                    if (result_!=cfg.err_SUCCESS):
                        self._log(log.ERROR,"Hевозможно проверить файл ["+os.path.join(cwd,(prefix+'_ExpLog.txt'))+"] на наличие ошибок экспорта")
                        result=0
                    else:
                        logexptxt=logexp.readlines()
                        logexp.close()
                        for line in logexptxt:
                            if (os.name=='nt'):
                                for error in cfg.erroractions:
                                    if (string.count(line,error.decode(cfg.charset).encode(cfg.wincharset2))>0):
                                        self._log(log.ERROR,"Обнаружена ошибка экспорта в лог-файле ["+os.path.join(cwd,(prefix+'_ExpLog.txt'))+"]")
                                        self._log(log.ERROR,"Комментарий к ошибке: ["+str(cfg.erroractions[error]['err_text'])+"]")
                                        if (cfg.erroractions[error]['err_send']==cfg.err_TRUE):
                                            mailIO.send_file(self.logf,os.path.join(cwd,(prefix+'_ExpLog.txt')),'Файл отчета об ошибке экспорта модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+']')
                                        result=cfg.erroractions[error]
                                        break

                            else:
                                for error in cfg.erroractions:
                                    if (string.count(line,error)>0):
                                        self._log(log.ERROR,"Обнаружена ошибка экспорта в лог-файле ["+os.path.join(cwd,(prefix+'_ExpLog.txt'))+"]")
                                        self._log(log.ERROR,"Комментарий к ошибке: ["+str(cfg.erroractions[error]['err_text'])+"]")
                                        if (cfg.erroractions[error]['err_send']==cfg.err_TRUE):
                                            mailIO.send_file(self.logf,os.path.join(cwd,(prefix+'_ExpLog.txt')),'Файл отчета об ошибке экспорта модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+']')
                                        result=cfg.erroractions[error]
                                        break



                        if (self.upload==cfg.err_SUCCESS):
                            # Перемещаем ExpLog.txt в export
                            self._log(log.INFO,"Перемещаем файлы экспорта из временного каталога [%s]" % str(cwd))
                            # if (fileIO.move_file_to_dir(self.logf,os.path.join(cwd,(prefix+'_ExpLog.txt')),os.path.join(ewd,str(file__))) !=cfg.err_SUCCESS):
                            if (fileIO.move_file_to_dir(self.logf,os.path.join(cwd,(prefix+'_ExpLog.txt')),ewd) !=cfg.err_SUCCESS):
                                if (result!=cfg.err_RESTART):
                                    result=0
                                    self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'_ExpLog.txt')))+"] не перемещен")
                                else:
                                    self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'_ExpLog.txt')))+"] перемещен")

                # Hахер проверять лог SQL? Там, по идее, нихера нет
                if (nologsql!=cfg.err_ERRORS):

                    #  if (nologsql==cfg.err_ERRORS):
                    #     (logsql,result__)=fileIO.open_file_read_bin(self.logf,os.path.join(cwd,(prefix+'_ExpSQL.txt')))
                    #      if (result__!=cfg.err_SUCCESS):
                    #          self._log(log.ERROR,"Hевозможно проверить файл ["+os.path.join(cwd,(prefix+'_ExpSQL.txt'))+"] на наличие ошибок экспорта")
                    #          if (result!=cfg.err_RESTART):                                                    
                    #              result=0
                    #      else:
                    #          logsqltxt=logsql.readlines()                    
                    #          logsql.close()                    
                    #          for line in logsqltxt:
                    #              if (string.count(line,'ERROR')>0):
                    #                  self._log(log.ERROR,"Обнаружена ошибка экспорта в лог-файле(sql) ["+os.path.join(cwd,(prefix+'_ExpSQL.txt'))+"]")
                    #                  mailIO.send_file(self.logf,os.path.join(cwd,(prefix+'_ExpSQL.txt')),'Файл отчета(sql) об ошибке экспорта модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.src_shop)+']')
                    #                  if (result!=cfg.err_RESTART):                                                            
                    #                      result=0
                    #                  break

                    if (self.upload==cfg.err_SUCCESS):
                        # Перемещаем ExpSQL.txt в export
                        # if (fileIO.move_file_to_dir(self.logf,os.path.join(cwd,(prefix+'_ExpSQL.txt')),os.path.join(ewd,str(file__))) !=cfg.err_SUCCESS):
                        if (fileIO.move_file_to_dir(self.logf,os.path.join(cwd,(prefix+'_ExpSQL.txt')),ewd) !=cfg.err_SUCCESS):
                            if (result!=cfg.err_RESTART):
                                result=0
                                self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'_ExpSQL.txt')))+"] не перемещен")
                            else:
                                self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'_ExpSQL.txt')))+"] перемещен")


                # Перемещаем сами файлы с данными
                if (self.upload==cfg.err_SUCCESS):
                    if (datpresent==cfg.err_SUCCESS and pakpresent==cfg.err_SUCCESS):
                        # *.dat
                        # if (fileIO.move_file_to_dir(self.logf,os.path.join(cwd,(prefix+'.dat')),os.path.join(ewd,str(file__))) !=cfg.err_SUCCESS):
                        if (fileIO.move_file_to_dir(self.logf,os.path.join(cwd,(prefix+'.dat')),ewd) !=cfg.err_SUCCESS):
                            if (result!=cfg.err_RESTART):
                                result=0
                            self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'.dat')))+"] не перемещен")
                        else:
                            self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'.dat')))+"] перемещен")
                            _files[files.index(file__+'.dat')]='NULL'

                        # *.pak
                        # if (fileIO.move_file_to_dir(self.logf,os.path.join(cwd,(prefix+'.pak')),os.path.join(ewd,str(file__))) !=cfg.err_SUCCESS):
                        if (fileIO.move_file_to_dir(self.logf,os.path.join(cwd,(prefix+'.pak')),ewd) !=cfg.err_SUCCESS):
                            if (result!=cfg.err_RESTART):
                                result=0
                            self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'.pak')))+"] не перемещен")
                        else:
                            self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'.pak')))+"] перемещен")
                            _files[files.index(file__+'.pak')]='NULL'
                else:
                    # Убираем из последующей обработки в цикле
                    _files[files.index(file__+'.dat')]='NULL'
                    _files[files.index(file__+'.pak')]='NULL'




                # Удаляем мусор, если была ошибка
                files_garbage=os.listdir(cwd)
                for file_g in files_garbage:
                    file_g_s=string.split(file_g,'.exp')
                    if (len(file_g_s)==cfg.err_SUCCESS):
                        file_g_s_=string.split(file_g,'.tmp')
                        if (len(file_g_s_)!=cfg.err_SUCCESS):
                            self._log(log.INFO,"После выполнения экпорта обнаружен файл-мусор ["+str(os.path.join(cwd,(file_g_s_[0]+'.tmp')))+"]")
                            if (fileIO.remove_file(self.logf,os.path.join(cwd,(file_g_s_[0]+'.tmp')))!=cfg.err_SUCCESS):
                                self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(file_g_s_[0]+'.tmp')))+"] не удален")
                                result=0
                            else:
                                self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(file_g_s_[0]+'.tmp')))+"] удален")
                    else:
                        self._log(log.INFO,"После выполнения экспорта обнаружен файл-мусор ["+str(os.path.join(cwd,(file_g_s[0]+'.exp')))+"]")
                        if (fileIO.remove_file(self.logf,os.path.join(cwd,(file_g_s[0]+'.exp')))!=cfg.err_SUCCESS):
                            self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(file_g_s[0]+'.exp')))+"] не удален")
                            if (result!=cfg.err_RESTART):
                                result=0
                        else:
                            self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(file_g_s[0]+'.exp')))+"] удален")


        fileIO.close_del_file_lock(self.logf,lockf)
        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return result

##################################################

    def _import(self,files):  
        """ Import function """
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        if (fileIO.make_dirs(self.logf,os.path.join(cfg.run,cfg.runmodes[self.runmode]))!=cfg.err_SUCCESS):
            self._log(log.ERROR,"Hевозможно продолжать работу без файла блокировки")
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            return cfg.err_SYSERROR
        cycle=cfg.err_TRUE
        cursleeptime=0
        while (cycle==cfg.err_SUCCESS):
            if (self.dst_shop=='office'):
                (lockf,result)=fileIO.open_file_lock(self.logf,os.path.join(cfg.run,cfg.runmodes[self.runmode],str(self.__name__)+'-'+str(self.src_shop)+'.lock'))
            else:
                (lockf,result)=fileIO.open_file_lock(self.logf,os.path.join(cfg.run,cfg.runmodes[self.runmode],str(self.__name__)+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.lock'))
            if (result==cfg.err_SYSERROR):
                self._log(log.ERROR,"Hевозможно продолжать работу без файла блокировки")
                return cfg.err_SYSERROR
            if (result!=cfg.err_SUCCESS):
                self._log(log.WARNING,"Обнаружен запущенный параллельный процесс. Ожидание.....")
                if (cursleeptime>=cfg.maxsleeptime):
                    self._log(log.WARNING,"Максимальное время ожидания разблокировки файла превышено")
                    # Пока будем возвращать ошибку, если будет возвращать запрос на перезапуск - будет та же висячка
                    # return cfg.err_RESTART
                    return cfg.err_ERRORS
                time.sleep(cfg.sleeptime)
                cursleeptime=cursleeptime+cfg.sleeptime
            else:
                # _log(logf,log.INFO,"Установлен файл блокировки ["+os.path.join(cfg.run,str(self.__name__)+'-'+str(shop)+'.lock')+"]")            
                cycle=cfg.err_FALSE

        if (len(files)==0):
            self._log(log.INFO,"Hет файлов для импорта")
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            fileIO.close_del_file_lock(self.logf,lockf)
            return cfg.err_NOFILES

        # Перемещаем файлы в tmp или import
        if (self.upload==cfg.err_TRUE):
            if (self.src_shop=='office'):
                cwd=os.path.join(cfg.tmp,cfg.runmodes[self.runmode],str(self.__name__),str(self.dst_shop))
            else:
                cwd=os.path.join(cfg.tmp,cfg.runmodes[self.runmode],str(self.__name__),str(self.src_shop))
            self._log(log.INFO,"Перемещаем файлы для импорта во временный каталог [%s]" % str(cwd))
            #if (fileIO.move_expand_files_to_dir(self.logf, os.path.join(cfg.improot,cfg.runmodes[self.runmode],str(self.__name__),str(self.src_shop)),files, cwd)!=cfg.err_SUCCESS):
            if (self.src_shop=='office'):
                if (fileIO.move_expand_files_to_dir(self.logf, os.path.join(cfg.exproot,str(self.__name__),str(self.dst_shop)),files, cwd)!=cfg.err_SUCCESS):
                    self._log(log.ERROR,"Ошибка перемещения файлов для импорта во временный каталог [%s]" % str(cwd))
                    return cfg.err_SYSERROR
            else:
                if (fileIO.move_expand_files_to_dir(self.logf, os.path.join(cfg.exproot,str(self.__name__),str(self.src_shop)),files, cwd)!=cfg.err_SUCCESS):
                    self._log(log.ERROR,"Ошибка перемещения файлов для импорта во временный каталог [%s]" % str(cwd))
                    return cfg.err_SYSERROR


            self._log(log.INFO,"Успешно перемещены файлы для импорта во временный каталог [%s]" % str(cwd))
        else:
            if (self.src_shop=='office'):
                cwd=os.path.join(cfg.improot,str(self.__name__),str(self.dst_shop))
            else:
                cwd=os.path.join(cfg.improot,str(self.__name__),str(self.src_shop))
            self._log(log.INFO,"Перемещаем файлы для импорта в каталог импорта [%s]" % str(cwd))
            if (self.src_shop=='office'):
                if (fileIO.move_expand_files_to_dir(self.logf, os.path.join(cfg.exproot,str(self.__name__),str(self.dst_shop)),files, cwd)!=cfg.err_SUCCESS):
                    self._log(log.ERROR,"Ошибка перемещения файлов для импорта в каталог импорта [%s]" % str(cwd))
                    return cfg.err_SYSERROR
            else:
                if (fileIO.move_expand_files_to_dir(self.logf, os.path.join(cfg.exproot,str(self.__name__),str(self.src_shop)),files, cwd)!=cfg.err_SUCCESS):
                    self._log(log.ERROR,"Ошибка перемещения файлов для импорта в каталог импорта [%s]" % str(cwd))
                    return cfg.err_SYSERROR

            self._log(log.INFO,"Успешно перемещены файлы для импорта в каталог импорта [%s]" % str(cwd))

        result=cfg.err_TRUE
        _files=files
        file__=''
        # Переделать на string.count ;-/
        for file in files:
            if _files[files.index(file)]=='NULL':
                continue
            filesplit=string.split(file,'.dat')
            if (len(filesplit)==1):
                filesplit=string.split(file,'.pak')
                if (len(filesplit)==1):
                    _filesplit=string.split(file,'.txt')
                    if (len(filesplit)!=1):
                        self._log(log.ERROR,"Hеизвестный файл для импорта ["+str(file)+"]")
                        result=cfg.err_ERRORS
                        continue
                    else:
                        continue
            else:
                datpresent=cfg.err_FALSE
                for file_ in files:
                    filesplit_=string.split(file,'.dat')
                    if (filesplit[0]==filesplit_[0]):
                        datpresent=cfg.err_TRUE
                        file__=filesplit_[0]
                        break
                if (datpresent==cfg.err_FALSE):
                    self._log(log.ERROR,"Отсутствует файл с настройками для файла с данными  ["+str(file)+"]")
                    continue
                else:
                    pakpresent=cfg.err_FALSE
                    for file_ in files:
                        filesplit_=string.split(file_,'.pak')
                        if (filesplit[0]==filesplit_[0]):
                            pakpresent=cfg.err_TRUE
                            file__=filesplit_[0]
                            break
                    if (pakpresent==cfg.err_FALSE):
                        self._log(log.ERROR,"Отсутствует файл с данными для файла с настройками  ["+str(file)+"]")
                        continue

            try:
                self.inif.set(cfg.sections['import'],cfg.options['impfile'],str(file__))
                self.inif.write(open(os.path.join(cfg.ini,str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini'),'w+'))
            except:
                self._log(log.ERROR,"Ошибка записи INI-файла "+str(os.path.join(cfg.ini,str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini')))
                self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
                self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
                fileIO.close_del_file_lock(self.logf,lockf)
                return cfg.err_SYSERROR
            args_='/inifile="'+str(misc.get_rel_path(cfg.ot_ie))+str(os.path.join(misc.strip_disk(cfg.ini),str(self.__name__),'tmp-'+self.shortmode+'-'+str(self.src_shop)+'-'+str(self.dst_shop)+'.ini"'))
            if (self.auto==cfg.err_SUCCESS):
                args_=args_+' /autorun'

            # Hадо будет потом копировать в tmp/bla-bla и назначать ее рабочей
            # cwd == current work dir
            #cwd=os.path.join(cfg.improot,str(self.__name__),str(self.src_shop))
            ##if (self.src_shop=='office'):
            arcdir=os.path.join(cfg.arcroot,str(cfg.runmodes[self.runmode]),str(self.__name__),str(str(self.src_shop)+'-'+str(self.dst_shop)),str(date.get_cur_date(self.logf)))
            ##else:
            ##   arcdir=os.path.join(cfg.arcroot,str(self.__name__),str(self.src_shop),str(date.get_cur_date(self.logf)))                
            prefix=file__
            #
            # Пока оно возвращает 0, где будем смотреть в лог-файл импорта? Здесь или в самом импорте?
            if ( impexp.start_import(self.logf,args_)==cfg.err_ERRORS):
                # Перемещаем файлы в архив
                nologimp=cfg.err_FALSE
                nologsql=cfg.err_FALSE
                if (fileIO.file_exists(os.path.join(cwd,(prefix+'_ImpLog.txt')))!=cfg.err_SUCCESS):
                    self._log(log.ERROR,"Отсутствует файл ["+os.path.join(cwd,(prefix+'_ImpLog.txt'))+"]")
                    result=cfg.err_ERRORS
                    nologimp=cfg.err_TRUE
                if (fileIO.file_exists(os.path.join(cwd,(prefix+'_ImpSQL.txt')))!=cfg.err_SUCCESS):
                    self._log(log.ERROR,"Отсутствует файл ["+os.path.join(cwd,(prefix+'_ImpSQL.txt'))+"]")
                    result=cfg.err_ERRORS
                    nologsql=cfg.err_TRUE

                if (nologimp==cfg.err_FALSE):
                    (logimp,result_)=fileIO.open_file_read_bin(self.logf,os.path.join(cwd,(prefix+'_ImpLog.txt')))
                    if (result_!=cfg.err_SUCCESS):
                        self._log(log.ERROR,"Hевозможно проверить файл ["+os.path.join(cwd,(prefix+'_ImpLog.txt'))+"] на наличие ошибок импорта")
                        result=cfg.err_ERRORS
                    else:
                        logimptxt=logimp.readlines()
                        logimp.close()
                        for line in logimptxt:
                            if (os.name=='nt'):
                                for error in cfg.erroractions:
                                    if (string.count(line,error.decode(cfg.charset).encode(cfg.wincharset2))>0):
                                        self._log(log.ERROR,"Обнаружена ошибка импорта в лог-файле ["+os.path.join(cwd,(prefix+'_ImpLog.txt'))+"]")
                                        self._log(log.ERROR,"Комментарий к ошибке: ["+str(cfg.erroractions[error]['err_text'])+"]")
                                        if (cfg.erroractions[error]['err_send']==cfg.err_TRUE):
                                            mailIO.send_file(self.logf,os.path.join(cwd,(prefix+'_ImpLog.txt')),'Файл отчета об ошибке импорта модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+']')
                                        result=cfg.erroractions[error]
                                        break

                                for error in cfg.erroractions:
                                    if (string.count(line,error)>0):
                                        self._log(log.ERROR,"Обнаружена ошибка импорта в лог-файле ["+os.path.join(cwd,(prefix+'_ImpLog.txt'))+"]")
                                        self._log(log.ERROR,"Комментарий к ошибке: ["+str(cfg.erroractions[error]['err_text'])+"]")
                                        if (cfg.erroractions[error]['err_send']==cfg.err_TRUE):
                                            mailIO.send_file(self.logf,os.path.join(cwd,(prefix+'_ExpLog.txt')),'Файл отчета об ошибке импорта модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+']')
                                        result=cfg.erroractions[error]
                                        break


                        # Если не было команды на рестарт, то не трогаем файлы
                        if (result!=cfg.err_RESTART):
                            # Копируем и удаляем ImpLog.txt
                            if (fileIO.copy_file_to_dir(self.logf,os.path.join(cwd,(prefix+'_ImpLog.txt')),os.path.join(arcdir,str(file__))) !=cfg.err_SUCCESS):
                                # if (result!=cfg.err_RESTART):
                                result=cfg.err_ERRORS
                                self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'_ImpLog.txt')))+"] не скопирован в архив")
                            else:
                                self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'_ImpLog.txt')))+"] скопирован в архив")
                                if (fileIO.remove_file(self.logf,os.path.join(cwd,(prefix+'_ImpLog.txt')))!=cfg.err_SUCCESS):
                                    self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'_ImpLog.txt')))+"] не удален")
                                    # if (result!=cfg.err_RESTART):
                                    result=cfg.err_ERRORS
                                else:
                                    self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(file__+'_ImpLog.txt')))+"] удален")


                if (nologsql!=cfg.err_FALSE):
                    # if (nologsql==cfg.err_ERRORS):
                    #     (logsql,result__)=fileIO.open_file_read_bin(self.logf,os.path.join(cwd,(prefix+'_ImpSQL.txt')))
                    #     if (result__!=cfg.err_SUCCESS):
                    #         self._log(log.ERROR,"Hевозможно проверить файл ["+os.path.join(cwd,(prefix+'_ImpSQL.txt'))+"] на наличие ошибок импорта")
                    #         if (result!=cfg.err_RESTART):
                    #             result=0
                    #     else:
                    #         logsqltxt=logsql.readlines()
                    #         logsql.close()
                    #         for line in logsqltxt:
                    #             if (string.count(line,'ERROR')>0):
                    #                 self._log(log.ERROR,"Обнаружена ошибка импорта в лог-файле(sql) ["+os.path.join(cwd,(prefix+'_ImpSQL.txt'))+"]")
                    #                 mailIO.send_file(self.logf,os.path.join(cwd,(prefix+'_ImpSQL.txt')),'Файл отчета(sql) об ошибке импорта модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.src_shop)+']')
                    #                 if (result!=cfg.err_RESTART):
                    #                     result=0
                    #                 break

                    # Если не было команды на рестарт, то не трогаем файлы
                    if (result!=cfg.err_RESTART):
                        # Копируем и удаляем ImpSQL.txt
                        if (fileIO.copy_file_to_dir(self.logf,os.path.join(cwd,(prefix+'_ImpSQL.txt')),os.path.join(arcdir,str(file__))) !=cfg.err_SUCCESS):
                            result=cfg.err_ERRORS
                            self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'_ImpSQL.txt')))+"] не скопирован в архив")
                        else:
                            self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'_ImpSQL.txt')))+"] скопирован в архив")
                            if (fileIO.remove_file(self.logf,os.path.join(cwd,(prefix+'_ImpSQL.txt')))!=cfg.err_SUCCESS):
                                self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'_ImpSQL.txt')))+"] не удален")
                                # if (result!=cfg.err_RESTART):
                                result=cfg.err_ERRORS
                            else:
                                self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'_ImpSQL.txt')))+"] удален")



                # Если не было команды на рестарт, то не трогаем файлы
                if (result!=cfg.err_RESTART):

                    # Копируем и удаляем сами файлы с данными
                    # *.dat
                    if (fileIO.copy_file_to_dir(self.logf,os.path.join(cwd,(prefix+'.dat')),os.path.join(arcdir,str(file__))) !=cfg.err_SUCCESS):
                        # if (result!=cfg.err_RESTART):
                        result=cfg.err_ERRORS
                        self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'.dat')))+"] не скопирован в архив")
                    else:
                        self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'.dat')))+"] скопирован в архив")
                        if (fileIO.remove_file(self.logf,os.path.join(cwd,(prefix+'.dat')))!=cfg.err_SUCCESS):
                            self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'.dat')))+"] не удален")
                            # if (result!=cfg.err_RESTART):
                            result=cfg.err_ERRORS
                        else:
                            self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'.dat')))+"] удален")
                            _files[files.index(file__+'.dat')]='NULL'
                    # *.pak
                    if (fileIO.copy_file_to_dir(self.logf,os.path.join(cwd,(prefix+'.pak')),os.path.join(arcdir,str(file__))) !=cfg.err_SUCCESS):
                        # if (result!=cfg.err_RESTART):
                        result=cfg.err_ERRORS
                        self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'.pak')))+"] не скопирован в архив")
                    else:
                        self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'.pak')))+"] скопирован в архив")
                        if (fileIO.remove_file(self.logf,os.path.join(cwd,(prefix+'.pak')))!=cfg.err_SUCCESS):
                            self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(prefix+'.pak')))+"] не удален")
                            # if (result!=cfg.err_RESTART):
                            result=cfg.err_ERRORS
                        else:
                            self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(prefix+'.pak')))+"] удален")
                            _files[files.index(file__+'.pak')]='NULL'

                # Удаляем мусор, если была ошибка
                files_garbage=os.listdir(cwd)
                for file_g in files_garbage:
                    file_g_s=string.split(file_g,'.imp')
                    if (len(file_g_s)==cfg.err_SUCCESS):
                        file_g_s_=string.split(file_g,'.tmp')
                        if (len(file_g_s_)!=cfg.err_SUCCESS):
                            self._log(log.INFO,"После выполнения импорта обнаружен файл-мусор ["+str(os.path.join(cwd,(file_g_s_[0]+'.tmp')))+"]")
                            if (fileIO.remove_file(self.logf,os.path.join(cwd,(file_g_s_[0]+'.tmp')))!=cfg.err_SUCCESS):
                                self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(file_g_s_[0]+'.tmp')))+"] не удален")
                                if (result!=cfg.err_RESTART):
                                    result=cfg.err_ERRORS
                            else:
                                self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(file_g_s_[0]+'.tmp')))+"] удален")
                    else:
                        self._log(log.INFO,"После выполнения импорта обнаружен файл-мусор ["+str(os.path.join(cwd,(file_g_s[0]+'.imp')))+"]")
                        if (fileIO.remove_file(self.logf,os.path.join(cwd,(file_g_s[0]+'.imp')))!=cfg.err_SUCCESS):
                            self._log(log.ERROR,"Файл ["+str(os.path.join(cwd,(file_g_s[0]+'.imp')))+"] не удален")
                            if (result!=cfg.err_RESTART):
                                result=cfg.err_ERRORS
                        else:
                            self._log(log.INFO,"Файл ["+str(os.path.join(cwd,(file_g_s[0]+'.imp')))+"] удален")


        fileIO.close_del_file_lock(self.logf,lockf)
        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return result


    def _gui_import(self):
        # WORKAROUND
        self.auto=cfg.err_UNKNOWN

        if (self.runmode==cfg.GUI_IMPORT):
            self.runmode=cfg.IMPORT
        else:
            self.runmode=cfg.EXPORT

        def start_pressed(event):
            if (self.src_shop==None):
                label_error.text='Hе задан магазин-источник'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=cfg.err_TRUE
                return cfg.err_ERRORS
            if (self.dst_shop==None):
                label_error.text='Hе задан магазин назначения'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=cfg.err_TRUE
                return cfg.err_ERRORS
            if (self.auto==cfg.err_UNKNOWN):
                label_error.text='Hе задан режим запуска'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=cfg.err_TRUE
                return cfg.err_ERRORS
            self.dates=text_dates.text
            if (self.dates==''):
                label_error.text='Hе задана ни одна дата'.decode(cfg.charset).encode(cfg.guicharset)
                label_error.visible=cfg.err_TRUE
                return cfg.err_ERRORS
            label_error.text=''
            label_error.visible=cfg.err_FALSE

            self.oldlogf=self.logf
            self.oldloglevel=self.loglevel
            self.oldrunmode=self.runmode
            self.oldupload=self.upload
            self.oldauto=self.auto
            self.oldargs=self.args
            self.oldsrc_shop=self.src_shop
            self.olddst_shop=self.dst_shop


            (modfile,modname,moddesc)=imp.find_module(self.__name__)
            module=imp.load_module(self.__name__,modfile,modname,moddesc)
            name=self.__name__
            module_=eval('module.'+name+'()')


            if (self.runmode==cfg.IMPORT):
                self._log(log.INFO,"Запуск новой нити импорта модуля ["+str(module.__desc__)+"] из магазина ["+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'], даты '+str(self.dates)+' с аргументами '+str(self.args)+'')                
                newthread=thread.start_new_thread(module_.start_import,(self.auto,self.runmode,self.upload,self.src_shop,self.dst_shop,self.dates,self.loglevel,self.args))                                            
            else:
                self._log(log.INFO,"Запуск новой нити экпорта модуля ["+str(module.__desc__)+"] из магазина ["+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'], даты '+str(self.dates)+' с аргументами '+str(self.args)+'')                                
                newthread=thread.start_new_thread(module_.start_export,(self.auto,self.runmode,self.upload,self.src_shop,self.dst_shop,self.dates,self.loglevel,self.args))

            list_shops_from.selection=-1
            list_shops_to.selection=-1
            self.logf=self.oldlogf
            self.loglevel=self.oldloglevel
            self.runmode=self.oldrunmode
            self.upload=self.oldupload
            self.auto=self.oldauto
            self.args=self.oldargs
            self.src_shop=None
            self.dst_shop=None



        def exit_pressed(event):
            gui.remove(window_main)
            gui._running=cfg.err_FALSE
            return cfg.err_ERRORS

        def dates_entered(event):
            # BUG
            # Почему-то не работает этот хандлер ;-(
            self.dates=text_dates.text

        def shop_from_selected(event):
            self.src_shop=[]
            self.src_shop.append(cfg.shops.items()[list_shops_from.selection][0])

        def shop_to_selected(event):
            self.dst_shop=[]
            self.dst_shop.append(cfg.shops.items()[list_shops_to.selection][0])

        def auto_selected(event):
            self.auto=cfg.err_TRUE

        def manual_selected(event):
            self.auto=cfg.err_FALSE
        # Рисуем корявую морду
        gui = anygui.Application()
        if (self.runmode==cfg.IMPORT):
            window_main = anygui.Window(text=(self.__desc__.decode(cfg.charset).encode(cfg.guicharset))+' ['+(self.__version__.decode(cfg.charset).encode(cfg.guicharset))+']'.decode(cfg.charset).encode(cfg.guicharset))
        else:
            window_main = anygui.Window(text=(self.__desc__.decode(cfg.charset).encode(cfg.guicharset))+' ['+(self.__version__.decode(cfg.charset).encode(cfg.guicharset))+']'.decode(cfg.charset).encode(cfg.guicharset))            

        button_start = anygui.Button(text='Старт'.decode(cfg.charset).encode(cfg.guicharset))
        button_exit = anygui.Button(text='Выход'.decode(cfg.charset).encode(cfg.guicharset))

        group_auto=anygui.RadioGroup()

        radio_auto=anygui.RadioButton(text='Автоматически'.decode(cfg.charset).encode(cfg.guicharset))
        radio_manual=anygui.RadioButton(text='Вручную'.decode(cfg.charset).encode(cfg.guicharset))

        group_auto.add([radio_auto,radio_manual])
        group_auto.selection=cfg.err_TRUE

        text_dates=anygui.TextField()
        text_dates.text=date.get_cur_date(self.logf)

        label_dates=anygui.Label(text='Даты'.decode(cfg.charset).encode(cfg.guicharset))
        label_direction=anygui.Label(text='из                          в'.decode(cfg.charset).encode(cfg.guicharset))        
        label_error=anygui.Label(text=''.decode(cfg.charset).encode(cfg.guicharset))
        label_error.visible=cfg.err_FALSE

        list_shops_from=anygui.ListBox(items=cfg.shops)
        list_shops_to=anygui.ListBox(items=cfg.shops)


        if (self.runmode==cfg.IMPORT):
            label_runmode=anygui.Label(text='Импорт'.decode(cfg.charset).encode(cfg.guicharset))
        else:
            label_runmode=anygui.Label(text='Экспорт'.decode(cfg.charset).encode(cfg.guicharset))

        window_main.add(label_runmode,left=10,top=5,hmove=0)
        window_main.add(label_direction,left=50,top=(label_runmode,2),hmove=0)
        window_main.add((list_shops_from,list_shops_to),direction='right',left=10,top=(label_direction,5),space=10)
        window_main.add((radio_auto,radio_manual),direction='down',left=10,top=(list_shops_from,15))
        window_main.add(label_error,direction='down',left=10,top=(radio_manual,5))
        window_main.add(label_dates,direction='down',left=10,top=(label_error,5))
        window_main.add(text_dates,direction='down',left=10,top=(label_dates,5),hstretch=1)
        text_dates.width=(list_shops_to.right-10)
        window_main.add(button_start,left=10,top=(text_dates,5))
        window_main.add(button_exit,left=(button_start,10),top=(text_dates,5))
        window_main.width=(list_shops_to.right+10)
        label_error.width=window_main.width
        label_direction.width=window_main.width
        window_main.height=(button_exit.bottom+10)
        label_runmode.left=int((window_main.width-len(label_runmode.text)-50)/2)

        anygui.link(button_start,'click',start_pressed)
        anygui.link(button_exit,'click',exit_pressed)
        anygui.link(list_shops_from,'select',shop_from_selected)
        anygui.link(list_shops_to,'select',shop_to_selected)
        anygui.link(text_dates,'enterkey',dates_entered)
        anygui.link(radio_auto,auto_selected)
        anygui.link(radio_manual,manual_selected)

        gui.add(window_main)
        gui.run()

        return cfg.err_SUCCESS

    def _gui_export(self):
        return cfg.err_SUCCESS






###############################################




    def is_alive_threads(self):
        """ Check if there are live threads """
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        for thread_ in self.threads:
            if (cfg._oldthreads==cfg.err_FALSE):
                if (thread_.isAlive()==cfg.err_TRUE):
                    self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
                    return cfg.err_SUCCESS
            else:
                if (thread_['evt'].isSet()==cfg.err_FALSE):
                    self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
                    return cfg.err_TRUE
        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        return cfg.err_FALSE




    def module_thread(self,sem,evt):
        """ Start thread for each shop """
        # allow main thread to run
        sem.release()
        # time.sleep(2)
        self.init_module_log()
        result=self.init_module_ini()
        #self.logf.setlevel(self.loglevel)
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        #
        if (self.runmode==cfg.EXPORT):
            self.shortmode='exp'
        elif (self.runmode==cfg.IMPORT):
            self.shortmode='imp'
        else:
            self.shortmode='err'

        if (result!=cfg.err_SUCCESS):
            self._log(log.ERROR,"Работа модуля невозможна без INI-файла с общими настройками")
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            self.send_module_log()
            self.done_module_log()
            evt.set()
            return result

        if (self.prepare_ini()!=cfg.err_SUCCESS):
            self._log(log.ERROR,"Работа модуля невозможна без корректного INI-файлы")
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
            self.send_module_log()
            self.done_module_log()
            evt.set()
            return cfg.err_SYSERROR

        #
        if (self.runmode==cfg.EXPORT):
            if (netIO.is_mssql_alive(cfg.servers[cfg.runmodes[self.runmode]][self.src_shop])!=cfg.err_TRUE):
                self._log(log.ERROR,"MSSQL сервер магазина ["+str(self.src_shop)+"] не запущен или нет связи")
                result=cfg.err_NOCONNECT
            else:
                result=self._export(None)
            while (result==cfg.err_RESTART):
                self._log(log.INFO,"Перезапуск экспорта из магазина ["+str(self.src_shop)+'] для магазина ['+str(self.dst_shop)+'], даты '+str(self.date)+' с аргументами '+str(self.args)+' с кодом выхода ['+str(cfg.errors[result])+']')                                        
                result=self._export(None)
            self._log(log.INFO,"Завершение экспорта из магазина ["+str(self.src_shop)+'] для магазина ['+str(self.dst_shop)+'], даты '+str(self.date)+' с аргументами '+str(self.args)+' с кодом выхода ['+str(cfg.errors[result])+']')
            mailIO.send_message(self.logf,'Экспорт модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] для магазина ['+str(self.dst_shop)+'] завершен с кодом выхода ['+str(cfg.errors[result])+']','Экспорт модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'] завершен с кодом выхода ['+str(cfg.errors[result])+']')            
        else:
            # Пытаемся сообразить, как же это правильно делать, мать-перемать
            # files=os.listdir(os.path.join(cfg.improot,str(self.__name__),str(self.src_shop)))
            if (self.src_shop=='office'):
                fileIO.make_dirs(self.logf,os.path.join(cfg.exproot,str(self.__name__),str(self.dst_shop)))
                files=os.listdir(os.path.join(cfg.exproot,str(self.__name__),str(self.dst_shop)))
            else:
                fileIO.make_dirs(self.logf,os.path.join(cfg.exproot,str(self.__name__),str(self.src_shop)))
                files=os.listdir(os.path.join(cfg.exproot,str(self.__name__),str(self.src_shop)))

            if (netIO.is_mssql_alive(cfg.servers[cfg.runmodes[self.runmode]][self.src_shop])!=cfg.err_SUCCESS):
                self._log(log.ERROR,"MSSQL сервер магазина ["+str(self.src_shop)+"] не запущен или нет связи")                
                result=cfg.err_NOCONNECT
            else:
                result=self._import(files)
            while (result==cfg.err_RESTART):
                self._log(log.WARNING,"Перезапуск импорта из магазина ["+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'], даты '+str(self.date)+' с аргументами '+str(self.args)+' с кодом выхода ['+str(cfg.errors[result])+']')
                result=self._import(files)
            self._log(log.INFO,"Завершение импорта из магазина ["+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'], даты '+str(self.date)+' с аргументами '+str(self.args)+' с кодом выхода ['+str(cfg.errors[result])+']')
            mailIO.send_message(self.logf,'Импорт модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'] завершен с кодом выхода ['+str(result)+']','Импорт модуля ['+str(self.__desc__)+'] из магазина ['+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'] завершен с кодом выхода ['+str(cfg.errors[result])+']')

        self.send_module_log()
        self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        self.done_module_ini()
        self.done_module_log()
        evt.set()
        # BUG
        # При возврате чего-либо, отличного от 0 - родитель сообщает о ошибке в треде ;-/
        # Связано с неправильным использованием threads
        return result


    def start_import_single(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args,sem,evt):
        self.loglevel=loglevel
        self.runmode=runmode
        self.upload=upload
        self.auto=auto
        self.args=args
        result=cfg.err_SUCCESS
        self.src_shop=src_shops
        self.dst_shop=dst_shops
        self.date=dates
        # self._log(log.INFO,'Магазины '+str(self.src_shop)+str(self.dst_shop))
        if (self.runmode==cfg.EXPORT):
            self.do_archive=cfg.err_FALSE
        else:
            self.do_archive=cfg.err_TRUE
        self.module_thread(sem,evt)

    def start_export_single(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args,sem,evt):
        self.start_import_single(auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args,sem,evt)

    def start_import(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        self.loglevel=loglevel
        self.runmode=runmode
        self.upload=upload
        self.auto=auto
        self.args=args
        result=cfg.err_SUCCESS
        self.src_shop=''
        self.dst_shop=''
        if (self.runmode==cfg.EXPORT):
            self.do_archive=cfg.err_FALSE
        else:
            self.do_archive=cfg.err_TRUE

        # some shit ;(
        # при использвании класса фигня с logf, тот же самый идет
        self.logf=self.init_module_log()
        self._log(log.DEBUG,"В функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));
        # self._log(log.ERROR,str(src_shops)+','+str(dst_shops))
        dates_=date.get_dates(dates,self.logf)
        if (len(dst_shops)>1) and (len(src_shops)>1):
            self._log(log.ERROR,"Hельзя указывать несколько магазинов-источников и магазинов назначения одновременно")
            return cfg.err_MULTISRCDST
        if (self.runmode==cfg.EXPORT):
            if (dst_shops[0]=='office'):
                # Одновременный экпорт в офис может быть
                cfg._oldthreads=cfg.err_TRUE
                for src_shop_ in src_shops:
                    for date_ in dates_:
                        sem=threading.Semaphore(2)
                        sem.acquire()
                        evt=threading.Event()
                        evt.clear()
                        self.src_shop=src_shop_
                        self.dst_shop=dst_shops[0]
                        self.date=date_
                        try:
                            self._log(log.INFO,"Запуск новой нити модуля (экспорт) из магазина ["+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'], даты '+str(self.date)+' с аргументами '+str(self.args)+'')
                            self.oldlogf=self.logf
                            self.oldinif=self.inif
                            self.oldloglevel=self.loglevel
                            self.oldrunmode=self.runmode
                            self.oldupload=self.upload
                            self.oldauto=self.auto
                            self.oldargs=self.args
                            self.oldsrc_shop=self.src_shop
                            self.olddst_shop=self.dst_shop


                            if (cfg._oldthreads==cfg.err_TRUE):
                                newthread=threading.Thread(target=self.module_thread(sem,evt))
                                newthread.setName(str(self.src_shop)+'-'+str(self.dst_shop)+','+str(self.date))
                                newthread.start()
                            else:
                                (modfile,modname,moddesc)=imp.find_module(self.__name__)
                                module=imp.load_module(self.__name__,modfile,modname,moddesc)
                                name=self.__name__
                                module_=eval('module.'+name+'()')
                                thread_=thread.start_new_thread(module_.start_export_single,(self.auto,self.runmode,self.upload,self.src_shop,self.dst_shop,self.date,self.loglevel,self.args,sem,evt))                                                                            

                            # wait thread to start
                            sem.acquire()
                            self.logf=self.oldlogf
                            self.inif=self.oldinif
                            self.loglevel=self.oldloglevel
                            self.runmode=self.oldrunmode
                            self.upload=self.oldupload
                            self.auto=self.oldauto
                            self.args=self.oldargs
                            self.src_shop=self.oldsrc_shop
                            self.dst_shop=self.olddst_shop


                            if (cfg._oldthreads==cfg.err_FALSE):
                                self._log(log.INFO,"Hовая нить успешно запущена ["+str(newthread.getName())+"]")
                            else:
                                self._log(log.INFO,"Hовая нить успешно запущена ["+str(thread_)+"]")
                        except:
                            self._log(log.ERROR,"Ошибка запуска новой нити модуля");
                            self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                            result=cfg.err_SYSERROR
                            continue
                        if (cfg._oldthreads==cfg.err_FALSE):
                            self.threads.append(newthread)
                        else:
                            entry={}
                            entry['pid']=thread_
                            entry['evt']=evt
                            self.threads.append(entry)


            else:
                # Одновременный экпорт в магазины может быть
                # cfg._oldthreads=cfg.err_TRUE
                # BUG! Временно отключаем threads ;(
                cfg._oldthreads=cfg.err_FALSE
                for dst_shop_ in dst_shops:
                    for date_ in dates_:
                        sem=threading.Semaphore(2)
                        sem.acquire()
                        evt=threading.Event()
                        evt.clear()
                        self.src_shop=src_shops[0]
                        self.dst_shop=dst_shop_
                        self.date=date_
                        try:
                            self._log(log.INFO,"Запуск новой нити модуля (экспорт) из магазина ["+str(self.src_shop)+'] в магазин ['+str(self.dst_shop)+'], даты '+str(self.date)+' с аргументами '+str(self.args)+'')
                            self.oldlogf=self.logf
                            self.oldinif=self.inif
                            self.oldloglevel=self.loglevel
                            self.oldrunmode=self.runmode
                            self.oldupload=self.upload
                            self.oldauto=self.auto
                            self.oldargs=self.args
                            self.oldsrc_shop=self.src_shop
                            self.olddst_shop=self.dst_shop

                            if (cfg._oldthreads==cfg.err_FALSE):
                                # BUG
                                # нужно убрать использование функции везде и решить проблему с логами
                                ##newthread=threading.Thread(target=self.module_thread,args=(sem,evt))
                                newthread=threading.Thread(target=self.module_thread(sem,evt))                                
                                newthread.setName(str(self.src_shop)+'-'+str(self.dst_shop)+','+str(self.date))
                                newthread.start()
                            else:
                                (modfile,modname,moddesc)=imp.find_module(self.__name__)
                                module=imp.load_module(self.__name__,modfile,modname,moddesc)
                                name=self.__name__
                                module_=eval('module.'+name+'()')
                                thread_=thread.start_new_thread(module_.start_export_single,(self.auto,self.runmode,self.upload,self.src_shop,self.dst_shop,self.date,self.loglevel,self.args,sem,evt))                                                                            

                            # wait thread to start
                            sem.acquire()
                            self.logf=self.oldlogf
                            self.inif=self.oldinif
                            self.loglevel=self.oldloglevel
                            self.runmode=self.oldrunmode
                            self.upload=self.oldupload
                            self.auto=self.oldauto
                            self.args=self.oldargs
                            self.src_shop=self.oldsrc_shop
                            self.dst_shop=self.olddst_shop
                            if (cfg._oldthreads==cfg.err_FALSE):
                                self._log(log.INFO,"Hовая нить успешно запущена ["+str(newthread.getName())+"]")
                            else:
                                self._log(log.INFO,"Hовая нить успешно запущена ["+str(thread_)+"]")
                        except:
                            self._log(log.ERROR,"Ошибка запуска новой нити модуля");
                            self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                            result=cfg.err_SYSERROR
                            continue
                        if (cfg._oldthreads==cfg.err_FALSE):
                            self.threads.append(newthread)
                        else:
                            entry={}
                            entry['pid']=thread_
                            entry['evt']=evt
                            self.threads.append(entry)


        else:
            if (dst_shops[0]=='office'):
                # Hе должно быть одновременного импорта в офис
                cfg._oldthreads=cfg.err_FALSE
                for src_shop_ in src_shops:
                    for date_ in dates_:
                        sem=threading.Semaphore(2)
                        sem.acquire()
                        evt=threading.Event()
                        evt.clear()
                        self.dst_shop=dst_shops[0]
                        self.src_shop=src_shop_
                        self.date=date_
                        try:
                            self._log(log.INFO,"Запуск новой нити модуля (импорт) в магазин ["+str(self.dst_shop)+'] из магазина ['+str(self.src_shop)+'], даты '+str(self.date)+' с аргументами '+str(self.args)+'')
                            self.oldlogf=self.logf
                            self.oldinif=self.inif
                            self.oldloglevel=self.loglevel
                            self.oldrunmode=self.runmode
                            self.oldupload=self.upload
                            self.oldauto=self.auto
                            self.oldargs=self.args
                            self.oldsrc_shop=self.src_shop
                            self.olddst_shop=self.dst_shop


                            if (cfg._oldthreads==cfg.err_FALSE):
                                newthread=threading.Thread(target=self.module_thread(sem,evt))
                                newthread.setName(str(self.src_shop)+'-'+str(self.dst_shop)+','+str(self.date))
                                newthread.start()
                            else:
                                (modfile,modname,moddesc)=imp.find_module(self.__name__)
                                module=imp.load_module(self.__name__,modfile,modname,moddesc)
                                name=self.__name__
                                module_=eval('module.'+name+'()')
                                thread_=thread.start_new_thread(module_.start_import_single,(self.auto,self.runmode,self.upload,self.src_shop,self.dst_shop,self.date,self.loglevel,self.args,sem,evt))                                                                            

                            # wait thread to start
                            sem.acquire()
                            self.logf=self.oldlogf
                            self.inif=self.oldinif
                            self.loglevel=self.oldloglevel
                            self.runmode=self.oldrunmode
                            self.upload=self.oldupload
                            self.auto=self.oldauto
                            self.args=self.oldargs
                            self.src_shop=self.oldsrc_shop
                            self.dst_shop=self.olddst_shop
                            if (cfg._oldthreads==cfg.err_FALSE):
                                self._log(log.INFO,"Hовая нить успешно запущена ["+str(newthread.getName())+"]")
                            else:
                                self._log(log.INFO,"Hовая нить успешно запущена ["+str(thread_)+"]")
                        except:
                            self._log(log.ERROR,"Ошибка запуска новой нити модуля");
                            self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                            result=cfg.err_SYSERROR
                            continue
                        if (cfg._oldthreads==cfg.err_FALSE):
                            self.threads.append(newthread)
                        else:
                            entry={}
                            entry['pid']=thread_
                            entry['evt']=evt
                            self.threads.append(entry)

            else:
                for dst_shop_ in dst_shops:
                    # Одновременный импорт в магазины может быть
                    cfg._oldthreads=cfg.err_TRUE
                    for date_ in dates_:
                        sem=threading.Semaphore(2)
                        sem.acquire()
                        evt=threading.Event()
                        evt.clear()
                        self.dst_shop=dst_shop_
                        self.src_shop=src_shops[0]
                        self.date=date_
                        try:
                            self._log(log.INFO,"Запуск новой нити модуля (импорт) в магазин ["+str(self.dst_shop)+'] из магазина ['+str(self.src_shop)+'], даты '+str(self.date)+' с аргументами '+str(self.args)+'')
                            self.oldlogf=self.logf
                            self.oldinif=self.inif
                            self.oldloglevel=self.loglevel
                            self.oldrunmode=self.runmode
                            self.oldupload=self.upload
                            self.oldauto=self.auto
                            self.oldargs=self.args
                            self.oldsrc_shop=self.src_shop
                            self.olddst_shop=self.dst_shop


                            if (cfg._oldthreads==cfg.err_FALSE):
                                newthread=threading.Thread(target=self.module_thread(sem,evt))
                                newthread.setName(str(self.src_shop)+'-'+str(self.dst_shop)+','+str(self.date))
                                newthread.start()
                            else:
                                (modfile,modname,moddesc)=imp.find_module(self.__name__)
                                module=imp.load_module(self.__name__,modfile,modname,moddesc)
                                name=self.__name__
                                module_=eval('module.'+name+'()')
                                thread_=thread.start_new_thread(module_.start_import_single,(self.auto,self.runmode,self.upload,self.src_shop,self.dst_shop,self.date,self.loglevel,self.args,sem,evt))

                            # wait thread to start
                            sem.acquire()
                            self.logf=self.oldlogf
                            self.inif=self.oldinif
                            self.loglevel=self.oldloglevel
                            self.runmode=self.oldrunmode
                            self.upload=self.oldupload
                            self.auto=self.oldauto
                            self.args=self.oldargs
                            self.src_shop=self.oldsrc_shop
                            self.dst_shop=self.olddst_shop
                            if (cfg._oldthreads==cfg.err_ERRORS):
                                self._log(log.INFO,"Hовая нить успешно запущена ["+str(newthread.getName())+"]")
                            else:
                                self._log(log.INFO,"Hовая нить успешно запущена ["+str(thread_)+"]")

                        except:
                            self._log(log.ERROR,"Ошибка запуска новой нити модуля");
                            self._log(log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"));
                            result=cfg.err_SYSERROR
                            continue
                        if (cfg._oldthreads==cfg.err_FALSE):
                            self.threads.append(newthread)
                        else:
                            entry={}
                            entry['pid']=thread_
                            entry['evt']=evt
                            self.threads.append(entry)

        cycle=cfg.err_TRUE
        while (cycle==cfg.err_TRUE):
            if (len(self.threads)==0):
                self._log(log.WARNING,"Hет ни одной нити модуля")
                break
            for thread_ in self.threads:
                if (cfg._oldthreads==cfg.err_FALSE):
                    if (thread_.isAlive()==cfg.err_FALSE):
                        self._log(log.INFO,'Hить модуля ['+str(thread_.getName())+'] завершила работу')
                        self.threads.remove(thread_)
                else:
                    if (thread_['evt'].isSet()==cfg.err_TRUE):
                        self._log(log.INFO,'Hить модуля ['+str(thread_['pid'])+'] завершила работу')
                        self.threads.remove(thread_)
            if (self.is_alive_threads()==cfg.err_FALSE):
                self._log(log.INFO,"Все нити модуля завершили работу")
                cycle=cfg.err_FALSE
                break
            time.sleep(2)
            self._log(log.DEBUG,"Выход из функции %s" % str(inspect.getframeinfo(inspect.currentframe())[1]));

        self.send_module_log()
        self.done_module_log()
        return result


    def start_export(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        result=self.start_import(auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args)
        return result


    def start_gui_import(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        self.loglevel=loglevel
        self.runmode=runmode
        self.upload=upload
        self.auto=auto
        self.args=args
        self.src_shop=src_shops
        self.dst_shop=dst_shops
        self.dates=dates
        self.do_archive=cfg.err_TRUE
        self.logf=self.init_module_log()
        result=self._gui_import()
        self.send_module_log()
        self.done_module_log()

        return result

    def start_gui_export(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        self.loglevel=loglevel
        self.runmode=runmode
        self.upload=upload
        self.auto=auto
        self.args=args
        self.src_shop=src_shops
        self.dst_shop=dst_shops
        self.dates=dates
        self.do_archive=cfg.err_FALSE
        self.logf=self.init_module_log()
        result=self._gui_import()
        self.send_module_log()
        self.done_module_log()
        return result


    def start_module(self,auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args):
        """ Start current module """
        result=eval('self.start_'+cfg.runmodes[runmode])(auto,runmode,upload,src_shops,dst_shops,dates,loglevel,args)
        return result
