import os
import pandas as pd
# import pytest
try:    import nutDb as db
except:
    print('Online Test...')
    from pyNut import nutDb as db
try:    import nutFiles as fl
except: from pyNut import nutFiles as fl



#=============================================================================
# function...
#=============================================================================
def fBl_liteAccessible(str_pathDb):
    if not fl.fBl_FolderExist(str_pathDb):
        print('You do not have access to the lite DB to test it: |{}|'.format(str_pathDb))
        return False
    return True

def fDf_lite_Launch():
    str_pathDb = r'C:\Users\laurent.tupin\Documents\GitLab\sola-pcf\db_param.db'
    if not fBl_liteAccessible(str_pathDb):
        return None
    str_req =       "SELECT * FROM tbl_connectSolaDb"
    db_lite =       db.c_db_lite()
    db_lite.definePath( str_pathDb )
    db_lite.connect()
    df_UID =        db_lite.getDataframe(str_req)
    db_lite.closeConnection()
    return df_UID



#=============================================================================
# UNIT TEST
#=============================================================================
def test_c_db_lite_singleton():
    db_lite = db.c_db_lite()
    db_lit2 = db.c_db_lite()
    db_lite.definePath('pathDb1')
    db_lit2.definePath('pathDb2')
    assert (db_lite.str_pathDb == db_lit2.str_pathDb)
    assert (db_lite.str_pathDb == 'pathDb2')
    db_lite.connect()
    assert (db_lite.cnxn is not None)
    assert (db_lit2.cnxn is not None)
    db_lit2.closeConnection()
    assert (db_lite.cnxn is None)
    assert (db_lit2.cnxn is None)

def test_c_db_sqlServer():
    dbServer = db.c_db_sqlServer()
    d_param = dict(server = '101', database = 'Test', uid = 'laurent', pwd = '**abc**')
    dbServer.defineCredentials( **d_param )
    dbServer.request = "SELECT * FROM Table"
    assert (dbServer is not None)

def test_c_db_sqlServ_single_singleton():
    dbServer = db.c_db_sqlServ_single()
    dbServe2 = db.c_db_sqlServ_single()
    d_param = dict(server='103', database='Test', uid='laurent', pwd='**abc**')
    dbServer.defineCredentials(**d_param)
    assert (dbServer.server == '103')
    assert (dbServe2.server == '103')
    d_para2 = dict(server='104', database='Prod', uid='Guillaume', pwd='**xyz**', timeout = 50, bl_AlertIfEmptyReq = False)
    dbServe2.defineCredentials(**d_para2)
    assert (dbServer.uid == 'Guillaume')
    assert (dbServe2.uid == 'Guillaume')
    assert (dbServer.timeout == 50)
    assert (dbServe2.timeout == 50)

def test_c_db_dataframeCred_singleton():
    dbServer = db.c_db_dataframeCred()
    dbServe2 = db.c_db_dataframeCred()
    d_param = dict(server='201', database='Test', uid='laurent', pwd='**abc**')
    dbServer.defineCredentials(**d_param)
    assert (dbServer.server == '201')
    assert (dbServe2.server == '201')
    d_para2 = dict(server='202', database='Prod', uid='Guillaume', pwd='**xyz**', timeout = 50, bl_AlertIfEmptyReq = False)
    dbServe2.defineCredentials(**d_para2)
    assert (dbServer.uid == 'Guillaume')
    assert (dbServe2.uid == 'Guillaume')
    assert (dbServer.timeout == 50)
    assert (dbServe2.timeout == 50)

def test_c_db_withLog_singleton():
    dbServer = db.c_db_withLog()
    dbServe2 = db.c_db_withLog()
    d_param = dict(server='301', database='Test', uid='laurent', pwd='**abc**')
    dbServer.defineCredentials(**d_param)
    assert (dbServer.server == '301')
    assert (dbServe2.server == '301')
    d_para2 = dict(server='302', database='Prod', uid='Guillaume', pwd='**xyz**', timeout = 50, bl_AlertIfEmptyReq = False)
    dbServe2.defineCredentials(**d_para2)
    assert (dbServer.uid == 'Guillaume')
    assert (dbServe2.uid == 'Guillaume')
    assert (dbServer.timeout == 50)
    assert (dbServe2.timeout == 50)



#=============================================================================
# FUNCTIONAL TEST
#=============================================================================
def test_c_db_lite_functionnal():
    str_pathDb = r'C:\Users\laurent.tupin\Documents\GitLab\sola-pcf\db_param.db'
    if not fBl_liteAccessible(str_pathDb):
        return None
    str_req = "SELECT * FROM tbl_connectSolaDb"
    db_lite = db.c_db_lite()
    db_lite.definePath(str_pathDb)
    assert(db_lite.str_pathDb == str_pathDb)
    db_lite.connect()
    assert (db_lite.cnxn is not None)
    df_UID =  db_lite.getDataframe(str_req)
    assert (isinstance(df_UID, pd.DataFrame))
    assert (isinstance(db_lite.df_req, pd.DataFrame))
    # assert (db_lite.df_req == df_UID)
    db_lite.closeConnection()
    assert (db_lite.cnxn is None)

def test_c_db_dataframeCred_dataframeCredentials():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_dataframeCred()
    dbServer.dataframeCredentials(df_UID)
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')

def test_c_db_withLog_dataframeCredentials():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_withLog()
    dbServer.dataframeCredentials(df_UID)
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')

def test_c_db_dataframeCred_change_server():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_dataframeCred()
    dbServer.dataframeCredentials(df_UID)
    # Wrong Server
    dbServer.change_server('WrongServer')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    # right Server
    dbServer.change_server('10.229.125.101')
    assert ('10.229.125.101' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcfReporting')

def test_c_db_withLog_change_server():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_withLog()
    dbServer.dataframeCredentials(df_UID)
    # Wrong Server
    dbServer.change_server('WrongServer')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    # right Server
    dbServer.change_server('10.228.117.59')
    assert ('10.228.117.59' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcfReporting')

def test_c_db_dataframeCred_change_database():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_dataframeCred()
    dbServer.dataframeCredentials(df_UID)
    # right Server
    dbServer.change_database('database_ppp')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'database_ppp')
    assert (dbServer.uid == 'pcf_reporting')

def test_c_db_withLog_change_database():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_withLog()
    dbServer.dataframeCredentials(df_UID)
    # right Server
    dbServer.change_database('database_ppp')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'database_ppp')
    assert (dbServer.uid == 'pcf_reporting')

def test_c_db_dataframeCred_connect():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_dataframeCred()
    dbServer.dataframeCredentials(df_UID)
    # Connect
    int_return = dbServer.connect()
    assert (int_return == 2)
    assert (dbServer.cnxn is not None)
    int_return = dbServer.connect()
    assert (int_return == 1)
    # New connection
    dbServer.change_server('10.229.125.101')
    int_return = dbServer.connect()
    assert (int_return == 2)
    # go back to old connection
    dbServer.change_server('D1PRDSOLADB.infocloud.local')
    int_return = dbServer.connect()
    assert (int_return == 3)
    # Close connection
    dbServer.closeConnection()
    assert (dbServer.cnxn is None)

def test_c_db_withLog_connect():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_withLog()
    dbServer.dataframeCredentials(df_UID)
    # Connect
    int_return = dbServer.connect()
    assert (int_return == 2)
    assert (dbServer.cnxn is not None)
    int_return = dbServer.connect()
    assert (int_return == 1)
    # New connection
    dbServer.change_server('10.229.125.101')
    int_return = dbServer.connect()
    assert (int_return == 2)
    # go back to old connection
    dbServer.change_server('D1PRDSOLADB.infocloud.local')
    int_return = dbServer.connect()
    assert (int_return == 3)
    # Close connection
    dbServer.closeConnection()
    assert (dbServer.cnxn is None)

def test_c_db_dataframeCred_request():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_dataframeCred()
    dbServer.dataframeCredentials(df_UID)
    dbServer.change_server('10.229.125.101')
    dbServer.change_database('SolaQC')
    dbServer.connect()
    dbServer.request = 'SELECT top 1 * FROM log ORDER BY [dtm_log]'
    dbServer.getDataframe()
    dbServer.commit()
    df_data = dbServer.df_result
    assert (df_data['str_user'].values[0] == 'laurent.tupin')
    assert (df_data['str_toolName'].values[0] == 'Sirius_PCF_dev.xlsb')

def test_c_db_withLog_request():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_withLog()
    dbServer.dataframeCredentials(df_UID)
    dbServer.change_server('10.229.125.101')
    dbServer.change_database('SolaQC')
    dbServer.connect()
    dbServer.request = 'SELECT top 1 * FROM log ORDER BY [dtm_log]'
    dbServer.getDataframe()
    dbServer.commit()
    df_data = dbServer.df_result
    assert (df_data['str_user'].values[0] == 'laurent.tupin')
    assert (df_data['str_toolName'].values[0] == 'Sirius_PCF_dev.xlsb')

def test_c_db_dataframeCred_request():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_dataframeCred()
    dbServer.dataframeCredentials(df_UID)
    dbServer.change_server('10.229.125.101')
    dbServer.change_database('SolaQC')
    dbServer.connect()
    assert (dbServer.cnxn is not None)
    assert (dbServer.cursor is not None)
    dbServer.request = 'SELECT top 1 * FROM log ORDER BY [dtm_log]'
    dbServer.executeReq()
    dbServer.commit()
    assert ('10.229.125.101' in dbServer.server)
    assert (dbServer.database == 'SolaQC')

def test_c_db_withLog_request():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_withLog()
    dbServer.dataframeCredentials(df_UID)
    dbServer.change_server('10.229.125.101')
    dbServer.change_database('SolaQC')
    dbServer.connect()
    assert (dbServer.cnxn is not None)
    assert (dbServer.cursor is not None)
    dbServer.request = 'SELECT top 1 * FROM log ORDER BY [dtm_log]'
    dbServer.executeReq()
    dbServer.commit()
    assert ('10.229.125.101' in dbServer.server)
    assert (dbServer.database == 'SolaQC')

def test_c_db_withLog_executeLog():
    df_UID = fDf_lite_Launch()
    if df_UID is None:
        return None
    dbServer = db.c_db_withLog()
    dbServer.dataframeCredentials(df_UID)
    dbServer.define_Log_Cred(str_serverForLog = '10.229.125.101', str_databaseForLog = 'SolaQC')
    dbServer.executeLog(str_logExec = 'SELECT top 1 * FROM log ORDER BY [dtm_log]')
    # Check it is still Prod Server + DB after a Log
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    dbServer.change_server('10.233.6.147')
    dbServer.executeLog(str_logExec='SELECT top 1 * FROM log ORDER BY [dtm_log]')
    # Check it is still Prod Server + DB after a Log
    assert ('10.233.6.147' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcfReporting')



#=============================================================================
# FUNCTIONAL TEST on Launching function
#=============================================================================
def launch_db_credentials():
    dbServer =  db.c_db_withLog()
    df_UID =    fDf_lite_Launch()
    dbServer.dataframeCredentials(df_UID)
    dbServer.define_Log_Cred(str_serverForLog = '10.229.125.101', str_databaseForLog = 'SolaQC')
    return dbServer

def test_db_DefineConnectCursor():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    db.db_DefineConnectCursor('')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    assert (dbServer.cursor is not None)
    assert (dbServer.cnxn is not None)

def test_db_EXECLog():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    dbServer.executeLog(str_logExec='SELECT top 1 * FROM log ORDER BY [dtm_log]')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    assert (dbServer.cursor is not None)
    assert (dbServer.cnxn is not None)

def test_db_EXEC():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    db.db_EXEC('SELECT top 10 * FROM tblCountry')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    assert (dbServer.cursor is not None)
    assert (dbServer.cnxn is not None)

def test_db_SelectReq():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    db.db_SelectReq('SELECT top 10 * FROM tblCountry')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    assert (dbServer.cursor is not None)
    assert (dbServer.cnxn is not None)
    assert (isinstance(dbServer.df_result, pd.DataFrame))

def test_db_EXEC_dbLogInRequest():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    db.db_SelectReq('SELECT top 10 * FROM tblCountry')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    assert (dbServer.cursor is not None)
    assert (dbServer.cnxn is not None)
    assert (isinstance(dbServer.df_result, pd.DataFrame))
    db.db_EXEC('SELECT top 1 * FROM SolaQC..log ORDER BY [dtm_log]')
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')
    assert (dbServer.uid == 'pcf_reporting')
    assert (dbServer.cursor is not None)
    assert (dbServer.cnxn is not None)
    assert (isinstance(dbServer.df_result, pd.DataFrame))

def test_getDfLog():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    db.db_SelectReq('SELECT top 10 * FROM tblCountry')
    assert ('D1PRDSOLADB' in dbServer.server)
    str_req = r"SELECT str_product FROM SolaQC..tbl_inactiveProduct WHERE str_listType = 'Restricted Stocks' AND str_perimeter = 'UK_Harvest_CSI300' AND bl_inactive = 1"
    df_sql = db.db_SelectReq(str_req, bl_AlertIfEmptyReq=True)
    assert (isinstance(df_sql, pd.DataFrame))
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (dbServer.database == 'SolaDBServer')

def test_keepSingletonInMemory():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    assert ('D1PRDSOLADB' in dbServer.server)
    assert (isinstance(dbServer.df_UID, pd.DataFrame))
    db.db_SelectReq("SELECT top 10 * FROM tblCountry")
    assert (isinstance(dbServer.df_result, pd.DataFrame))
    dbServer.executeLog(str_logExec=r"SELECT top 1 * FROM log ORDER BY [dtm_log]")
    assert ('D1PRDSOLADB' in dbServer.server)
    db.db_SelectReq("SELECT top 5 * FROM tblCountry")
    assert (isinstance(dbServer.df_result, pd.DataFrame))

def test_ChangeDB_forARequest():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    str_req =   r"SELECT top 1 * FROM log ORDER BY [dtm_log]"
    df_req =    db.db_SelectReq(str_req, str_database = 'SolaQC')
    assert (isinstance(df_req, pd.DataFrame))
    assert ('D1PRDSOLADB' in dbServer.server)

def test_ChangeDB_forARequest_details():
    launch_db_credentials()
    dbServer = db.c_db_withLog()
    str_req =   r"""DECLARE @Yesterday DATE
                DECLARE @Today DATE
                DECLARE @ISIN VARCHAR(12)
                
                SET @Today = '2022-05-24 00:00:00'
                SET @ISIN = 'HK0000172673'
                
                SELECT @Yesterday = MAX(tep.AsAtDate)
                FROM SolaDBServer..vwSecurity sec
                    inner join SolaDBServer..vwFamily f on f.SecurityID = sec.SecurityID
                    inner join SolaDBServer..tblETFPosition tep on tep.ETFID = f.ETFID
                WHERE tep.AsAtDate < @Today AND sec.Isin = @ISIN
                
                SELECT tep.AsAtDate, tep.NAV
                FROM SolaDBServer..vwSecurity sec
                    inner join SolaDBServer..vwFamily f on f.SecurityID = sec.SecurityID
                    inner join SolaDBServer..tblETFPosition tep on tep.ETFID = f.ETFID
                WHERE tep.AsAtDate = @Yesterday AND sec.Isin = @ISIN"""
    # Details of db_SelectReq
    db.db_DefineConnectCursor(str_req, str_database = 'SolaQC')
    dbServer.defineCredentials(bl_AlertIfEmptyReq = True)
    # Test
    assert (dbServer.bl_useLog is True)
    df_UID = dbServer.df_UID
    uid_Log = df_UID.loc[df_UID[dbServer.serverColName] == dbServer.server_Log, 'Uid'].values[0]
    pwd_Log = df_UID.loc[df_UID[dbServer.serverColName] == dbServer.server_Log, 'Password'].values[0]
    d_pLog = dict(server = dbServer.server_Log, database = dbServer.db_Log, uid = uid_Log, pwd = pwd_Log)
    assert (d_pLog['uid'] == 'pcfReporting')
    assert (dbServer.uid == 'pcf_reporting')

# pytest test/test_nutDb.py
