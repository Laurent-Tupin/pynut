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
    
    
    
    
    

Temporary documentation for nutFiles :

    from pyNut import nutFiles as fl
    
    l_fileList_consti = fl.fL_listFile(str_path_consti)
    "" fL_listFile is listing all files in a folder using the library glob """
    
    o_file = fl.fO_readfile_parquet(str_path)
    """ fO_readfile_parquet reads parquet - require the libraries : pyarrow / fastparquet"""
    
    
    
___END______________________




