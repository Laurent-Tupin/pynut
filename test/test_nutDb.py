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
    db_lite.definePath(str_pathDb)
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
    dbServer.defineCredentials(**d_param)
    dbServer.request = "SELECT * FROM Table"
    assert (dbServer is not None)

def test_c_db_sqlServ_single_singleton():
    dbServer = db.c_db_sqlServ_single()
    dbServe2 = db.c_db_sqlServ_single()
    d_param = dict(server='101', database='Test', uid='laurent', pwd='**abc**')
    dbServer.defineCredentials(**d_param)
    assert (dbServer.server == '101')
    assert (dbServe2.server == '101')
    d_para2 = dict(server='102', database='Prod', uid='Guillaume', pwd='**xyz**', timeout = 50, bl_AlertIfEmptyReq = False)
    dbServe2.defineCredentials(**d_para2)
    assert (dbServer.uid == 'Guillaume')
    assert (dbServe2.uid == 'Guillaume')
    assert (dbServer.timeout == 50)
    assert (dbServe2.timeout == 50)

def test_c_db_dataframeCred_singleton():
    dbServer = db.c_db_dataframeCred()
    dbServe2 = db.c_db_dataframeCred()
    d_param = dict(server='101', database='Test', uid='laurent', pwd='**abc**')
    dbServer.defineCredentials(**d_param)
    assert (dbServer.server == '101')
    assert (dbServe2.server == '101')
    d_para2 = dict(server='102', database='Prod', uid='Guillaume', pwd='**xyz**', timeout = 50, bl_AlertIfEmptyReq = False)
    dbServe2.defineCredentials(**d_para2)
    assert (dbServer.uid == 'Guillaume')
    assert (dbServe2.uid == 'Guillaume')
    assert (dbServer.timeout == 50)
    assert (dbServe2.timeout == 50)

def test_c_db_withLog_singleton():
    dbServer = db.c_db_withLog()
    dbServe2 = db.c_db_withLog()
    d_param = dict(server='101', database='Test', uid='laurent', pwd='**abc**')
    dbServer.defineCredentials(**d_param)
    assert (dbServer.server == '101')
    assert (dbServe2.server == '101')
    d_para2 = dict(server='102', database='Prod', uid='Guillaume', pwd='**xyz**', timeout = 50, bl_AlertIfEmptyReq = False)
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











