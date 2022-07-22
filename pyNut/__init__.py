__version__ = "2.2.5"


#-----------------------------------------------------------------
# pynut
#-----------------------------------------------------------------
def nutOther():
    try:
        from pyNutTools import nutOther
    except Exception as err:
        print('  IMPORT FAIL |nutOther|, err:|{}|'.format(err))
        return None
    return nutOther

def nutDataframe():
    try:
        from pyNutTools import nutDataframe
    except Exception as err:
        print('  IMPORT FAIL |nutDataframe|, err:|{}|'.format(err))
        return None
    return nutDataframe

def nutDate():
    try:
        from pyNutTools import nutDate
    except Exception as err:
        print('  IMPORT FAIL |nutDate|, err:|{}|'.format(err))
        return None
    return nutDate

def nutApi():
    try:
        from pyNutApi import nutApi
    except Exception as err:
        print('  IMPORT FAIL |nutApi|, err:|{}|'.format(err))
        return None
    return nutApi

def nutFiles():
    try:
        from pyNutFiles import nutFiles
    except Exception as err:
        print('  IMPORT FAIL |nutFiles|, err:|{}|'.format(err))
        return None
    return nutFiles

def nutDb():
    try:
        from pyNutDB import nutDb
    except Exception as err:
        print('  IMPORT FAIL |nutDb|, err:|{}|'.format(err))
        return None
    return nutDb

def nutEmail():
    try:
        from pyNutEmail import nutEmail
    except Exception as err:
        print('  IMPORT FAIL |nutEmail|, err:|{}|'.format(err))
        return None
    return nutEmail

def nutFtp():
    try:
        from pyNutFtp import nutFtp
    except Exception as err:
        print('  IMPORT FAIL |nutFtp|, err:|{}|'.format(err))
        return None
    return nutFtp
