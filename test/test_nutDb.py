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


#=============================================================================
# FUNCTIONAL TEST
#=============================================================================
def test_c_db_lite_functionnal():
    str_pathDb = r'C:\Users\laurent.tupin\Documents\GitLab\sola-pcf\db_param.db'
    str_req =   "SELECT * FROM tbl_connectSolaDb"
    if not fBl_liteAccessible(str_pathDb):
        return None
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













