import os
import pandas as pd
import numpy as np
# import pytest
try:
    import nutDataframe as dframe
except:
    print('Online Test...')
    from pyNut import nutDataframe as dframe


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
    df_1 = dframe.fDf_createSimpleDataframe(l_column=['col_Join', 'data1'],
                                            l_values=[['0', 0], ['1', 1], ['2', 2], ['3', 3], ['4', 4], ['5', 5],
                                                      ['6', 6], ['7', 7], ['8', 8], ['9', 9], ['10', 10]])
    df_2 = dframe.fDf_createSimpleDataframe(l_column=['col_Join', 'data2'],
                                            l_values=[['0', 0], ['1', 1], ['2', 2], ['3', 3], ['4', 4], ['5', 5],
                                                      ['6', 6], ['7', 7], ['8', 8], ['9', 9], ['10', 10]])
    bl_compare, df_compare = dframe.fBl_compareDfCol({'df': df_1, 'colJoin': 'col_Join','colToCompare':'data1'},
                                                     {'df': df_2, 'colJoin': 'col_Join','colToCompare':'data2'})
    assert( bl_compare is True )
    assert( df_compare is None )
    df_2 = dframe.fDf_createSimpleDataframe(l_column=['col_Join', 'data1'],
                                            l_values=[['0', 0], ['1', 1], ['2', 2], ['3', 3], ['4', 4], ['5', 5],
                                                      ['6', 6], ['7', 7], ['8', 8], ['9', 9], ['10', 10]])
    bl_compare, df_compare = dframe.fBl_compareDfCol({'df': df_1, 'colJoin': 'col_Join', 'colToCompare': 'data1'},
                                                     {'df': df_2, 'colJoin': 'col_Join', 'colToCompare': 'data1'})
    assert (bl_compare is True)
    assert (df_compare is None)


def test_round_down():
    df_1 = dframe.fDf_createSimpleDataframe(l_column=['col_Join', 'RightData', 'DataToBeRounded'],
                                            l_values=[[0, 0, 0.1], [1, 0, 0.9], [2, 1, 1.5], [3, 1, 1.999], [4, 3, 3.9], [5, 2, 2],
                                                      [6, -4, -3.9], [7, -1, -0.1], [8, -2, -1.0001], [9, -7, -7], [10, -8, -7.00001]])
    df_2 = df_1.copy()
    df_2['DataRounded'] = df_2['DataToBeRounded'].apply(lambda x: dframe.round_down(x))
    bl_compare, df_compare = dframe.fBl_compareDfCol({'df': df_1, 'colJoin': 'col_Join', 'colToCompare': 'RightData'},
                                                     {'df': df_2, 'colJoin': 'col_Join', 'colToCompare': 'DataRounded'})
    assert (bl_compare is True)
    assert (df_compare is None)


def test_round_up():
    df_1 = dframe.fDf_createSimpleDataframe(l_column=['col_Join', 'RightData', 'DataToBeRounded'],
                                            l_values=[[0, 1, 0.1], [1, 1, 0.9], [2, 2, 1.5], [3, 2, 1.999], [4, 4, 3.5], [5, 2, 2],
                                                      [6, -3, -3.9], [7, 0, -0.1], [8, -1, -1.9999], [9, -7, -7], [10, -7, -7.00001]])
    df_2 = df_1.copy()
    df_2['DataRounded'] = df_2['DataToBeRounded'].apply(lambda x: dframe.round_up(x))
    bl_compare, df_compare = dframe.fBl_compareDfCol({'df': df_1, 'colJoin': 'col_Join', 'colToCompare': 'RightData'},
                                                     {'df': df_2, 'colJoin': 'col_Join', 'colToCompare': 'DataRounded'})
    assert (bl_compare is True)
    assert (df_compare is None)

def test_fBl_IsNan():
    nanValue = np.nan
    bl_nan = dframe.fBl_IsNan(nanValue)
    assert (bl_nan is True)
    df = dframe.fDf_createSimpleDataframe(l_column=['col1', 'col2', 'col3'],
                                          l_values=[[0, 1, 0.1], [2, np.nan, np.nan], [3, 2, 1.999], [4, 4, np.nan],
                                                    [np.nan, -3, -3.9], [8, np.nan, -1.9999], [9, -7, np.nan]])
    df_1 = df[df['col1'].apply(lambda x: dframe.fBl_IsNan(x))]
    df_2 = df[df['col2'].apply(lambda x: dframe.fBl_IsNan(x))]
    df_3 = df[df['col3'].apply(lambda x: dframe.fBl_IsNan(x))]
    assert (len(df_1) == 1)
    assert (len(df_2) == 2)
    assert (len(df_3) == 3)

def test_fDf_readCsv_enhanced():
    str_path = os.path.dirname(os.path.abspath(__file__))
    str_path1 = str_path + r'\fileToTest\NICB Detailed Portfolio Valuation Report 06Apr22.csv'
    df_data = dframe.fDf_readCsv_enhanced(str_path1, bl_header = None, l_names=range(13))
    assert (isinstance(df_data, pd.DataFrame) )
    str_path2 = str_path + r'\fileToTest\20211026_20211026_10740_718708NETRCNH'
    df_data = dframe.fDf_readCsv_enhanced(str_path2, bl_header=None, str_sep='|', l_names=range(13))
    assert (isinstance(df_data, pd.DataFrame))

def test_fDf_removeDoublons():
    df1 = dframe.fDf_createSimpleDataframe(l_column=['col1', 'col2', 'col3'],
                                           l_values=[[0, 1, 0.1], [2, np.nan, np.nan], [0, 1, 0.1], [0, 1, 4],
                                                     [np.nan, -3, -3.9], [0, 1, 0.1], [9, -7, np.nan]])
    df2 = dframe.fDf_removeDoublons(df1)
    assert (len(df2) == len(df1) - 2)
    assert (2 not in list(df2.index))
    assert (1 in list(df2.index))

def test_fDf_DropRowsIfNa_resetIndex():
    df1 = dframe.fDf_createSimpleDataframe(l_column=['col1', 'col2', 'col3'],
                                           l_values=[[0, 1, 0.1], [2, np.nan, np.nan], [0, 1, 0.1], [0, 1, 4],
                                                     [np.nan, -3, -3.9], [0, 1, 0.1], [9, -7, np.nan]])
    df2 = dframe.fDf_DropRowsIfNa_resetIndex(df1, l_colToDropNA = ['col1'])
    assert (len(df2) == len(df1) - 1)

def test_dDf_fillNaColumn():
    df1 = dframe.fDf_createSimpleDataframe(l_column=['col1', 'col2', 'col3'],
                                           l_values=[[0, 1, 0.1], [2, np.nan, np.nan], [3, 1, 0.1], [4, 1, 4],
                                                     [5, np.nan, -3.9], [6, np.nan, 0.1], [7, -7, np.nan]])
    df2 = dframe.dDf_fillNaColumn(df1, 'col2', 'col1')
    df3 = dframe.fDf_DropRowsIfNa_resetIndex(df2, l_colToDropNA=['col2'])
    assert (len(df2) == len(df3))

