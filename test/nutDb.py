try:
    from . import _lib as lib
    from . import nutFiles as fl
    from . import nutDate as dat
    from . import nutOther as oth
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
os = lib.os()
pd = lib.pandas()
pyodbc = lib.pyodbc()
lite =   lib.sqlite3()



#---------------------------------------------------------------
#------------- CLASS DB management -----------------------------
#---------------------------------------------------------------
@oth.dec_singletonsClass
class c_db_lite:
    """ This class allows you to manage simple lite database"""
    def __init__(self):
        self.str_pathDb = None
        self.cnxn = None
    def definePath(self, str_pathDb):
        self.str_pathDb = str_pathDb
    def connect(self):
        cnxn = lite.connect(self.str_pathDb)
        self.cnxn = cnxn
    def getDataframe(self, str_req):
        df_req = pd.read_sql_query(str_req, self.cnxn)
        self.df_req = df_req
        return df_req
    def closeConnection(self):
        try:    self.cnxn.close()
        except: pass
        self.cnxn = None
    def __del__(self):
        self.closeConnection()



class c_db_sqlServer:
    def __init__(self):
        self.__dict_Connect = {}
        self.__bl_AlertIfEmptyReq = True
        self.__timeout = 100
        self.__request = 'Request not defined'
        self.cnxn = None
        self.cursor = None
    def defineCredentials(self, **d_param):
        if 'server' in d_param:
            self.__server =     d_param['server']
        if 'database' in d_param:
            self.__database =   d_param['database']
        if 'uid' in d_param:
            self.__uid =        d_param['uid']
        if 'pwd' in d_param:
            self.__pwd =        d_param['pwd']
        if 'timeout' in d_param:
            self.__timeout = d_param['timeout']
        if 'bl_AlertIfEmptyReq' in d_param:
            self.__bl_AlertIfEmptyReq = d_param['bl_AlertIfEmptyReq']
    @property
    def server(self):
        return self.__server
    @property
    def database(self):
        return self.__database
    @property
    def uid(self):
        return self.__uid
    @property
    def pwd(self):
        return self.__pwd
    @property
    def timeout(self):
        return self.__timeout
    @property
    def request(self):
        return self.__request
    @request.setter
    def request(self, str_request = ''):
        if str_request != '':
            self.__request = str_request

    def __str__(self, message = ''):
        str_msg = '--------------------------------------\n'
        str_msg += '  - |{}|, |{}|, |{}| \n'.format(self.__server, self.__database, self.__uid)
        str_msg += '  - |{}| \n'.format(self.__request)
        str_msg += '  - {} \n'.format(message)
        str_msg += '--------------------------------------'
        print(str_msg)
        return str_msg

    def connect(self):                  # db_sqlConnectCursor
        i_cnxReturn = 0
        t_keyConnect = (self.__server, self.__database, self.__uid)
        if t_keyConnect not in self.__dict_Connect:
            #----------------------------------------------------------------------------------
            # NEW connexion
            try:
                self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + self.__server +
                                           ';DATABASE=' + self.__database +
                                           ';UID=' + self.__uid +
                                           ';PWD=' + self.__pwd,
                                           timeout = self.__timeout)
                # trusted_connection=YES;  for Windows Authentification
                # Save the connexion in a dico with KEY = ID in tuple0
            except Exception as err:
                self.__str__(' ERROR: Your db connexion is not working || {} || {}'.format(err, str(i_cnxReturn)))
                raise
            # ----------------------------------------------------------------------------------
            self.__dict_Connect[t_keyConnect] = self.cnxn
            # Keep in mind for the next Connexion
            self.t_keyConnect_Current = t_keyConnect
            i_cnxReturn = 2
        elif self.t_keyConnect_Current != t_keyConnect:
            self.cnxn = self.__dict_Connect[t_keyConnect]
            # Keep in mind for the next Connexion
            self.t_keyConnect_Current = t_keyConnect
            i_cnxReturn = 3
        # elif self.__dict_Connect[t_keyConnect] == -1:
        #     # raise
        #     i_cnxReturn = -1
        #     return i_cnxReturn
        else:
            i_cnxReturn = 1
            return i_cnxReturn
        # CURSOR
        try:    self.cursor = self.cnxn.cursor()
        except Exception as err:
            self.__str__(' ERROR: Your db CURSOR is not working || {} || {}'.format(err, str(i_cnxReturn)))
            raise
        # END
        return i_cnxReturn

    def availablePyodbcDrivers(self):       # db_seeDriversAvailable
        self.__drivers = pyodbc.drivers()
        return self.__drivers

    def executeReq(self):                   # db_Execute
        try:    self.cursor.execute(self.__request)
        except Exception as err:
            self.__str__(' ERROR: executeReq is not working || {}'.format(err))
            raise

    def commit(self):                       # db_Commit
        try:    self.cnxn.commit()
        except Exception as err:
            self.__str__(' ERROR: commit is not working || {}'.format(err))
            raise

    def getDataframe(self):                 # getDataFrame_fReq
        self.df_result = False
        try:
            self.df_result = pd.read_sql(self.__request, self.cnxn)
            # Message if request is empty
            if self.__bl_AlertIfEmptyReq is True:
                if self.df_result.empty or self.df_result.dropna(how='all').empty:
                    self.__str__(' EMPTY: getDataframe is empty')
        except Exception as err:
            self.__str__(' ERROR: getDataframe is not working || {}'.format(err))
            raise
        return self.df_result

    def getDataframe_multipleReq(self):
        self.df_result = False
        try:
            l_resultSet =   self.cursor.fetchall()
            df_resultSet =  pd.DataFrame.from_records(l_resultSet)
            while ( self.cursor.nextset() ):
                l_resultSet =       self.cursor.fetchall()
                df_resultSet_Suiv = pd.DataFrame.from_records(l_resultSet)
                df_resultSet =      self.fDf_Concat(df_resultSet, df_resultSet_Suiv)
            # Final Result
            self.df_result =      df_resultSet
            # Message if empty
            if self.__bl_AlertIfEmptyReq is True:
                if self.df_result.empty or self.df_result.dropna(how = 'all').empty:
                    self.__str__(' EMPTY: getDataframe is empty')
        except Exception as err:
            self.__str__(' ERROR: getDataframe_multipleReq is not working || {}'.format(err))
            raise
        return self.df_result

    @classmethod
    def fDf_Concat(cls, df1, df2):
        try:
            if len(df1.columns) >= len(df2.columns):
                df2.columns = df1.columns[:len(df2.columns)]
                df_return = pd.concat([df1, df2], ignore_index=True)
                df_return = df_return[df1.columns]
            else:
                df2.columns = list(df1.columns) + list(df2.columns[len(df1.columns):])
                df_return = pd.concat([df1, df2], ignore_index=True)
                df_return = df_return[df2.columns]
        except:
            df_return = False
        return df_return

    def closeConnection(self):
        try:
            self.__dict_Connect = {}
            self.__str__(' INFO: Your db connexion is closing !')
        except: pass
        try:
            self.cursor.close()
            del self.cursor
        except: pass
        try:    self.cnxn.close()
        except: pass
        try:    self.cnxn = None
        except: pass
    def __del__(self):
        self.closeConnection()


@oth.dec_singletonsClass
class c_db_sqlServ_single(c_db_sqlServer):
    """ This inehrit from c_db_sqlServer and is a singleton"""
    def __init__(self):
        super().__init__()


class c_db_dfCredentials(c_db_sqlServer):
    """ This inehrit from c_db_sqlServer and is a singleton
    Manage the Credentials in a dataframe form"""
    def __init__(self):
        super().__init__()
    def dataframeCredentials(self, df_UID):
        self.df_UID = df_UID
        # Get the columns of the UID given the order of columns are: Server, database, UID, Password
        l_columns = df_UID.columns
        self.serverColName =    l_columns[0]
        self.databaseColName =  l_columns[1]
        self.uidColName =       l_columns[2]
        self.pwdColName =       l_columns[3]
        try:
            str_server =     df_UID[self.serverColName].values[0]
            str_database =   df_UID[self.databaseColName].values[0]
            str_uid =        df_UID[self.uidColName].values[0]
            str_pwd =        df_UID[self.pwdColName].values[0]
        except:
            self.serverColName = 'Server'
            self.databaseColName = 'Database'
            self.uidColName = 'Uid'
            self.pwdColName = 'Password'
            str_server =    df_UID[self.serverColName].values[0]
            str_database =  df_UID[self.databaseColName].values[0]
            str_uid =       df_UID[self.uidColName].values[0]
            str_pwd =       df_UID[self.pwdColName].values[0]
        # Keep in memory the last working server
        self.__last_server = str_server
        # Set the value by the original Class
        d_param = dict(server=str_server, database=str_database, uid=str_uid,pwd=str_pwd)
        self.defineCredentials(**d_param)
    def change_server(self, str_server = ''):
        if not str_server == '':
            df_UID = self.df_UID
            try:
                str_database =   df_UID.loc[df_UID[self.serverColName] == str_server, self.databaseColName].values[0]
                str_uid =        df_UID.loc[df_UID[self.serverColName] == str_server, self.uidColName].values[0]
                str_pwd =        df_UID.loc[df_UID[self.serverColName] == str_server, self.pwdColName].values[0]
            except Exception as err:
                print('ERROR in change_server: we could not find the server: |{}| in the Dataframe provided \n'.format(str_server))
                print(df_UID)
                return False
            # Keep in memory the last working server
            self.__last_server = str_server
            # Set the value by the original Class
            d_param = dict(server=str_server, database=str_database, uid=str_uid, pwd=str_pwd)
            self.defineCredentials(**d_param)
        return True
    def change_database(self, str_database = ''):
        if not str_database == '':
            df_UID = self.df_UID
            str_server = self.__last_server
            str_uid = df_UID.loc[df_UID[self.serverColName] == str_server, self.uidColName].values[0]
            str_pwd = df_UID.loc[df_UID[self.serverColName] == str_server, self.pwdColName].values[0]
            # Set the value by the original Class
            d_param = dict(server=str_server, database=str_database, uid=str_uid, pwd=str_pwd)
            self.defineCredentials(**d_param)
        return True


@oth.dec_singletonsClass
class c_db_dataframeCred(c_db_dfCredentials):
    """ This inehrit from c_db_dfCredentials + is a singleton"""
    def __init__(self):
        super().__init__()


@oth.dec_singletonsClass
class c_db_withLog(c_db_dfCredentials):
    """ This inehrit from c_db_dfCredentials + is a singleton
    Allow you to manage some Log request inside a particular server and database
    without changing the connection of the other requests"""
    def __init__(self):
        super().__init__()
        self.__server_default = None
    def dataframeCredentials(self, df_UID):
        super().dataframeCredentials(df_UID)
        self.__server_default =     self.server
        self.__database_default =   self.database
        self.__uid_default =        self.uid
        self.__pwd_default =        self.pwd
    def change_server(self, str_server = ''):
        super().change_server(str_server)
        if not str_server == '':
            self.__server_default =     self.server
            self.__database_default =   self.database
            self.__uid_default =        self.uid
            self.__pwd_default =        self.pwd
    def define_Log_Cred(self, str_serverForLog = None, str_databaseForLog = None):
        df_UID = self.df_UID
        self.server_Log =       str_serverForLog
        self.db_Log =           str_databaseForLog
        self.__uid_Log =        df_UID.loc[df_UID[self.serverColName] == self.server_Log, self.uidColName].values[0]
        self.__pwd_Log =        df_UID.loc[df_UID[self.serverColName] == self.server_Log, self.pwdColName].values[0]
    def executeLog(self, str_logExec = ''):
        d_pLog = dict(server=self.server_Log, database=self.db_Log, uid=self.__uid_Log, pwd=self.__pwd_Log)
        self.defineCredentials(**d_pLog)
        self.request = str_logExec
        self.connect()
        self.executeReq()
        self.commit()
        # Go back to the original Credentials
        d_pDefault = dict(server=self.__server_default, database=self.__database_default, uid=self.__uid_default, pwd=self.__pwd_default)
        self.defineCredentials(**d_pDefault)




#---------------------------------------------------------------
#----- Function to launch the Class ----------------------------
#---------------------------------------------------------------
def db_defineInstance():
    dbServer = c_db_withLog()
    return dbServer

def db_DefineConnectCursor(str_req, df_UID=None, t_logId=None):
    dbServer = c_db_withLog()
    if not df_UID is None:
        dbServer.dataframeCredentials(df_UID)
    if not t_logId is None:
        dbServer.define_Log_Cred(str_serverForLog=t_logId(0), str_databaseForLog=t_logId(1))
    dbServer.request = str_req
    dbServer.connect()
    return True

def db_EXEC(str_req, df_UID = None, t_logId = None):
    dbServer = c_db_withLog()
    db_DefineConnectCursor(str_req, df_UID, t_logId)
    if '{}.'.format(dbServer.db_Log).lower() in str_req.lower():
        print('  (**) Database will be {} for this request: \n   **{}**'.format(dbServer.db_Log, str_req))
        dbServer.executeLog(str_req)
    else:
        dbServer.executeReq()
        dbServer.commit()
    return True

def db_SelectReq(str_req, df_UID=None, t_logId=None, bl_AlertIfEmptyReq = True):
    dbServer = c_db_withLog()
    db_DefineConnectCursor(str_req, df_UID, t_logId)
    dbServer.defineCredentials(bl_AlertIfEmptyReq = bl_AlertIfEmptyReq)
    dbServer.getDataframe()
    dbServer.commit()
    return dbServer.df_result

def db_MultipleReq(str_req, df_UID=None, t_logId=None):
    dbServer = c_db_withLog()
    db_DefineConnectCursor(str_req, df_UID, t_logId)
    dbServer.executeReq()
    dbServer.getDataframe_multipleReq()
    dbServer.db_Commit()
    return dbServer.df_result




#-------------------------------------------------------------------------------------------------------------
# Read DB, Save into CSV and read CSV after that (avoid connexion to the same DB several times)
#-------------------------------------------------------------------------------------------------------------
@oth.dec_singletonsClass
class c_FolderCsv:
    def __init__(self):
        self.__folder = None
    @property
    def folder(self):
        return self.__folder
    @folder.setter
    def folder(self, str_folder=None):
        if not str_folder is None:
            self.__folder = str_folder

def fDf_readDB_orReadCsv(str_req, str_csvName, int_dayToKeep, str_folderCsv = None, bl_AlertIfEmptyReq = True):
    # Manage so you dont need to tell everytime the folder we are in
    if (str_folderCsv is None) or (str_folderCsv == ''):
        FolderCsv =     c_FolderCsv()
        str_folderCsv = FolderCsv.folder
    else:
        FolderCsv =         c_FolderCsv()
        FolderCsv.folder =  str_folderCsv

    # Boolean
    bl_fileExist =  False
    bl_fileTooOld = False

    # ----- Get the Path -----
    str_Path = os.path.join(str_folderCsv, str_csvName)

    # ----- Get the information : is the file exist / too old -----
    if fl.fBl_FileExist(str_Path):
        bl_fileExist = True
        if fl.fBl_fileTooOld(str_Path):
            bl_fileTooOld = True

    # ----- READ the FILE -----
    if bl_fileExist is True and bl_fileTooOld is False:
        try:
            df_return = pd.read_csv(str_Path, header=0)
            return df_return
        except Exception as err:
            print(' Warning in fDf_readDB_orReadCsv: (pd.read_csv) \n |{}| \n |{}| \n'.format(str_Path, err))
            bl_fileTooOld = True

    # ----- READ SQL information -----
    try:
        df_return = db_SelectReq(str_req, bl_AlertIfEmptyReq=bl_AlertIfEmptyReq)
    except Exception as err:
        # ----- CANT connect to SQL: Read the CSV even it is too old (AND DONT DELETE IT !!!) -----
        print(' Warning in fDf_readDB_orReadCsv (db_SelectReq): ')
        print('  ** CANT connect to SQL: Read the CSV even it is too old (AND DONT DELETE IT !!!)')
        print('  ** {}'.format(err))
        df_return = pd.read_csv(str_Path, header=0)
        return df_return

    # ----- Delete the file : too old -----
    if bl_fileExist is True and bl_fileTooOld is True:
        try:    fl.del_fichier_ifOldEnought(str_Path, '', int_dayToKeep)
        except: print(' Warning in db.fDf_readDB_orReadCsv: (os.delete) \n |{}| \n'.format(str_Path))

    # ----- Save the request on CSV -----
    try:    df_return.to_csv(str_Path, index=False, header=True)
    except: print(' Warning in db.fDf_readDB_orReadCsv: (df_return.to_csv) \n |{}| \n'.format(str_Path))

    return df_return
