


# dfIn_HOLD_stock = dframe.fDf_CleanPrepareDF(dfIn_HOLD_stock, l_colToBeFloat = ['TOTAL MARKET VALUE'], l_colToDropNA = ['ISIN'])
#
#
#
# df_Nav_1 = dframe.fDf_FindSubDataframe(df_Nav, str_ID, str_valueToEnd = 'TOTAL_NET_ASSETS',int_addRowsEnd = 10,
#                                                     bl_Make1stRow_columns = False, bl_DropRowsIfNa_resetIndex = False)
#
# flt_nav =   dframe.fStr_VlookUp(df_Nav, 'NAV', int_colNb = 1)
#
# df_Compo = dframe.dDf_fillNaColumn(df_Compo, 'Ric', 'RIC')
#
# df_3Compo = dframe.fDf_Concat_wColOfDf1(df_3Compo, df_Compo)
#
# dfIn_HOLD_stock = dframe.fDf_removeDoublons(dfIn_HOLD_stock)
#
# df_Pcf = dframe.fDf_replaceStringColByZero(df_Pcf, 'QUANTITY', 0)
#
# df_NAV['Price share CCY'] = df_NAV['Price share CCY'].apply(lambda x:dframe.round_Correction(x, 13))





import pandas as pd
import sys
sys.path.append('../')
import pyNut.nutDataframe as dframe
# import pytest


#=============================================================================
# UNIT TEST
#=============================================================================
def test_fDf_createSimpleDataframe():
    df_simple = dframe.fDf_createSimpleDataframe()
    assert( isinstance(df_simple, pd.DataFrame) )

def test_fBl_isDataframeEmpty():
    df_simple = dframe.fDf_createSimpleDataframe()
    bl_isempty = dframe.fBl_isDataframeEmpty(df_simple)
    assert( bl_isempty is False )

def test_fBl_compareDfCol():
    df_1 = dframe.fDf_createSimpleDataframe(l_column=['colJoin', 'data'],
                                            l_values=[['0', 0], ['1', 1], ['2', 2], ['3', 3], ['4', 4], ['5', 5],
                                                      ['6', 6], ['7', 7], ['8', 8], ['9', 9], ['10', 10]])
    df_2 = dframe.fDf_createSimpleDataframe(l_column=['colJoin', 'data'],
                                            l_values=[['0', 0], ['1', 1], ['2', 2], ['3', 3], ['4', 4], ['5', 5],
                                                      ['6', 6], ['7', 7], ['8', 8], ['9', 9], ['10', 10]])
    bl_compare, df_compare = dframe.fBl_compareDfCol({'df': df_1, 'colJoin': 'colJoin','colToCompare':'data'},
                                                     {'df': df_2,'colJoin': 'colJoin','colToCompare':'data'})
    assert( bl_compare is True )
    assert( df_compare is None )



# def test_round_down():
#     df_1 = dframe.fDf_createSimpleDataframe(l_column = ['DataRounded', 'DataToBeRounded'], l_values = [ [0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10] ])
#     df_1['DataRounded'] = df_1['DataToBeRounded'].apply(lambda x: dframe.round_down(x))
#     print(df_1)















