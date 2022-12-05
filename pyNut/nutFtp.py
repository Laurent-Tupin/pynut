try:
    from . import _lib as lib
    from . import nutOther as oth
    from . import nutDate as dat
    from . import nutFiles as fl
except:
    try:
        import _lib as lib
        import nutFiles as fl
        import nutDate as dat
        import nutOther as oth
    except:
        from pyNut import _lib as lib
        from pyNut import nutFiles as fl
        from pyNut import nutDate as dat
        from pyNut import nutOther as oth
os          = lib.os()
np          = lib.numpy()
ftplib      = lib.ftplib()
SSLSocket   = lib.SSLSocket()
pmiko       = lib.paramiko()



#****************************************************************************************
#******** Class Correction of FTP_TLS ***************************************************
# Source: https://raw.githubusercontent.com/weewx/weewx/master/bin/weeutil/ftpupload.py
#****************************************************************************************
class ReusedSslSocket(SSLSocket):
    def unwrap(self):
        pass

class FTP_TLS_IgnoreHost(ftplib.FTP_TLS):
    def makepasv(self):
        _, port = super().makepasv()
        return self.host, port
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn, server_hostname = self.host, session = self.sock.session)
            conn.__class__ = ReusedSslSocket
        return conn, size
#****************************************************************************************





#---------------------------------------------------------------
# ------------- CLASS FTP management ---------------------------
#---------------------------------------------------------------
@oth.dec_singletonsClass
class c_FTP:
    def __init__(self, str_host, str_uid, str_pwd, bl_ssl = False, int_timeOut = -1, int_portnumber = 21):
        self.__str_host = str_host
        self.__str_uid = str_uid
        self.__str_pwd = str_pwd
        self.l_Folder = []
        self.__bl_ssl = bl_ssl
        self.__int_timeOut = int_timeOut
        self.__int_portnumber = int_portnumber
        self.__bl_msgLosingConnection = False
        self.__d_ListFiles = {}
        
    def __del__(self):
        self.__ftpConnexionClose()

    def __str__(self):
        print('  ** FTP Credentials: {}|{}|{}|{}|'.format(self.__str_host, self.__str_uid, self.__str_pwd, self.__int_portnumber))
        
    def __ftpConnexionClose(self):
        print(' ** Closing FTP Connection: {}'.format(self.__str_host))
        self.l_Folder = []
        try:    
            self.o_ftpConnexion.quit()  
            self.o_ftpConnexion.close()
        except: pass

    # ========== CONNEXION ==============================
    def __ftpClassic_Connect(self):
        try:
            if self.__int_timeOut <= 0:
                ftp_connect = ftplib.FTP(self.__str_host)
            else:
                ftp_connect = ftplib.FTP(self.__str_host, timeout = self.__int_timeOut)
            ftp_connect.login(user = self.__str_uid, passwd = self.__str_pwd)
        except Exception as err:
            print(' ERROR: f_ftpConect in c_FTP | #{}#'.format(err))
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__int_timeOut )
            raise
        self.o_ftpConnexion = ftp_connect
        
    def __ftpSSL_Connect(self):
        try:
            ftp_connect = FTP_TLS_IgnoreHost(self.__str_host)
            if self.__int_timeOut <= 0:
                ftp_connect.connect(host = self.__str_host, port = self.__int_portnumber)
            else:
                ftp_connect.connect(host = self.__str_host, port = self.__int_portnumber, timeout = self.__int_timeOut)
            ftp_connect.auth()
            #            ftp_connect.set_debuglevel(1)  
            #            ftp_connect.set_pasv(True) 
            ftp_connect.login(user =  self.__str_uid, passwd = self.__str_pwd)
            ftp_connect.prot_p()
        except Exception as err:
            print(' ERROR: ftpSSL_Connect | #{}#'.format(err))
            print(' - ' + self.__str_host, self.__str_uid, self.__str_pwd, ' | Port: ', self.__int_portnumber)
            raise
        self.o_ftpConnexion = ftp_connect

    def __message_ConnexionLost(self):
        if self.__bl_msgLosingConnection:
            print(' ** FTP Connection LOST: {}'.format(self.__str_host))
        # This way, if connexion is not found, we have message Connection is lost
        self.__bl_msgLosingConnection = True
        # If we lose the connexion, we need to reset the folder to Null
        self.l_Folder = []

    def ftp_Connect(self, str_host, str_uid, str_pwd, bl_ssl = False, int_timeOut = -1, int_portnumber = 21):
        if self.__str_host == str_host and self.__str_uid == str_uid and self.__str_pwd == str_pwd and self.__bl_ssl == bl_ssl:
            try:
                ftpConnexion = self.o_ftpConnexion                
                # print(' FTP: An existing connexion already exist and will be used again | Server: {}'.format(ftpConnexion.host))
                return ftpConnexion
            except: self.__message_ConnexionLost()
        else:
            self.__ftpConnexionClose()          # Even if connexion NOT exist, does not matter as it will pass on expect of the function
            self.__init__(str_host, str_uid, str_pwd, bl_ssl, int_timeOut, int_portnumber) # Init the variables
        # CONNECT
        try:
            if self.__bl_ssl:   self.__ftpSSL_Connect() 
            else:               self.__ftpClassic_Connect()
        except Exception as err:
            self.__init__(str_host.replace(' ', ''), str_uid.replace(' ', ''), str_pwd.replace(' ', ''), bl_ssl, int_timeOut, int_portnumber)
            if self.__bl_ssl:   self.__ftpSSL_Connect() 
            else:               self.__ftpClassic_Connect()
            print(' WARNING: A parameter in the FTP must have a space in it, please remove it ! | #{}#'.format(err))
        return self.o_ftpConnexion
    # ==================================================
    
    
    def ftp_changeFolder(self, l_Folder):
        # Was the past connexion already on some folder ?
        try:        l_pastSessionFolder = self.l_Folder
        except:     l_pastSessionFolder = []
        # if Past Folder List is the same than the one now: DO NOTHING
        if l_Folder == l_pastSessionFolder:     return True
        # Run the List of Folder BACKWARD to go back to root
        try:
            for str_folder in l_pastSessionFolder:
                if not str_folder == None:
                    self.o_ftpConnexion.cwd("../")
        except Exception as err:
            print(' ERROR: ftp_changeFolder, FTP could not change backwards folder | #{}#'.format(err))
            print(' - ', l_Folder)
        # Run the List of Folder
        try:
            for str_folder in l_Folder:
                if not str_folder == None:
                    self.o_ftpConnexion.cwd(str_folder)
        except Exception as err:
            print(' ERROR: ftp_changeFolder, FTP could not change folder | #{}#'.format(err))
            print(' - ', l_Folder)
            try:    print(' - ', str_folder)
            except: pass
            self.__str__()        
        # Fin: Assign the folder to a variable to check up later
        self.l_Folder = l_Folder

    def fL_fileInFTP_beforeDownload(self):
        # Even if we lose connection we will keep the list of files inside the DIC
        # only way to update this list is to CLOSE the App
        try:
            d_ListFiles = self.__d_ListFiles
            l_ftpID = (self.__str_host, self.__str_uid, self.__str_pwd, '|'.join(self.l_Folder))
            if l_ftpID in d_ListFiles:
                self.l_nameFiles = d_ListFiles[l_ftpID]
            else:
                try:
                    self.l_nameFiles = self.o_ftpConnexion.nlst()
                except:
                    return None
                d_ListFiles[l_ftpID] = self.l_nameFiles
                self.__d_ListFiles = d_ListFiles
        except Exception as err:
            print(' ERROR in fL_fileInFTP_beforeDownload | {}'.format(err))
            raise
        return self.l_nameFiles

    def fL_fileInFTP(self):
        try:    self.l_nameFiles = self.o_ftpConnexion.nlst()
        except:
            print(' ERROR in fL_fileInFTP')
            raise
        return self.l_nameFiles
        
    def fL_fileInFTP_wCharac(self):
        try:    self.l_nameFiles_wCharac = self.o_ftpConnexion.retrlines('LIST')
        except:
            print(' ERROR in fL_fileInFTP_wCharac')
            raise
        return self.l_nameFiles_wCharac
    
    def ftp_DownloadFile(self, str_fileName, str_folder):
        # Create the file
        try:
            Open_file = open(os.path.join(str_folder, str_fileName), 'wb')
        except:
            print(' ERROR in ftp_DownloadFile - Creation of the file')
            print(' - ', str_folder, str_fileName)
            raise
        # Fill the file with whats in FTP
        try:
            self.o_ftpConnexion.retrbinary('RETR {}'.format(str_fileName), Open_file.write)
        except Exception as err:  
            print(' ERROR in ftp_DownloadFile - retrbinary | {}'.format(str(err)))
            print(' - ', str_folder, str_fileName)
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__bl_ssl, self.__int_timeOut, self.__int_portnumber)
            Open_file.close()
            # delete the file
            fl.del_fichier(str_folder, str_fileName)
            raise
        Open_file.close()
        
    def ftp_UploadFile(self, str_fileName, str_folder):
        # Create the file
        try:
            Open_file = open(os.path.join(str_folder, str_fileName), 'rb')
        except:
            print(' ERROR in ftp_UploadFile - Opening of the file')
            print(' - ', str_folder, str_fileName)
            raise
        # Fill the file with whats in FTP
        try:
            self.o_ftpConnexion.storbinary('STOR {}'.format(str_fileName), Open_file)
        except Exception as err:
            Open_file.close()
            print(' ERROR in ftp_UploadFile - storbinary | {}'.format(str(err)))
            print(' - ', str_folder, str_fileName)
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__bl_ssl, self.__int_timeOut, self.__int_portnumber)
            raise
        Open_file.close()
        # Rename tmp files...
        try:
            if str_fileName.lower()[-4:] == '.tmp':
                str_newName = RenameTMPfile(str_fileName)
                self.ftp_renameAfterUpload(str_fileName, str_newName)
        except: pass
        return True
    
    def ftp_renameAfterUpload(self, str_oldName, str_newName):
        try:
            self.o_ftpConnexion.rename(str_oldName, str_newName)
        except Exception as err:
            print(' ERROR in ftp_renameAfterUpload - rename | {}'.format(str(err)))
            print(' (-) ', str_oldName, ' |=>| ', str_newName)
        return True
    

  
        
# ------------- SFTP ----------------------------------------
@oth.dec_singletonsClass
class c_SFTP():
    def __init__(self, str_host, str_uid, str_pwd, int_timeOut = -1, int_portnumber = 22):
        self.__str_host = str_host
        self.__str_uid = str_uid
        self.__str_pwd = str_pwd
        self.l_Folder = []
        self.__int_timeOut = int_timeOut
        self.__bl_msgLosingConnection = False
        self.__d_ListFiles = {}
        if int_portnumber is None:  self.__int_portnumber = 22
        else:                       self.__int_portnumber = int_portnumber
        
    def __del__(self):
        self.__sftpConnexionClose()
        
    def __sftpConnexionClose(self, bl_closingMsg = True):
        # MESSAGE
        if bl_closingMsg:
            print(' ** Closing SFTP Connection: {}'.format(self.__str_host))        
        # If we lose the connexion, we need to reset the folder to Null
        self.l_Folder = []
        try:    self.o_sftpOpen.close()
        except: pass
        try:    self.o_sftpConnexion.close()
        except: pass
    
    def __message_ConnexionLost(self):
        if self.__bl_msgLosingConnection:      
            print(' ** SFTP Connection LOST: {}'.format(self.__str_host))
        # This way, if connexion is not found, we have message Connection is lost
        self.__bl_msgLosingConnection = True
        # If we lose the connexion, we need to reset the folder to Null
        self.l_Folder = []
    
    # ========== CONNEXION ==============================
    def sftp_Connect(self, str_host, str_uid, str_pwd, int_timeOut = -1, int_portnumber = 22):
        if self.__str_host == str_host and self.__str_uid == str_uid and self.__str_pwd == str_pwd:
            try:
                sftpConnexion = self.o_sftpConnexion
                sftp_oppen = self.o_sftpOpen
                return sftp_oppen
                print(' SFTP: An existing connexion already exists and will be used again | Server: {}'.format(sftpConnexion))
            except:     self.__message_ConnexionLost()
        else:
            self.__sftpConnexionClose(bl_closingMsg = True)
            self.__init__(str_host, str_uid, str_pwd, int_timeOut, int_portnumber) # Init the variables
        # CONNECT
        try:
            ssh_Client = pmiko.SSHClient()
            ssh_Client.set_missing_host_key_policy(pmiko.AutoAddPolicy())
            ssh_Client.load_system_host_keys()
            if int_portnumber == -1:    ssh_Client.connect(str_host, username = str_uid, password = str_pwd)
            else:                       ssh_Client.connect(str_host, username = str_uid, password = str_pwd, port = self.__int_portnumber)
            self.o_sftpConnexion = ssh_Client
        except:
            print(' ERROR in sftp_Connect (PARAMIKO)')
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__int_portnumber)
            raise
        # OPEN
        try:
            sftp_oppen = self.o_sftpConnexion.open_sftp()
            self.o_sftpOpen = sftp_oppen
        except:
            print(' ERROR in sftp_Connect - Open SFTP')
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__int_portnumber)
            raise
        # Return
        return self.o_sftpOpen
    # ==================================================    
    
    def __checkFolder(self):
        # Define what was the last Folder we are in
        try:        l_pastSessionFolder = self.l_Folder
        except:     return []
        if l_pastSessionFolder == []:       return []
        if l_pastSessionFolder == ['']:     return []
        str_pastSessionFolder = '/' + '/'.join(l_pastSessionFolder)
        if str_pastSessionFolder == '/':    return []
        # Check Current Sesion is really like Past Session
        str_currentFolder = self.o_sftpOpen.getcwd()
        if str_currentFolder is None:
            print('   ** SFTP has lost its current folder (None), we need to chDir again on : {}'.format(l_pastSessionFolder))
            l_pastSessionFolder = []
        elif str_pastSessionFolder != str_currentFolder:
            print('   ** SFTP has lost its folder (is currently in: {}, past session on : {})'.format(str_currentFolder, l_pastSessionFolder))
            l_pastSessionFolder = []
        return l_pastSessionFolder
    
    def sftp_changeFolder(self, l_Folder):
        l_pastSessionFolder = self.__checkFolder()
        # if Past Folder List is the same than the one now: DO NOTHING
        if l_Folder == l_pastSessionFolder:     
            return True
        # Run the List of Folder BACKWARD to go back to root
        try:
            for str_folder in l_pastSessionFolder:
                if not str_folder == None:
                    if not str_folder == '':
                        print('  -- Folder going backwards on folder: ', str_folder)
                        self.o_sftpOpen.chdir("../")
        except:
            print(' ERROR: sftp_changeFolder, SFTP could not change backwards folder')
            print(' - l_Folder', l_Folder)
            print(' - l_pastSessionFolder', l_pastSessionFolder)
        # Run the List of Folder
        try:
            for str_folder in l_Folder:
                if not str_folder == None:
                    if not str_folder == '':
                        self.o_sftpOpen.chdir(str_folder)
        except:
            print(' ERROR: sftp_changeFolder, SFTP could not change folder')
            print(' - l_Folder', l_Folder)
            try:    print('  - str_folder', str_folder)
            except: pass
            try:    
                print('  - SFTP is in the folder:')
                print('     |{}|'.format(self.o_sftpOpen.getcwd()))
            except: pass
        # Fin: Assign the folder to a variable to check up later
        self.l_Folder = l_Folder
        
    
    def sftp_DownloadFile(self, str_fileName, str_folder):
        try:
            self.o_sftpOpen.get(str_fileName, os.path.join(str_folder, str_fileName))
        except Exception as err:
            print(' ERROR in sftp_DownloadFile - get : {}'.format(str(err)))
            print(' - ', str_fileName)
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__int_timeOut, self.__int_portnumber)
            # print(' - Files available in FTP', self.fL_fileInSFTP())
            # delete the file
            fl.del_fichier(str_folder, str_fileName)
            #self.__sftpConnexionClose()
            raise
        # END
        return True
        
    def sftp_UploadFile(self, str_fileName, str_folder):
        try:
            self.o_sftpOpen.put(os.path.join(str_folder, str_fileName), str_fileName)
        except Exception as err:
            print(' ERROR in sftp_UploadFile - put : {}'.format(str(err)))
            print(' - ',  str_fileName)
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__int_timeOut, self.__int_portnumber)
            #self.__sftpConnexionClose()
            raise
        # Rename tmp files...
        try:
            if str_fileName.lower()[-4:] == '.tmp':
                str_newName = RenameTMPfile(str_fileName)
                self.sftp_renameAfterUpload(str_fileName, str_newName)
        except: pass
        return True
    
    def sftp_renameAfterUpload(self, str_oldName, str_newName):
        try:
            a = self.o_sftpConnexion.open_sftp()
            a.put(os.path.join(str_oldName, str_oldName), str_oldName)
            self.o_sftpOpen.rename(str_oldName, str_newName)
        except Exception as err:
            print(' ERROR in sftp_renameAfterUpload - rename | {}'.format(str(err)))
            print(' - ', str_oldName, str_newName)
        return True
        
    def fL_fileInSFTP_beforeDownload(self):
        # Even if we lose connection we will keep the list of files inside the DIC
        try:
            d_ListFiles = self.__d_ListFiles
            l_sftpID = (self.__str_host, self.__str_uid, self.__str_pwd, '|'.join(self.l_Folder))
            if l_sftpID in d_ListFiles:
                self.l_nameFiles = d_ListFiles[l_sftpID]
            else:
                try:    self.l_nameFiles = self.o_sftpOpen.listdir()
                except: return None
                d_ListFiles[l_sftpID] = self.l_nameFiles
                self.__d_ListFiles = d_ListFiles
        except Exception as err:
            print(' ERROR in fL_fileInSFTP | {}'.format(err))
            raise
        return self.l_nameFiles
    
    def fL_fileInSFTP(self):
        try:
            self.l_nameFiles = self.o_sftpOpen.listdir()
        except Exception as err:
            print(' ERROR in fL_fileInSFTP | {}'.format(err))
            raise
        return self.l_nameFiles
    
    def fL_fileInSFTP_wCharac(self):
        try:    
            l_Files = self.o_sftpOpen.listdir_attr()
            l_Files = [file for file in l_Files if '.' in file.filename]
            self.l_nameFiles_wCharac = l_Files
        except:
            print(' ERROR in fL_fileInSFTP_wCharac')
            raise
        return self.l_nameFiles_wCharac
    



#---------------------------------------------------------------
# ------ LEGACY: Function to launch Class ------------------
#---------------------------------------------------------------
def RenameTMPfile(str_fileName):
    str_newName = str_fileName.replace('.tmp', '')
    if not str_newName.lower()[-4:] in ['.csv', '.txt']:
        str_newName = str_newName + '.csv'
    return str_newName

def ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl = False, int_timeout = -1, bl_message = False):
    inst_ftp = c_FTP(str_host, str_uid, str_pwd, bl_ssl, int_timeout)
    inst_ftp.ftp_Connect(str_host, str_uid, str_pwd, bl_ssl, int_timeout)   # Carry out check if nay of this vraiables changed
    inst_ftp.ftp_changeFolder(l_ftpFolder)
    return inst_ftp

def ftp_listFolder_bfDwload(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, bl_ssl = False):
    try:
        inst_ftp = c_FTP(str_host, str_uid, str_pwd, bl_ssl, int_timeout)
        l_nameFiles = inst_ftp.fL_fileInFTP_beforeDownload()
        if l_nameFiles is None: raise
    except:
        inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout)
        l_nameFiles = inst_ftp.fL_fileInFTP_beforeDownload()
    return l_nameFiles

def ftp_listFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, bl_ssl = False):
    inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout, bl_message = 'ftp_listFolder')
    l_nameFiles = inst_ftp.fL_fileInFTP()
    return l_nameFiles

def ftp_printListFile_wCharac(str_host, str_uid, str_pwd,l_ftpFolder, int_timeout = -1, bl_ssl = False):
    inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout)
    l_nameFiles = inst_ftp.fL_fileInFTP_wCharac()
    return l_nameFiles
    
def fBl_ftpDownFileBinary(str_host, str_uid, str_pwd,l_ftpFolder, str_fileName, str_folder, int_timeout = -1, bl_ssl = False):
    inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout, bl_message = 'fBl_ftpDownFileBinary')
    inst_ftp.ftp_DownloadFile(str_fileName, str_folder)
    return True

def fBl_ftpUpFile_Bi(str_host, str_uid, str_pwd,l_ftpFolder, str_fileName, str_folder, int_timeout = -1, bl_ssl = False):
    inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout, bl_message = True)
    inst_ftp.ftp_UploadFile(str_fileName, str_folder)
    return True
    


# ------------- SFTP ----------------------------------------
def sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, int_port = None):
    inst_sftp = c_SFTP(str_host, str_uid, str_pwd, int_timeout, int_portnumber = int_port)
    inst_sftp.sftp_Connect(str_host, str_uid, str_pwd, int_timeout, int_portnumber = int_port)
    inst_sftp.sftp_changeFolder(l_ftpFolder)
    return inst_sftp

def ssh_downFile(str_host, str_uid, str_pwd, l_ftpFolder, str_fileName, str_folder, int_timeout = -1, int_port = None):
    inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
    inst_sftp.sftp_DownloadFile(str_fileName, str_folder)
    return True
    
def ssh_upFile(str_host, str_uid, str_pwd, l_ftpFolder, str_fileName, str_folder, int_timeout = -1, int_port = None):   
    inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
    inst_sftp.sftp_UploadFile(str_fileName, str_folder)
    return True

def ssh_listFilesInFolder_bfDwload(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, int_port = None):
    try:
        inst_sftp = c_SFTP(str_host, str_uid, str_pwd, int_timeout, int_portnumber = int_port)
        l_nameFiles = inst_sftp.fL_fileInSFTP_beforeDownload()
        if l_nameFiles is None: raise
    except:
        inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
        l_nameFiles = inst_sftp.fL_fileInSFTP_beforeDownload()
    return l_nameFiles

def ssh_listFilesInFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, int_port = None):
    inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
    l_nameFiles = inst_sftp.fL_fileInSFTP()
    return l_nameFiles

def ssh_listFilesInFolder_wCharac(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, int_port = None):
    inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
    l_nameFiles = inst_sftp.fL_fileInSFTP_wCharac()
    return l_nameFiles

def ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, int_port = None):
    l_Files = ssh_listFilesInFolder_wCharac(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
    try:
        l_dteModified = [file.st_mtime for file in l_Files]
        argMax_LastDate = np.argmax(l_dteModified)
    except:
        print(' ERROR in ssh_getLastFile_inFolder')
        print(' - ', str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
        raise
    return l_Files[argMax_LastDate]

def ssh_getLastFile_inFolder_name(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, int_port = None):
    file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
    return file.filename
    
def ssh_getLastFile_inFolder_date(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, int_port = None):
    file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
    return dat.fDte_formatToTimeStamp(file.st_mtime)

def ssh_getLastFile_inFolder_size(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, int_port = None):
    file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout, int_port)
    return file.st_size
#-----------------------------------------------------------------
