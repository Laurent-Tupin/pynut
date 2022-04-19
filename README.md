# pynut - Laurent Tupin

It provides various functions to simplify the users life. 


## Installation

You can install the package from [PyPI](https://pypi.org/project/pynut/):

    python -m pip install pynut

The package is supported on Python 3.7 and above.



## How to use


You can call a function as this example:

    $ ----------------------------------------------------
    >>> from pyNut import nutDate
    >>> nutDate.today()



This is the libraries I am using with the package

    $ ----------------------------------------------------
    >>> beautifulsoup4==4.7.1
    >>> exchangelib==4.7.2
    >>> openpyxl==3.0.5
    >>> pandas==1.1.3
    >>> paramiko==2.6.0
    >>> psutil==5.9.0
    >>> pyodbc==4.0.32
    >>> pywin32==303
    >>> selenium==3.141.0
    >>> xlrd==1.2.0
    >>> XlsxWriter==1.3.5
    >>> xlwings==0.20.8



To use nutAPI / Selenium Functionnalities:

    $ ----------------------------------------------------
    # To use Chrome Driver
    #  Go to chromedriver.chromium.org
    #  download and UnZip the folder
    #  Move it to Users/local/bin or C:\ProgramData\Anaconda3\Library\bin (Windows)


    


## Documentation

Temporary documentation for nutDate :

    from pyNut import nutDate as dat
    
    dte_date = dat.fDte_formatToDate(dte_date, str_dateFormat = '%d/%m/%Y')
    """ fDte_formatToDate makes sure you will have a varable with a date format
        The first Argument is the Variable (date), and the format of the string if it is a sting
        It allows you to avoid testing the type of the variable and get your get Date anyhow"""
    
    int_dateDiff = dat.fInt_dateDifference(dte_date1, dte_date2)
    """ fInt_dateDifference give you the difference in days between 2 dates"""
    
    Date2 = dat.fDte_convertExcelInteger(Date)
    """ fDte_convertExcelInteger takes an integer as input, 
        This is the integer you can find in Excel when it is a date 
        And return the associated date  """
    
    
Temporary documentation for nutDataframe :

    import pyNut.nutDataframe as dframe
    
    bl_isempty = dframe.fBl_isDataframeEmpty(df_simple)
    """ Test if a Dataframe is empty"""
    
    df_simple = dframe.fDf_createSimpleDataframe()
    """ Create a simple dataframe to make test"""
    
    bl_compare, df_compare = dframe.fBl_compareDfCol({'df': df_1, 'colJoin': 'colJoin','colToCompare':'data'},
                                                      {'df': df_2,'colJoin': 'colJoin','colToCompare':'data'})
    """ compare 2 dataframe one a numeric column by joining the df and returning the difference """
    
    df_1['DataRounded'] = df_1['DataToBeRounded'].apply(lambda x: dframe.round_down(x))
    """ Use the Math Function floor() - Able to add a decimals like in Excel
        floor() rounds down. int() truncates. 
        The difference is clear when you use negative numbers
        math.floor(-3.5)    -4
        int(-3.5)           -3"""
    
    df_2['DataRounded'] = df_2['DataToBeRounded'].apply(lambda x: dframe.round_up(x))
    """ Use the Math Function ceil() - Able to add a decimals like in Excel"""
    
    df_data = dframe.fDf_readCsv_enhanced(path, bl_header = None, str_sep = '|', l_names = range(33))
    """ Use the pandas method read_csv
        but resolving Parse Error and will try again after displaying a message 
        Also resolving UnicodeDecodeError by detecting the encoding and trying again accordingly """
     
    df2 = dframe.fDf_removeDoublons(df1)
    """ Remove all rows that are exactly the same"""
     
    df2 = dframe.fDf_DropRowsIfNa_resetIndex(df1, l_colToDropNA = ['col1'])
    """ Drop the rows where all defined columns will be Nan
        And reset the index"""
    
    df2 = dframe.dDf_fillNaColumn(df1, 'col2', 'col1')
    """ Replace Nan in a column by the value in another column or a Constant """
    
    df2 = dframe.fDf_fillColUnderCondition(df1, 'NameColApply', df1['data'], 'NameColC', 'YES', bl_except = False)
    ''' Transform DF with condition
        ValueToApply can be a value or a lambda function'''   
    
    
Temporary documentation for nutOther :
    
    from pyNut import nutOther as oth
    
    1. Decorators
    
    @oth.dec_singletonsClass
    class CLASS_TO_DECORATE():
    ''' Singeltons decorators: always use the first instance 
        Example: connection to database, FTP (keep the same connection for performance and possibly Access issue)
        '''    
    
    @oth.dec_getTimePerf(int_secondesLimitDisplay = 2)
    def function_TO_DECORATE(*args, **kwarks):
    ''' Time Performance Decorators on a function
        You can calculate and compare Performance on any function just by decorating it
        It will show nothing if the performance is better than a specific threshold you will defined
        '''   
    
    @oth.dec_stopProcessTimeOut(int_secondesLimit = 10, returnIfTimeOut = False)
    def function_TO_DECORATE(*args, **kwarks):
    ''' This decorators allow to stop a process if it is too long
        For example, testing a folder existence might be very very long...
        '''
    

Temporary documentation for nutFiles :

    from pyNut import nutFiles as fl
    
    1. Functions
    
    fileName = fl.fStr_myFileName(__file__)
    ''' Get the Python File Name '''
    
    myPath = fl.fStr_myPath(__file__)
    ''' Get the path of the Python File'''
    
    EnvUserName = fl.fStr_GetEnvUserName()
    ''' Get the Environment of the USERPROFILE'''
    
    UserEmail = fl.fStr_GetUserEmail(str_emailExtension = '@corporation.com')
    ''' Get the Corporate Email of the user '''
    
    folder = fl.fStr_GetFolderFromPath(myPath)
    ''' Get the Folder from a file path '''
    
    FileName = fl.fStr_GetFileFromPath(myPath)
    ''' Get the file Name from a file path '''
    
    l_files =   fl.fL_listFile(myFolder)
    """ Listing all files and folder in a folder using the library glob """
    
    l_files =   fl.fList_FileInDir(myFolder)
    """ Listing all files and folder in a folder using the library os """    
    
    if not fl.fBl_FileExist(_path):
    """ Test if a file exist. Giving a path, return a Boolean """
    
    if not fl.fBl_FolderExist(_path):
    """ Test if a folder exist. Giving a folder path, return a Boolean """
    
    if not fl.fBl_FolderExist_timeout(_path):
    """ Test if a folder exist. Giving a folder path, return a Boolean
        The function is decorated not to search for more than 10 secondes """
    
    fl.TrimTxtFile(str_path, bl_right = True)
    """ This function will Trim the space in a text file
        We can decide to Trim only the space on the left or right 
        By default, the Trim is both side"""
    
    fl.Act_Rename(str_newFolder, str_oldName, str_newName, False)
    """ Renaming a file and if it failed using the lib os, it will MOVE the file with shutil """
    
    newName = fl.fStr_TransformFilName_fromXXX_forGlobFunction(fileName, bl_exactNumberX = False)
    """ Change a string with unknown characters (XXXX) into sth understandable by the glob library
        'file_{*}_1.zip' ==> 'file_*_1.zip'     ( bl_exactNumberX = False)
        'file_{XXXX}_1.zip' ==> 'file_????.zip' ( bl_exactNumberX = True)
        'file_{XXXX}.zip' ==> 'file_*.zip'      ( bl_exactNumberX = False)
        """
    
    L_filIn =   fl.fL_GetFileListInFolder(myFolder, fileName_X, bl_searchOnly, bl_exactNb)
    """ Return the list of files in a folder that match the pattern given of the fileName 
        with {*} or {XXX} within """
    
    fileName = fl.fStr_GetMostRecentFile_InFolder(folder, fileName_X)
    """ Return the list of files in a folder that match the pattern given of the fileName
        with {*} or {XXX} within
        AND take the most recent one"""
    
    l_files_X = fl.fL_GetFileList_withinModel(l_files, str_fileName)
    """ If you have in memory a list of File Name
        you want to return the list of those who match the pattern given of the fileName
        with {*} or {XXX} within"""
    
    dte_modif = fl.fDte_GetModificationDate(myPath)
    """ Function Get the Modification Date of a file
        Useful for Update of App """
    
    l_pathReturn = fl.fL_KeepFiles_wTimeLimit(l_files, dte_after = 100)
    """ Filter a list of file Path to return the files that has been updated 
        after X days in the past and before Y days in the past 
        dte_after and dte_before can be date or integer of days in the past"""
    
    bl_creation = fl.fBl_createDir(myFolder)
    """ Create a Directory
        Return False if Directory exists, True if the folder has been created """
    
    o_file = fl.fO_readfile_parquet(str_pathFile, **d_options)
    """ fO_readfile_parquet reads parquet - require the libraries : pyarrow / fastparquet
        options: use_threads, engine='fastparquet', ... """
    
    str_sqlRequest = fl.fStr_ReadFile_sql(path)
    """ fStr_ReadFile_sql Opens and read the file as a single buffer"""
    
    df_data = fl.fDf_readExcelWithPassword(path, SheetName, ExcelPwd, 'A1:M400')
    """ You can read an Excel file protected with password - Requires to open the Excel App
        Also, for performance issue (and in order not to open Excel App again)
        it will create a csv copy named: fileName_sheetName.csv 
        Once the csv created, the same function will only use |pd.read_csv()|
        Return a Dataframe"""
    
    d_data = fl.fDic_readExcelWithPassword_sevSh(path, ExcelPwd, d_shName_areaToLoad)
    """ You can read an Excel file protected with password - Requires to open the Excel App
        Also, for performance issue (and in order not to open Excel App again)
        it will create 1 CSV per sheet in the spredsheet named: fileName_sheetName.csv
        Once all the csv created, the same function will only use |pd.read_csv()|
        Return a sictionary of Dataframe, key will be the SheetNames
        """
    
    df_data = pd_read_excel(str_path, str_SheetName, bl_header)
    """ To be able to read xlsx files with the function: |pd.read_excel|
        You need to have a previous xlrd version (xlrd==1.2.0)
        And replace the file xlsx.py (/Lib/site-packages/xlrd) by the one in this library !!!
        If it fails the engine openxyl will be used
        You can pass a sheet_name and a header as input
        """
    
    fl.fStr_createExcel_1Sh(path, '', df_PCF, str_SheetName = '', bl_header = False)
    """ Create a single sheet Excel file"""
    
    fl.fStr_createExcel_SevSh(path, '', l_dfData, l_SheetName, bl_header = True)
    """ Create a several sheets Excel file, Input is a list of Dataframe
        Will use pd.ExcelWriter and will no return any error depending of the version of xlrd
        if |options = d_options| wont work, |engine_kwargs = {'options' : d_options}| will be tried as well
        """
    
    fl.fStr_createExcel_SevSh_celByCel(path, '', l_dfData, l_SheetName)
    """ Create a several sheets Excel file
        Input is a list of Dataframe and list of Sheet Names
        Will use xlsxwriter and fill the Excel Cell by Cell
        Performance may be pretty low
        Preferable to use the function : fStr_createExcel_SevSh
        """
    
    fl.fStr_fillExcel_InsertNewSheet(path, '', df_data, str_SheetName)
    """ Take an existing  Excel file and insert a new sheet
        Input is a list of Dataframe - Will use pd.ExcelWriter 
        INSERT SHEET: 1 file out - 1 Dataframe - 1 Sheet """
    
    fl.fStr_fillXls_df_xlWgs_sevSh(folder, FileName, l_dfData, l_SheetName = l_shName)
    """ Take an existing Excel file and an existing sheet and fill it with new data
        Input is a Dataframe - Will use c_xlApp_xlwings class
        1 file out - 1 Dataframe - 1 Sheet"""
    
    str_path = fl.fStr_fillXls_df_xlWgs_sevSh(folder, FileName, l_dfData, l_SheetName = l_shName)
    """ Take an existing Excel file and several existing sheet and fill it with new data
        Input is a list of Dataframe, SheetNames - Will use c_win32_xlApp class
        1 fileout - n Dataframe - n Sheet"""
    
    Act_win32_SaveAsCleanFile(path, pathNew)
    """ Sometimes an Excel file is an old version and might be corrupted
        By Passing your file through this function, Excel App will be open, SaveAs and Close 
        so the new File will be useable by Python after"""
    
    df_donnee = fl.fDf_convertToXlsx(path, SheetName, bl_header = None)
    """ Will use Act_win32_SaveAsCleanFile to make sure the file is not corrupted
        and SaveAs XLSX instead of XLS 
        Read it and return the dataframe """
        
    df_donnee = fl.fDf_overwriteXlsx(path, SheetName, bl_header = None)
    """ Will use Act_win32_SaveAsCleanFile to save a non-corrupted XLSX file 
        Read it and return the dataframe """
    
    fl.Act_convertToXls_fromXlsx(path)
    """ Will use Act_win32_SaveAsCleanFile to make sure the file is not corrupted
        and SaveAs XLS instead of XLSX """
    
    fl.Act_win32OConvertXls_pdf(path)
    """ Will open an Excel file and convert it into PDF"""
    
    bl_tooOld = fl.fBl_fileTooOld(path, int_dayHisto = 10)
    """ Return a boolean to know if a file is older than N days in the past """
    
    fl.del_fichier_ifOldEnought(path,'', int_dayToKeep = 10)
    """ Check is a file is older than N days in the past 
        And if so, delete it 
        If the folder where the file is supposed to be does not exist, the function will create it"""
    
    fl.ZipExtractFile(ZipPath, pathDest, FileName, bl_extractAll=False, str_zipPassword='')
    """ Will read a ZIP file and extract its content in a destination folder
        It can take password
        It can extract all or only a file"""
    
    fl.Act_StyleIntoExcel(path, format, sheetName)
    """ Take an Excel Spreadsheet and a sheet and apply a format to it
        str_format is a dictionary within a string,
        the dictionary will be build by the fucntion eval
        Example of format:
            "{'A1:M500':{'font':{'name':'Calibri', 'size':9}},
            'B3:B5':{'font':{'name':'Calibri', 'size':10, 'bold':True,'color':styl.colors.WHITE},
                    'alignment':{'horizontal':'right'},
                    'fill':{'patternType':'solid', 'fill_type':'solid', 'fgColor': 'F2F2F2'}},
            'Column_size':{'A':50,'B':35,'C':10,'D':10,'E':15,'F':15,'G':18,'H':10},
            'Table_bord':{'A3:A11':'normBlack', 'B3:B11':'normBlack'},
            'Table_bord_full':{'A1:B1':'normBlack'},
            'Table_bord_EndDown_full':{'A13':'normBlack'},
            'num_format':{'B6:B6':'#,##0.0000', 'B7:B8':'#,##0'},
            'num_format_col':{'G13':'#,##0.00',  'H13':'0.00%'}
            }"
        """
        
    Act_KillExcel()
    """ This function kills all session of Excel
        Including the 'ghost' session you would kill from the Task Manager """
    
    
    2. Class
    
    inst_xlWings = c_xlApp_xlwings()
    inst_xlWings.FindXlApp(bl_visible = True, bl_screen_updating = False, bl_display_alerts = False)
    inst_xlWings.OpenWorkbook(path)
    inst_xlWings.DefineWorksheet(SheetName, i + 1)
    inst_xlWings.InsertDf_inRange(df_data)
    inst_xlWings.close_Book(bl_saveBeforeClose = True)
    """ The class allow you to manage excel with the library xlwings which might work better than win32
        Open the Excel Office App, Close, Save, define / rename / create sheet, fill an area
        The class is decorated to be a singleton so we always use the same instance of Excel
        DOC: https://docs.xlwings.org/en/stable/api.html
        """
    
    inst_xlApp = fl.c_win32_xlApp()
    inst_xlApp.FindXlApp(bl_visible = True)
    inst_xlApp.OpenWorkbook(str_path)
    inst_xlApp.xlApp.DisplayAlerts = False
    inst_xlApp.ConvertToPdf()
    inst_xlApp.CloseWorkbook(bl_saveBeforeClose = True)
    """ The class allow you to manage excel with the library win32com.client
        Open the Excel Office App, Close, Save, define / rename / create sheet, fill an area
        The class is decorated to be a singleton so we always use the same instance of Excel
        """
    

Temporary documentation for nutApi :

    from pyNut import nutApi as Api
        
    1. Class
    
    inst_getAPI = Api.C_API_simple( (str_uid, str_pwd) )
    inst_getAPI.api_connect_json( url )
    inst_getAPI.api_returnDataFrame( l_url_keyword = ['data', 'price'] )
    df_data = inst_getAPI.df_return
    """ The class inherit from C_API 
            allows the user to read an URL and get back a dataframe from JSON format
        Is decorated to be a singleton"""
    
    
    
    
    
    
    
    
***END***