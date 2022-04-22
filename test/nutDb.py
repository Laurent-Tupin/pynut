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
    def defineCredentials(self, **d_param):
        self.__server = d_param['server']
        self.__database = d_param['database']
        self.__uid = d_param['uid']
        self.__pwd = d_param['pwd']
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
        t_keyConnect = (self.__server, self.__database, self.__uid)
        try:
            if t_keyConnect not in self.__dict_Connect:
                # NEW connexion
                self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + self.__server +
                                           ';DATABASE=' + self.__database +
                                           ';UID=' + self.__uid +
                                           ';PWD=' + self.__pwd,
                                           timeout = self.__timeout)
                # trusted_connection=YES;  for Windows Authentification
                # Save the connexion in a dico with KEY = ID in tuple
                self.__dict_Connect[t_keyConnect] = self.cnxn
                self.t_keyConnect_Current = t_keyConnect  # Keep in mind for the next Connexion
            elif self.t_keyConnect_Current != t_keyConnect:
                self.cnxn = self.__dict_Connect[t_keyConnect]
                self.t_keyConnect_Current = t_keyConnect  # Keep in mind the last Connexion
            elif self.__dict_Connect[t_keyConnect] == -1:
                # raise
                return False
            else:   pass
            # CURSOR
            self.cursor = self.cnxn.cursor()
        except Exception as err:
            self.__str__(' ERROR: Your db connexion is not working || {}'.format(err))
            raise

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
            self.cursor.close()
            del self.cursor
        except: pass
        try:    self.cnxn.close()
        except: pass

    def __del__(self):
        self.closeConnection()



@oth.dec_singletonsClass
class c_db_sqlServ_single(c_db_sqlServer):
    """ This inehrit from c_db_sqlServer and is a singleton"""
    def __init__(self):
        super().__init__()


@oth.dec_singletonsClass
class c_db_dataframeCred(c_db_sqlServer):
    """ This inehrit from c_db_sqlServer and is a singleton
    Manage the Credentials in a dataframe form"""
    def __init__(self):
        super().__init__()





#---------------------------------------------------------------
#----- Function to launch the Class ----------------------------
#---------------------------------------------------------------
def db_defineInstance():
    inst_db = c_db_sqlServer()
    return inst_db

def db_DefineConnectCursor(str_req, **d_credentials):
    db_sqlServer = c_db_sqlServer()
    db_sqlServer.defineCredentials(**d_credentials)
    db_sqlServer.request = str_req
    db_sqlServer.connect()
    return True

def db_EXEC(str_req, **d_credentials):
    db_sqlServer = c_db_sqlServer()
    db_DefineConnectCursor(str_req, **d_credentials)
    db_sqlServer.executeReq()
    db_sqlServer.commit()
    return True

def db_SelectReq(str_req, **d_credentials):
    db_sqlServer = c_db_sqlServer()
    db_DefineConnectCursor(str_req, **d_credentials)
    db_sqlServer.getDataframe()
    db_sqlServer.db_Commit()
    return db_sqlServer.df_result

def db_MultipleReq(str_req, **d_credentials):
    db_sqlServer = c_db_sqlServer()
    db_DefineConnectCursor(str_req, **d_credentials)
    db_sqlServer.executeReq()
    db_sqlServer.getDataframe_multipleReq()
    db_sqlServer.db_Commit()
    return db_sqlServer.df_result


#-------------------------------------------------------------------------------------------------------------
# Read DB, Save into CSV and read CSV after that (avoid connexion to the same DB several times)
#-------------------------------------------------------------------------------------------------------------
def fDf_readDB_orReadCsv(str_req, str_csvName, int_dayToKeep, str_folderCsv, bl_AlertIfEmptyReq = True):
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
