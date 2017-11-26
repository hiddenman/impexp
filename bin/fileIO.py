# -*- coding: cp1251 -*-
# file and dir I/O module
# Сделать проверки в shutil>* ниже

import log,cfg,os,sys,shutil,locks,mailIO,string

def _log(logf,facility,logstr):
    """ Internal log wrapper """
    logf.log(str(__name__),facility,logstr)

def dir_exists(path):
    """ Check dir is exists """
    #return os.access(path,os.F_OK)
    return os.path.isdir(path)    

def file_exists(path):
    """ Check file is exists """
    # BUG: doesn't work correct with LOCKs
    #return os.access(path,os.F_OK)
    # this works
    return os.path.isfile(path)

def dir_r_ok(path):
    """ Check dir is readable """
    return os.access(path,os.R_OK)

def dir_w_ok(path):
    """ Check dir is writable """
    return os.access(path,os.W_OK)

def dir_x_ok(path):
    """ Check dir is executable """
    return os.access(path,os.X_OK)

def dir_ok(logf,path):
    """ Check dir is writable """
    if (dir_exists(path)==cfg.err_SUCCESS):
        if (dir_r_ok(path)==cfg.err_SUCCESS):
            if (dir_w_ok(path)==cfg.err_SUCCESS):
                if (dir_x_ok(path)==cfg.err_SUCCESS):
                    return cfg.err_SUCCESS
                else:
                    _log(logf,log.ERROR,"Ошибка открытия каталога ["+str(path)+"]")
                    return cfg.err_ERRORS
            else:
                _log(logf,log.ERROR,"Ошибка открытия на запись каталога ["+str(path)+"]")
                return cfg.err_ERRORS
        else:
            _log(logf,log.ERROR,"Ошибка открытия на чтение каталога ["+str(path)+"]")
            return cfg.err_ERRORS
    else:
        _log(logf,log.ERROR,"Каталог ["+str(path)+"] не существует")
        return cfg.err_ERRORS
        
def make_dirs(logf,path):
    """ Make all dirs in path """
    try:
        if (dir_exists(path)==cfg.err_SUCCESS):
            return cfg.err_SUCCESS
        else:
            os.makedirs(path)
            _log(logf,log.INFO,"Созданы каталоги [%s]" % str(path))
            # Временно убрали это, ибо мусорит много.
            # mailIO.send_message(logf,'Созданы каталоги ['+str(path)+'], обязательно установите необходимые права','Созданы новые каталоги')            
    except:
        _log(logf,log.ERROR,"Ошибка создания каталогов ["+str(path)+"]")
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return cfg.err_ERRORS
    return cfg.err_SUCCESS

def remove_file(logf,path):
    """ Remove file """
    try:
        os.remove(path)
    except:
        _log(logf,log.ERROR,"Ошибка удаления файла ["+str(path)+"]" )
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        _log(logf,log.ERROR,"Аттрибуты файла ["+str(os.stat(path))+"]" )        
        return cfg.err_ERRORS
    return cfg.err_SUCCESS



def copy_file_to_dir(logf,src,dst):
    """ Copy file from src to dst """
    if ( (make_dirs(logf,dst)!=cfg.err_SUCCESS) or ( dir_ok(logf,dst)!=cfg.err_SUCCESS) ):
        return cfg.err_ERRORS
    try:
        if (os.name=='nt'):
            srcbname=string.join(string.split(src,'\\')[:-1],'\\')
            srcfname=string.join(string.split(src,'\\')[-1:],'\\')
        else:
            srcbname=string.join(string.split(src,'/')[:-1],'/')
            srcfname=string.join(string.split(src,'/')[-1:],'/')
        if (file_exists(os.path.join(dst,srcfname))==cfg.err_SUCCESS):
            (sst_mode, sst_ino, sst_dev, sst_nlink, sst_uid, sst_gid, sst_size, sst_atime, sst_mtime, sst_ctime)= os.stat(src)
            (dst_mode, dst_ino, dst_dev, dst_nlink, dst_uid, dst_gid, dst_size, dst_atime, dst_mtime, dst_ctime)= os.stat(os.path.join(dst,srcfname))
            if ((sst_size==dst_size) and (sst_mtime==dst_mtime)):
                _log(logf,log.INFO,"Файлы  ["+str(src)+"] и ["+str(os.path.join(dst,srcfname))+"] одинаковые, не копируем")
                return cfg.err_SUCCESS
        shutil.copy2(src,dst)
    except:
        _log(logf,log.ERROR,"Ошибка копирования ["+str(src)+"] в ["+str(dst)+"]")
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return cfg.err_ERRORS
    return cfg.err_SUCCESS


def copy_expand_file_to_dir(logf,basename,src,dst):
    """ Copy all files from src to dst """
    return (copy_file_to_dir(logf,os.path.join(basename,src),dst))


def copy_files_to_dir(logf,src,dst):
    """ Copy all files from src to dst """
    result=cfg.err_SUCCESS
    for file in src:
        if (copy_file_to_dir(logf,file,dst)!=cfg.err_SUCCESS):
            result=cfg.err_ERRORS
    return result


def copy_expand_files_to_dir(logf,basename,src,dst):
    """ Copy all files from src to dst """
    result=cfg.err_SUCCESS
    for file in src:
        if (copy_expand_file_to_dir(logf,basename,file,dst)!=1):
            result=cfg.err_ERRORS
    return result



def move_file_to_dir(logf,src,dst):
    """ Move file from src to dst """
    if (copy_file_to_dir(logf,src,dst)==cfg.err_ERRORS):
        return cfg.err_ERRORS
    else:
        return (remove_file(logf,src))        

def move_expand_file_to_dir(logf,basename,src,dst):
    """ Move file from src to dst """
    if (copy_expand_file_to_dir(logf,basename,src,dst)==cfg.err_ERRORS):
        return cfg.err_ERRORS
    else:
        return (remove_file(logf,os.path.join(basename,src)))        


def move_files_to_dir(logf,src,dst):
    """ Move all files from src to dst """
    result=cfg.err_SUCCESS
    for file in src:
        if (copy_file_to_dir(logf,file,dst)!=cfg.err_SUCCESS):
            result=cfg.err_ERRORS
        if (remove_file(logf,src)!=cfg.err_SUCCESS):
            result=cfg.err_ERRORS
    return result

def move_expand_files_to_dir(logf,basename,src,dst):
    """ Move all files from src to dst """
    result=cfg.err_SUCCESS
    for file in src:
        if (move_expand_file_to_dir(logf,basename,file,dst)!=cfg.err_SUCCESS):
            result=cfg.err_ERRORS
    return result


        
def open_file_read_bin(logf,path):
    """ Open file for reading with binary mode """
    try:
        fd=open(path,"rb")
    except:
        _log(logf,log.ERROR,"Ошибка открытия файла на чтение ["+str(path)+']')
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return None,cfg.err_ERRORS
    return fd,cfg.err_SUCCESS

def open_file_read(logf,path):
    """ Open file for reading """
    try:
        fd=open(path,"r")
    except:
        _log(logf,log.ERROR,"Ошибка открытия файла на чтение ["+str(path)+']')
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return None,cfg.err_ERRORS
    return fd,cfg.err_SUCCESS

def open_file_lock(logf,path):
    """ Open file with locking """
    if (locks.check_file_lock(logf,path)!=cfg.err_FALSE):
        _log(logf,log.ERROR,"Ошибка создания файла ["+str(path)+"]")        
        return None,cfg.err_ERRORS
    try:
        lockf=open(path,"a+")
    except:
        _log(logf,log.ERROR,"Ошибка создания файла ["+str(path)+']')
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return None,cfg.err_SYSERROR
    if (locks.set_file_lock(logf,lockf)!=cfg.err_SUCCESS):
        return None,cfg.err_SYSERROR
        
    return lockf,cfg.err_SUCCESS


def close_file_lock(logf,lockf):
    """ Close locked file """
    path=lockf.name
    # BUG:
    # Hельзя разблокировать, а то могут покоцать до закрытия
    if (locks.unset_file_lock(logf,lockf)!=cfg.err_SUCCESS):
      _log(logf,log.ERROR,"Ошибка разблокировки файла ["+str(lockf)+']')
      _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
    return cfg.err_ERRORS
    try:
        lockf.close()        
    except:
        _log(logf,log.ERROR,"Ошибка закрытия файла ["+str(path)+']')
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return cfg.err_ERRORS
    return cfg.err_SUCCESS

def close_del_file_lock(logf,lockf):
    """ Close and remove locked file """
    path=lockf.name
    # BUG:
    # Hельзя разблокировать, а то могут покоцать до закрытия
    if (locks.unset_file_lock(logf,lockf)!=cfg.err_SUCCESS):
        _log(logf,log.ERROR,"Ошибка разблокировки файла ["+str(lockf)+']')
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return cfg.err_ERRORS
    try:
        lockf.close()        
    except:
        _log(logf,log.ERROR,"Ошибка закрытия файла ["+str(path)+']')
        _log(logf,log.ERROR,"Сообщение системы: "+str("["+str(sys.exc_info()[0])+"."+str(sys.exc_info()[1])+"]"))
        return cfg.err_ERRORS
    return (remove_file(logf,path))
