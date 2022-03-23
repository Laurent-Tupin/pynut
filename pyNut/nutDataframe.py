try:
    from . import _lib as lib
except:
    import _lib as lib
os  = lib.os()
math = lib.math()
pd  = lib.pandas()
np  = lib.numpy()



#==============================================================================
# Create Dataframe
#==============================================================================
def fBl_isDataframeEmpty(df):
    return df.empty

def fDf_createSimpleDataframe(l_column = None, l_values = None):
    if l_column == None:    l_column = ['Empty_Dataframe']
    if l_values == None:    l_values = [0]
    df_data = pd.DataFrame(l_values, columns = l_column)
    return df_data



#==============================================================================
# Special rounding treatment
#==============================================================================
def round_down(nb_in, decimals = 0):
    """floor() rounds down. int() truncates. The difference is clear when you use negative numbers
    math.floor(-3.5)    -4
    int(-3.5)           -3"""
    multiplier = 10 ** int(decimals)
    Result = math.floor(nb_in * multiplier) / multiplier
    return Result

def round_up(nb_in, decimals = 0):
    multiplier = 10 ** int(decimals)
    Result = math.ceil(nb_in * multiplier) / multiplier
    return Result

def round_Correction(nb_in, decimals = 0):
    try:
        nb_in = float(nb_in)
        if nb_in != 0:      flt_add = 0.5 * (nb_in/abs(nb_in))
        else:               return 0
        multiplier = 10 ** int(decimals)
        Result = int((nb_in * multiplier) + flt_add) / multiplier
    except Exception as err:    
        print('  ERRROR in round_Correction: {}'.format(str(err)))
        print('  - nb_in: ', nb_in)
        print('  - decimals: ', decimals)
        try:
            print('  - flt_add: ', flt_add)
            print('  - multiplier: ', multiplier)
        except: pass
        raise
    return Result

def round_corectPythonFlaws(nb_in):
    return round_Correction(nb_in, 10)

def round_myRound(nb_in, base = 1):
    try:
        # Special treatment as 0.5 needs to be round up and not down
        if nb_in != 0:      flt_add = 10**(-6) * (nb_in / abs(nb_in))
        else:               return 0
        MyRound = base * round((nb_in + flt_add) / base)
    except Exception as err:    
        print('  ERRROR in round_myRound: {}'.format(str(err)))
        print('  - nb_in: ', nb_in)
        print('  - base: ', base)
        try:
            print('  - flt_add: ', flt_add)
        except: pass
        raise
    return MyRound
    
  
#==============================================================================
# Nan
#==============================================================================
def fBl_IsNan(inputValue):
    if isinstance(inputValue, float):
        if np.isnan(inputValue):
            return True
        if math.isnan(inputValue):
            return True
    if inputValue != inputValue:
        return True
    try:
        if str(float(inputValue)).lower() == 'nan':
            return True
    except: pass
    return False
    
  

#==============================================================================
# Read file for Dataframe
#==============================================================================
def fDf_readCsv_enhanced(str_path, bl_header = None, str_sep = ',', l_names = None, str_encoding = None):       
    try:
        df_data = pd.read_csv(str_path, header = bl_header, sep = str_sep, names = l_names, encoding = str_encoding)
    # -------------------------------------------------------------
    # RECURSIVE solution if second row has more columns or enoding does not recognise special Symbol like EUR
    except pd.errors.ParserError as err:
        print(' ERROR ParserError: {}'.format(str(err)[:-1]))
        str_find = 'saw '
        int_position = int(str(err).find(str_find)) + len(str_find)
        str_nbCol = str(err)[int_position:]
        print(' - Nb of columns we should have: {}'.format(str(int(str_nbCol))))
        df_data = fDf_readCsv_enhanced(str_path, bl_header, str_sep, range(int(str_nbCol)))
        print(' - Error Solved \n')
    except UnicodeDecodeError as err:
        print(' ERROR UnicodeDecodeError: {}'.format(err))
        with open(str_path, 'r') as f:
            str_encoding = f.encoding 
            print(' - Encoding of the file is actually: {}'.format(str_encoding))
        df_data = fDf_readCsv_enhanced(str_path, bl_header, str_sep, l_names, str_encoding)
        print(' - Error Solved \n')
        #print(df_data.head(3))
    except Exception as err:
        print('   ERROR in fDf_readCsv_enhanced: other undetcted')
        print('   - Error: ', str(err))
        print('   - str_path', str_path)
        print('   - bl_header', bl_header)
        print('   - str_sep', str_sep)
        print('   - l_names', l_names)
        print('   - str_encoding', str_encoding)
        return None
    return df_data



#==============================================================================
# Operation on Dataframe
#==============================================================================
def fDf_removeDoublons(df_in):
    df = df_in.copy()
    df.drop_duplicates(subset = None, keep = 'first', inplace = True)
    return df

def fBl_checkDfColumn_isNumber(df, str_colName):
    if df[str_colName].dtype == object:
        return False
    return True

def fDf_replaceEmptyByNan(df_in):
    df = df_in.copy()
    df.replace('', np.nan, inplace=True)
    return df

def fDf_CleanPrepareDF(df_in, l_colToBeFloat = [], l_colToDropNA = [], o_fillNA_by = -404, l_colSort = [], bl_ascending = True):
    df = df_in.copy()
    # Change Null to NA (if directly out of DB)
    df.fillna(value = np.nan, inplace = True)
    # Drop NA & fill NA to avoid any issue and bug
    if l_colToDropNA:
        df.dropna(axis = 'index', subset = l_colToDropNA, inplace = True)
    if o_fillNA_by != -404:
         df.fillna(value = o_fillNA_by, inplace = True)
    # Make sure column is float
    if l_colToBeFloat:
        for str_colToBeFloat in l_colToBeFloat:
            df[str_colToBeFloat] = df[str_colToBeFloat].astype(float)
    # Sort
    if l_colSort:
        df.sort_values(by = l_colSort, ascending = bl_ascending, inplace = True)
    return df

def fDf_DropRowsIfNa_resetIndex(df, l_colToDropNA = []):
    df = df.copy()
    if l_colToDropNA:   df.dropna(axis = 'index', subset = l_colToDropNA, inplace = True)
    else:               df.dropna(axis = 'index', inplace = True)
    df.reset_index(drop = True, inplace = True)
    return df

def dDf_fillNaColumn(df, str_colTarget, str_colValueToInputIfNA, str_CONST = None):
    try:
        if str_CONST is None:
            df[str_colTarget] = df[str_colTarget].fillna(df[str_colValueToInputIfNA])
        else:
            df[str_colTarget] = df[str_colTarget].fillna(str_CONST)
    except Exception as err:   
        print(' ERROR in dDf_fillNaColumn: |{}|'.format(err))
        raise
    return df


def fDf_changeDateFormat(df_in, str_colToApply, str_dateFormatInitial = '%Y%m%d', str_dateFormatWanted = '%Y-%m-%d'):
    # pd.set_option('display.max_rows', 1000)
    # If format is String, need to change it to Date
    df_result = df_in.copy()
    l_col = df_result.columns
    df_result['dte'] = pd.to_datetime(df_result[str_colToApply], format = str_dateFormatInitial)
    # Change back to string with the new format
    df_result[str_colToApply] = df_result['dte'].dt.strftime(str_dateFormatWanted)
    # df_result[str_colToApply].apply(lambda x: dat.fStr_DateToString(x, str_dateFormat = str_dateFormatWanted))
    return df_result[l_col]


def fDf_fillColUnderCondition(df, str_colToApply, ValueToApply, str_colCondition, ValueCondition, bl_except = False, ValueDefault = 0):
    ''' Transform un DF avec condition
    ValueToApply can be a value or a lambda function
    mask / 'map'
    '''
    # Add column if not here
    if not str_colToApply in df.columns:
        df[str_colToApply] = ValueDefault
    # MASK
    if bl_except:   
        df[str_colToApply]      = df[str_colToApply].mask(df[str_colCondition] != ValueCondition, ValueToApply)
    elif ValueCondition is None:
        df = dDf_fillNaColumn(df, str_colToApply, str_colCondition)
    elif '<=' in str(ValueCondition):
        ValueCondition = float(ValueCondition.replace('<=', ''))
        df[str_colToApply]      = df[str_colToApply].mask(df[str_colCondition] <= ValueCondition, ValueToApply)
    elif '<' in str(ValueCondition):
        ValueCondition = float(ValueCondition.replace('<', ''))
        df[str_colToApply]      = df[str_colToApply].mask(df[str_colCondition] < ValueCondition, ValueToApply)
    elif '>' in str(ValueCondition):
        ValueCondition = float(ValueCondition.replace('>', ''))
        df[str_colToApply]      = df[str_colToApply].mask(df[str_colCondition] > ValueCondition, ValueToApply)
    else: 
        df[str_colToApply]      = df[str_colToApply].mask(df[str_colCondition] == ValueCondition, ValueToApply)
    #df[str_colToApply] = [ValueToApply if x == ValueCondition else '-' for x in df[str_colCondition]]
    #df['Units'] = df['Units'].where(df['column'] == 'S', - df['Units'])
    return df



def fDf_replaceStringColByZero(df, str_colToApply, ValueToApply = 0):
    # df.str.replace(r'\$-', str(ValueToApply))
    # df = df.convert_objects(convert_numeric = True)
    try:
        ser = df[str_colToApply]
        ser = pd.to_numeric(ser, errors = 'coerce')
        # fill NA
        ser = ser.fillna(ValueToApply)
        df[str_colToApply] = ser
    except Exception as err:
        print('   ERROR in dframe.fDf_replaceStringColByZero || {}'.format(err))
        raise
    return df

def fDf_FilterOnCol(df, str_colToApply, l_isIN = [], str_startWith = '', bl_except = False):
    if bl_except:
        if l_isIN:                  df = df[~df[str_colToApply].isin(l_isIN)].copy()
        elif str_startWith != '':   df = df[~df[str_colToApply].str.startswith(str_startWith, na = False)].copy()    
    else:
        if l_isIN:
            df = df[df[str_colToApply].isin(l_isIN)].copy()
            #df_Holdings = df_OUT_LIGHTINV[df_OUT_LIGHTINV['GTI'].isin(['S01','S39'])]
        elif str_startWith != '':
            df = df[df[str_colToApply].str.startswith(str_startWith, na = False)].copy()
            #df_Fund = df_Fund[df_Fund['colForCriteria'].str.startswith('S', na = False)].copy()
    return df

def fDf_filterNan(df, str_colToApply, bl_except = False):
    if bl_except:
        df_out = df[~df[str_colToApply].isnull()].copy()
        # df_out = df[~df[str_colToApply] == np.nan].copy()
        # df_noAn = df[~df[str_colToApply] == 'Nan'].copy()
        # df_out = fDf_Concat_wColOfDf1(df_noNa, df_noAn)
    else:               
        df_out = df[df[str_colToApply].isnull()].copy()
        # df_out = df[df[str_colToApply] == np.nan].copy()
        # df_An = df[df[str_colToApply] == 'Nan'].copy()
        # df_out = fDf_Concat_wColOfDf1(df_na, df_An)    
    return df_out


def fDf_InsertColumnOfIndex(df, int_StartNumber = 1, int_PositionOf_ColumnIndex = 0, l_colSort = [], bl_ascending = True, str_indColName = 'ind'):
    try:
        # Sort before to do anything else
        if l_colSort:
            df.sort_values(by = l_colSort, ascending = bl_ascending, inplace = True)
        # Keep the inital columns name in a list / Keep the index as well
        l_col = df.columns.tolist()
        l_index = df.index
        # Add a column of index
        df.reset_index(drop = True, inplace = True)
        df[str_indColName] = df.index + int_StartNumber
        df.index = l_index
        # re-Order the columns the the index column is not at the end
        if int_PositionOf_ColumnIndex == 0:
            df = df[[str_indColName] + l_col]
        else:
            df = df[l_col[:int_PositionOf_ColumnIndex] + [str_indColName] + l_col[int_PositionOf_ColumnIndex:]]
    except Exception as err:    
        print(' ERROR in fDf_InsertColumnOfIndex: {}'.format(err))
        raise
    return df

def fDf_MakeColumns_1stRow(df_in):
    try:
        l_column = list(df_in.columns)
        df_1stRow = pd.DataFrame([l_column], columns = l_column)
        df_return = fDf_Concat_wColOfDf1(df_1stRow, df_in)
        # df_return.reset_index(drop = True, inplace = True) 
    except Exception as err:    
        print(' ERROR in fDf_MakeColumns_1stRow: {}'.format(err))
        raise
    return df_return

def fDf_Make1stRow_columns(df_in):
    try:
        df_return = df_in.iloc[1:].copy()
        df_return.columns = list(df_in.iloc[0])
        df_return.reset_index(drop = True, inplace = True) 
    except Exception as err:
        print(' ERROR in fDf_Make1stRow_columns: {}'.format(err))
        return df_in
    return df_return


def fDf_InsertRows(df, int_nbRows, int_rows):
    df_return = df
    for i in range(0, int_nbRows):
        df_line = pd.DataFrame([[''] * len(df_return.columns)], columns =  df_return.columns, index = [int_rows - 0.5])
        #df_return = pd.concat([df_return.ix[:int_rows], df_line, df_return.ix[int_rows + 1:]]).reset_index(drop=True)
        df_return = df_return.append(df_line, ignore_index = False)
        df_return = df_return.sort_index().reset_index(drop = True) 
    return df_return


def fDf_Concat_wColOfDf1(df1, df2, bl_colDf2_AsARow = False, int_emptyRow = 0):
    # Intro: Prepare the DF
    if bl_colDf2_AsARow or int_emptyRow > 0:
        df_inBetween = pd.DataFrame(columns = df2.columns)
        for i in range(int_emptyRow):
            df_inBetween.loc[len(df_inBetween)] = [''] * len(df2.columns)
        if bl_colDf2_AsARow:
            df_inBetween.loc[len(df_inBetween)] = df2.columns
        df2 = pd.concat([df_inBetween, df2], ignore_index = True, sort = False)
    # CONCAT
    if len(df1.columns) >= len(df2.columns):
        df2.columns = df1.columns[:len(df2.columns)]
        df_return = pd.concat([df1, df2], ignore_index = True, sort = False)
        df_return = df_return[df1.columns]
    else:
        df2.columns = list(df1.columns) + list(df2.columns[len(df1.columns):])
        df_return = pd.concat([df1, df2], ignore_index = True, sort = False)
        df_return = df_return[df2.columns]
    return df_return

def fDf_Concat_horizontal(df1, df2, bl_colDf2_AsARow = False):
    df_return = pd.concat([df1, df2], axis = 1)
    if bl_colDf2_AsARow:
        df_inBetween = pd.DataFrame(columns = df_return.columns)
        df_inBetween.loc[len(df_inBetween)] = df_return.columns
        df_return = pd.concat([df_inBetween, df_return], ignore_index = True, sort = False)
    return df_return

#-------------------------------------------
# Sub-Dataframe, find String to delimiter
#-------------------------------------------
def fInt_FindIndex(df, str_valueToFind, bl_resetIndex = False):
    try:
        df_RowToFind = df.copy()
        if bl_resetIndex:
            df_RowToFind = df_RowToFind.reset_index(drop = True)
        # sBl_search = df_RowToFind.eq(str_valueToFind).any(1)
        # sBl_search = (df_RowToFind == str_valueToFind).any(1)
        sBl_search = df_RowToFind.isin([str_valueToFind]).any(1)
        df_RowToFind = df_RowToFind[sBl_search]
        # df_RowToFind = df_RowToFind[df_RowToFind.iloc[:, 1] == str_valueToFind]
        l_index_RowToFind = df_RowToFind.index
    except Exception as err:
        print('  ERROR in dframe.fInt_FindIndex: {}'.format(err))
        print('  - ', str_valueToFind)
        raise        
    return l_index_RowToFind

def fInt_FindInde_like(df, str_valueToFind, bl_resetIndex = False):
    # df[df['ids'].str.contains('ball', na = False)]
    # df.set_index('ids').filter(like='ball', axis=0)
    # df.set_index('ids').filter(regex='ball$', axis=0)     # ENd by Ball
    # df.set_index('ids').filter(regex='^ball', axis=0)     # start by ball
    try:
        df_RowToFind = df.copy()
        if bl_resetIndex:
            df_RowToFind = df_RowToFind.reset_index(drop = True)
        # Loop on column
        for colum in list(df_RowToFind.columns):
            try:
                df_search = df_RowToFind[df_RowToFind[colum].str.contains(str_valueToFind, na = False)]
                l_index = df_search.index
                # SUCCESS: So we return one first column
                return l_index
            except: pass
        # Raise if it str(colum) never been found in any column
        str_msgErr = 'End of the loop, didnt find anything'
        raise
    except Exception as err:
        print('  ERROR in dframe.fInt_FindInde_like: {}'.format(err))
        print('  |{}|'.format(str_valueToFind))
        print('   - {}'.format(str_msgErr))
        raise        


def fInt_FindColumn(df, str_valueToFind):
    #pd.set_option('display.max_rows', 1000)
    # df_booleanIfValueOrNot = df.eq(str_valueToFind)
    # df_ValueOrNan_IfValueOrNot = df[df.eq(str_valueToFind)]
    try:
        df_ColToFind = df.copy()
        df_booleanIfValueOrNot =        df_ColToFind.isin([str_valueToFind])
        df_ValueOrNan_IfValueOrNot =    df_ColToFind[df_booleanIfValueOrNot]
        df_ColToFind =                  df_ValueOrNan_IfValueOrNot.dropna(axis = 'columns', how = 'all')
        l_colNameToFind = df_ColToFind.columns
    except Exception as err:
        print('  ERROR in dframe.fInt_FindColumn: {}'.format(err))
        print('  - ', str_valueToFind)
        raise        
    return l_colNameToFind
    

def fDf_FindSubDataframe(df, str_valueToFind, str_valueToEnd = '!@#$%', int_addRowsStart = 0, int_addRowsEnd = 0, int_occurStart = 0,  
                         int_occurEnd = 0, bl_Make1stRow_columns = True, bl_DropRowsIfNa_resetIndex = True, bl_like = False):
    try:
        # Find the list of index (like or exact value)
        if bl_like:     l_index_RowToFind = fInt_FindInde_like(df, str_valueToFind)
        else:           l_index_RowToFind = fInt_FindIndex(df, str_valueToFind)
        if not list(l_index_RowToFind):
            print('  Warning: you are using fDf_FindSubDataframe but didnt find any value: #{}#. So we return the original DF'.format(str_valueToFind))
            return df
        # Start Cut DF by the first row
        int_rowStart = l_index_RowToFind[int_occurStart] + int_addRowsStart
        df_sub = df.loc[int_rowStart:].copy()
        
        # Cut with a end value 
        if not str_valueToEnd == '!@#$%':
            if bl_like:     l_index_End = fInt_FindInde_like(df_sub, str_valueToEnd)
            else:           l_index_End = fInt_FindIndex(df_sub, str_valueToEnd)
            if list(l_index_End):
                int_rowEnd = l_index_End[int_occurEnd] + int_addRowsEnd
                df_sub = df_sub.loc[:int_rowEnd]
        # Remove NaN on the columns
        if not bl_like:
            l_colNameToFind = fInt_FindColumn(df, str_valueToFind)
            if list(l_colNameToFind):
                if bl_DropRowsIfNa_resetIndex:
                    df_sub = fDf_DropRowsIfNa_resetIndex(df_sub, list(l_colNameToFind))
            else:       print(' WARNING in fDf_FindSubDataframe: could not find the column')
        # March 2021: Remove columns at the end where all is NA
        df_sub.dropna(axis = 'columns', how = 'all', inplace = True)
        # 1st columns become Title
        if bl_Make1stRow_columns:
            df_sub = fDf_Make1stRow_columns(df_sub)
    except Exception as err:
        print('   ERROR in fDf_FindSubDataframe')
        print('   - Error: ', str(err))
        print('   - str_valueToFind: ', str_valueToFind)
        print('   - str_valueToEnd: ', str_valueToEnd)
        return df
    return df_sub

def fStr_VlookUp(df, v_valueToFind, int_colNb = 1):
    if isinstance(v_valueToFind, str):
        try:
            int_row = fInt_FindIndex(df, v_valueToFind, bl_resetIndex = True)
            str_return = df.iloc[int_row, int_colNb].values[0]
        except Exception as err: 
            print(' ERROR in fStr_VlookUp: Could not find the value in the file: |{}|'.format(v_valueToFind))
            print(' - ', str(err))
            pd.set_option('display.max_rows', 1000)
            print(df, '\n\n')
            # Return None avoid error and is more logic with the LIST behavior
            return None
        return str_return
    elif isinstance(v_valueToFind, list):
        for _valueToFind in v_valueToFind:
            try:
                int_row = fInt_FindIndex(df, _valueToFind, bl_resetIndex = True)
                str_return = df.iloc[int_row, int_colNb].values[0]
                return str_return
            except: print(' No error in fStr_VlookUp: dont find the value: |{}|'.format(str(_valueToFind)))
        # out of FOR loop without finding anything
        print(' ERROR in fStr_VlookUp: Could not find any value in the list: ', v_valueToFind)
        pd.set_option('display.max_rows', 1000)
        print(df, '\n\n')
        return None
    else: 
        print('  ** ERROR fStr_VlookUp, check type v_valueToFind: |{}| \n '.format(type(v_valueToFind)), v_valueToFind)
        return None
    
        
        


#-------------------------------------------
# Join / Merge
#-------------------------------------------
def fDf_JoinDf(df_left, df_right, str_columnON, str_how = 'inner', str_columnRightON = ''):
    # MERGE ASOF
    # https://pandas.pydata.org/pandas-docs/version/0.25.0/reference/api/pandas.merge_asof.html
    # how{‘left’, ‘right’, ‘outer’, ‘inner’}, default ‘inner’
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html
    
    # Verification
    if not str_columnON in df_left.columns :
        print(' ERROR  in fDf_JoinDf: Column {0} is not in left dataframe: {1}'.format(str_columnON, list(df_left.columns)))
        print(df_left.head(5), '\n\n')
        return df_left
    if str_columnRightON == '':
        if not str_columnON in df_right.columns:
            print(' ERROR  in fDf_JoinDf: Column {0} is not in right dataframe: {1}'.format(str_columnON, list(df_right.columns)))
            print(df_right.head(5), '\n\n')
            return df_left
    else:
        if not str_columnRightON in df_right.columns:
            print(' ERROR  in fDf_JoinDf: Column {0} is not in right dataframe: {1}'.format(str_columnRightON, list(df_right.columns)))
            print(df_right.head(5), '\n\n')
            return df_left
    # JOIN 
    try:
        if str_columnRightON == '':
            df = pd.merge(df_left, df_right, on = str_columnON, how = str_how)
        else:
            df = pd.merge(df_left, df_right, left_on = str_columnON, right_on = str_columnRightON, how = str_how)
        #df_Holds_MACI = df_Holds_MACI.join(df_Out_Fx[['Curr', 'Fx']].set_index('Curr'), on = 'Curr')
    except Exception as err:    
        print(' ERROR  in fDf_JoinDf: {}'.format(str(err)))
        return df_left
    return df


#-------------------------------------------
# Compare DF (only a column) (done for WT)
#-------------------------------------------
def fBl_compareDfCol(d_1, d_2, str_how = 'inner'):
    # Param
    df1 =           d_1['df']
    str_colJoin1 =  d_1['colJoin']
    str_col1 =      d_1['colToCompare']
    df2 =           d_2['df']
    str_colJoin2 =  d_2['colJoin']
    str_col2 =      d_2['colToCompare']
    # Join the df
    df = df2[[str_colJoin2, str_col2]].copy()
    if str_colJoin1 != str_colJoin2:
        df[str_colJoin1] = df[str_colJoin2]
    df = fDf_JoinDf(df1, df, str_colJoin1, str_how)
    # Compare, make the difference
    df['col1-col2'] = (df[str_col1] - df[str_col2]).apply(round_corectPythonFlaws)
    # Prepare the case its not numbers to compare
    df_compare = df.loc[df['col1-col2'] != 0, [str_colJoin1, str_col1, str_col2,'col1-col2']]
    int_nbRowDiff = len(df_compare)
    if int_nbRowDiff == 0:  return True, None
    else:                   return False, df_compare


def fDf_imposerStr_0apVirgule(df, str_colName, int_0apVirgule = 2):
    try:
        df_result = df.copy()
        df_result[str_colName] = pd.to_numeric(df_result[str_colName])
        df_result[str_colName] = df_result[str_colName].astype(str) + '0' * int_0apVirgule
        df_temp = df_result[str_colName].str.split('.', n = 1, expand = True)
        if int_0apVirgule == 0: 
            df_result[str_colName] = df_temp[0] 
        else:
            df_temp[1] = df_temp[1].str.slice(0, int_0apVirgule)
            df_result[str_colName] = df_temp[0] + '.' + df_temp[1]
    except:
        print(' ERROR: fDf_imposerStr_0apVirgule did not work - it will pass without raising')
        print('  str_colName', str_colName, 'int_0apVirgule', int_0apVirgule)
        return df
    return df_result





#-------------------------------------------
# GROUP BY
#-------------------------------------------
def fDf_putBackColPivot_afGroupBy(df, str_colPivot):
    df[str_colPivot] = df.index                 # Put again the Column Pivot that disapear into index
    df.reset_index(drop = True, inplace = True) # reset_index
    df = df[[df.columns[-1]] + list(df.columns[:-1])]   # Put the col Pivot on first Position
    return df

def fDf_GroupBy(df_in, str_colPivot, str_colMeasure, d_aggPerCol = {}):
    df = fDf_CleanPrepareDF(df_in, l_colToBeFloat = [str_colMeasure], l_colToDropNA = [str_colPivot], o_fillNA_by = 0)
    # Sum is by default
    if d_aggPerCol == {}:
        d_aggPerCol = {str_colMeasure: 'sum'}
    # Group and have the colPivot as Index
    df_group = df.groupby(str_colPivot)
    # Aggregate the measures
    try:
        df = df_group.agg(d_aggPerCol)          
    except Exception as err:
        print('  error in fDf_GroupBy: {}'.format(err))
        df = df_group[str_colMeasure].sum()
    df = fDf_putBackColPivot_afGroupBy(df, str_colPivot)
    return df

def fDf_GroupBy_multiply(df_in, str_colPivot, l_colMeasure = []):
    df = fDf_CleanPrepareDF(df_in, l_colToBeFloat = l_colMeasure, l_colToDropNA = [str_colPivot], o_fillNA_by = 1)
    # Group and have the colPivot as Index
    df_group = df.groupby(str_colPivot)
    # Aggregate the measures
    try:
        df = df_group.prod()
        # df = df_group.apply(np.prod)
    except Exception as err:
        print('  error in fDf_GroupBy_multiply: {}'.format(err))
        raise
    df = fDf_putBackColPivot_afGroupBy(df, str_colPivot)
    return df

def fDf_GetFirst_onGroupBy(df_in, str_colPivot, str_colMeasure, bl_sort = True, l_ColSort = [], bl_ascending = False):
    df = fDf_CleanPrepareDF(df_in, l_colToBeFloat = [str_colMeasure], l_colToDropNA = [str_colPivot], o_fillNA_by = 0)
    # Get First on a Group By - 1 : Sort the value
    if l_ColSort:
        df.sort_values(by = l_ColSort, ascending = bl_ascending, inplace = True)
    elif bl_sort:
        df.sort_values(by = [str_colPivot, str_colMeasure], ascending = False, inplace = True)
    
    df_group = df.groupby(str_colPivot)                     # Group and have the colPivot as Index
    df = df_group.first()                                   # Keep only the first of the Column Pivot
    df = fDf_putBackColPivot_afGroupBy(df, str_colPivot)
    return df
    
def fDidDf_SplitDataframe(df_in, l_colTogether = ['ID']):
    dic_df = {}
    dic_value = {}
    # LOOP
    for i, row in enumerate(df_in.index):
        df_tmp = df_in.loc[row : row].copy()
        l_value = [df_in.loc[row, col] for col in l_colTogether]
        l_inOrOut = [x for x in l_value if x in dic_value]
        # NEW DF
        if l_inOrOut == []:
            dic_df[row] = df_tmp
            dic_row = {df_in.loc[row, col] : row for col in l_colTogether}
            dic_value.update(dic_row)
        #ROS TO ADD to existing DF
        else:
            int_iNumber = dic_value[l_inOrOut[0]]            
            dic_row = {df_in.loc[row, col] : row for col in l_colTogether}
            for val in dic_row.keys():
                if val not in dic_value:
                    dic_value[val] = int_iNumber
            dic_df[int_iNumber] = fDf_Concat_wColOfDf1(dic_df[int_iNumber], df_tmp, bl_colDf2_AsARow = False)
    return dic_df


    
