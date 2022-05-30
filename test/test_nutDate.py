import datetime
import time
try:    import nutDate as dat
except:
    print('Online Test...')
    from pyNut import nutDate as dat

#import pytest

# pytest test/test_nutDate.py


#=============================================================================
# UNIT TEST
#=============================================================================
def test_fDte_Now_GMT():
    dte_now = dat.fDte_Now()
    dte_GMT = dat.fDte_Now_GMT()
    assert (dte_GMT.hour+8 == dte_now.hour)

def test_fDte_formatToDate():
    dte_date = '2022-02-20'
    str_format = '%Y-%m-%d'
    dte_date = dat.fDte_formatToDate(dte_date, str_format)
    assert( isinstance(dte_date, datetime.date) )
    dte_today = dat.fDte_Today()
    str_format = 'xxxx'
    dte_date = dat.fDte_formatToDate(dte_today, str_format)
    assert( isinstance(dte_date, datetime.date) )

def test_fInt_dateDifference():
    dte_today =     dat.fDte_Today()
    dte_yesterday = dat.fDte_AddDay(dte_today, -1)
    int_diff =      dat.fInt_dateDifference(dte_today, dte_yesterday)
    assert( isinstance(int_diff, int) )
    assert( int_diff == 1 )

def test_fBl_TimeIsBetween():
    dte_now =       dat.fDte_Now()
    dte_past =      dat.fDte_AddHour(dte_now, -1)
    dte_future =    dat.fDte_AddHour(dte_now, 1)
    bl_isBtw =      dat.fBl_TimeIsBetween(dte_past, dte_future, dte_now)
    assert ( isinstance(bl_isBtw, bool) )
    assert ( bl_isBtw is True )

def test_fStr_DateToString():
    dte_now =       dat.fDte_Now()
    str_dateFormat = '%Y-%m-%d'
    str_date =      dat.fStr_DateToString(dte_now, str_dateFormat = str_dateFormat)
    assert (isinstance(str_date, str))

def test_fDte_convertExcelInteger():
    int_date = 46106
    dte_date = dat.fDte_convertExcelInteger(int_date)
    print(dte_date)
    assert (isinstance(dte_date, datetime.date))
    str_date = dat.fStr_DateToString(dte_date, str_dateFormat='%Y-%m-%d')
    assert( str_date == '2026-03-25' )
    dte_date = dat.fDte_convertExcelInteger(int_date, bl_formatDate_tuple = True)
    print(dte_date)
    print(type(dte_date))
    assert (isinstance(dte_date, time.struct_time))
