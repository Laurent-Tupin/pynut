import os
import datetime
import pytest
try:
    import nutFiles as fl
except:
    print('Online Test...')
    from pyNut import nutFiles as fl


#=============================================================================
# UNIT TEST
#=============================================================================
def test_fStr_myFileName():
    fileName_os =   os.path.basename(__file__)
    fileName =      fl.fStr_myFileName(__file__)
    assert (fileName_os == fileName)
def test_fStr_myPath():
    path_os =       os.path.dirname(os.path.abspath(__file__))
    myPath =        fl.fStr_myPath(__file__)
    assert (path_os == myPath)
def test_fStr_GetEnvUserName():
    EnvUserName =   fl.fStr_GetEnvUserName()
    EnvUserName_os = os.environ['USERPROFILE']
    assert (EnvUserName == EnvUserName_os)
def test_fStr_GetFolderFromPath():
    myPath =        fl.fStr_myPath(__file__) + '\\' + fl.fStr_myFileName(__file__)
    folder =        fl.fStr_GetFolderFromPath(myPath)
    str_folder =    fl.fStr_myPath(__file__)
    assert (folder == str_folder)
def test_fStr_GetFileFromPath():
    myPath =        fl.fStr_myPath(__file__) + '\\' + fl.fStr_myFileName(__file__)
    myFileName =    fl.fStr_GetFileFromPath(myPath)
    str_fileName =  fl.fStr_myFileName(__file__)
    assert (myFileName == str_fileName)
def test_fStr_BuildPath():
    myPath =        fl.fStr_myPath(__file__) + '\\' + fl.fStr_myFileName(__file__)
    folder =        fl.fStr_myPath(__file__)
    myFileName =    fl.fStr_myFileName(__file__)
    Path_0 =        fl.fStr_BuildPath(folder, myFileName)
    Path_1 =        fl.fStr_BuildPath(myPath, '')
    Path_2 =        fl.fStr_BuildPath('', myPath)
    assert (Path_0 == Path_1)
    assert (Path_0 == Path_2)

def test_fL_listFile():
    myFolder =  fl.fStr_myPath(__file__)
    fileName =  fl.fStr_myFileName(__file__)
    l_files =   fl.fL_listFile(myFolder)
    l_files = [fl.fStr_GetFileFromPath(path) for path in l_files]
    assert (fileName in l_files)

@pytest.mark.parametrize("fileName, expectedReturn, bl_exactNumb",
                         [('file_{*}_1.zip', 'file_*_1.zip', False),
                          ('file_{XXXX}.zip', 'file_????.zip', True),
                          ('file_{XXXX}.zip', 'file_*.zip', False)])
def test_fStr_TransformFilName_fromXXX_forGlobFunction(fileName, expectedReturn, bl_exactNumb):
    str_newName = fl.fStr_TransformFilName_fromXXX_forGlobFunction(fileName, bl_exactNumberX = bl_exactNumb)
    assert str_newName == expectedReturn

@pytest.mark.parametrize("fileName_X, bl_searchOnly, bl_exactNb, exp_fileName",
                         [('test_{XXX}Files.py', False, True, None),
                          ('test_{XX}Files.py', False, False, None),
                          ('test_{XX}Files.py', False, True, None),
                          ('test_{*}Files.py', False, True, None),
                          ('test_{X}Files.py', False, True, None),
                          ('abc_{XXX}_abc.py', True, None, 'abc_{XXX}_abc.py')
                          ])
def test_fL_GetFileListInFolder(fileName_X, bl_searchOnly, bl_exactNb, exp_fileName):
    myFolder =  fl.fStr_myPath(__file__)
    if exp_fileName is None:    fileName = fl.fStr_myFileName(__file__)
    else:                       fileName = exp_fileName
    L_filIn =   fl.fL_GetFileListInFolder(myFolder, fileName_X, bl_searchOnly, bl_exactNb)
    L_filIn = [fl.fStr_GetFileFromPath(path) for path in L_filIn]
    assert (fileName in L_filIn)

@pytest.mark.parametrize("fileName_X, bl_searchOnly, bl_exactNb",
                         [('abc_{XXX}_abc.py', False, True),
                          ('abc_{XXX}_abc.py', False, False)])
def test_FAIL_fL_GetFileListInFolder(fileName_X, bl_searchOnly, bl_exactNb):
    myFolder =  fl.fStr_myPath(__file__)
    with pytest.raises(Exception):
        fl.fL_GetFileListInFolder(myFolder, fileName_X, bl_searchOnly, bl_exactNb)

@pytest.mark.parametrize("fileName_X, bl_searchOnly, bl_exactNb, exp_fileName",
                         [('test_{XXX}Files.py', False, True, None),
                          ('test_{XX}Files.py', False, False, None),
                          ('test_{XX}Files.py', False, True, None),
                          ('test_{*}Files.py', False, True, None),
                          ('test_{X}Files.py', False, True, None),
                          ('abc_{XXX}_abc.py', True, None, 'abc_{XXX}_abc.py')
                          ])
def test_fStr_GetMostRecentFile_InFolder(fileName_X, bl_searchOnly, bl_exactNb, exp_fileName):
    myFolder =  fl.fStr_myPath(__file__)
    if exp_fileName is None:    fileName = fl.fStr_myFileName(__file__)
    else:                       fileName = exp_fileName
    str_fileName =  fl.fStr_GetMostRecentFile_InFolder(myFolder, fileName_X, bl_searchOnly, bl_exactNb)
    assert (fileName == str_fileName)

@pytest.mark.parametrize("fileName_X, bl_searchOnly, bl_exactNb",
                         [('abc_{XXX}_abc.py', False, True),
                          ('abc_{XXX}_abc.py', False, False)])
def test_FAIL_fStr_GetMostRecentFile_InFolder(fileName_X, bl_searchOnly, bl_exactNb):
    myFolder =  fl.fStr_myPath(__file__)
    with pytest.raises(Exception):
        fl.fStr_GetMostRecentFile_InFolder(myFolder, fileName_X, bl_searchOnly, bl_exactNb)


@pytest.mark.parametrize("fileName_X",
                         [('test_nutFiles.py'), ('_nutFiles.py'),
                          ('test_{XXX}Files.py'), ('test_{XX}Files.py'), ('test_{X}Files.py'),
                          ('test_{*}Files.py')])
def test_fL_GetFileList_withinModel(fileName_X):
    myFolder =  fl.fStr_myPath(__file__)
    fileName =  fl.fStr_myFileName(__file__)
    l_files =   fl.fL_listFile(myFolder)
    l_files_X = fl.fL_GetFileList_withinModel(l_files, fileName_X)
    l_files_X = [fl.fStr_GetFileFromPath(path) for path in l_files_X]
    assert (fileName in l_files_X)
    assert (len(l_files_X) == 1)

@pytest.mark.parametrize("fileName_X", [('test_{XXXFiles.py')])
def test_fL_GetFileList_withinModel_2(fileName_X):
    myFolder =  fl.fStr_myPath(__file__)
    fileName =  fl.fStr_myFileName(__file__)
    l_files =   fl.fL_listFile(myFolder)
    l_files_X = fl.fL_GetFileList_withinModel(l_files, fileName_X)
    l_files_X = [fl.fStr_GetFileFromPath(path) for path in l_files_X]
    assert (fileName in l_files_X)

@pytest.mark.parametrize("fileName_X", [('abc_{XXX}_abc.py')])
def test_fL_GetFileList_withinModel_empty(fileName_X):
    myFolder = fl.fStr_myPath(__file__)
    l_files = fl.fL_listFile(myFolder)
    l_files_X = fl.fL_GetFileList_withinModel(l_files, fileName_X)
    assert (len(l_files_X) == 0)

def test_fDte_GetModificationDate():
    myPath = fl.fStr_myPath(__file__) + '\\' + fl.fStr_myFileName(__file__)
    dte_modif = fl.fDte_GetModificationDate(myPath)
    assert (isinstance(dte_modif, datetime.datetime))


def test_fL_KeepFiles_wTimeLimit():
    myFolder = fl.fStr_myPath(__file__)
    l_files = fl.fL_listFile(myFolder)
    l_pathReturn = fl.fL_KeepFiles_wTimeLimit(l_files, dte_after = 100_000)
    assert (isinstance(l_pathReturn, list))
    assert(len(l_pathReturn) > 0)
    l_pathEmpty = fl.fL_KeepFiles_wTimeLimit(l_files, dte_after=-1)
    # print('l_pathEmpty', l_pathEmpty)
    # print(len(l_pathEmpty))
    assert (isinstance(l_pathEmpty, list))
    assert (l_pathEmpty == [])

def test_fBl_createDir():
    myFolder = fl.fStr_myPath(__file__)
    bl_creation = fl.fBl_createDir(myFolder)
    assert (bl_creation is False)
    # We wont create a folder for a Unit Test

def test_fBl_fileTooOld():
    myPath = fl.fStr_myPath(__file__) + '\\' + fl.fStr_myFileName(__file__)
    bl_tooOld = fl.fBl_fileTooOld(myPath, int_dayHisto=100_000)
    assert (bl_tooOld is False)
    bl_tooOld = fl.fBl_fileTooOld(myPath, int_dayHisto=-1)
    assert (bl_tooOld is True)
    myPath_noFile = fl.fStr_myPath(__file__) + '\\aaabbbccc.csv'
    bl_tooOld = fl.fBl_fileTooOld(myPath_noFile, int_dayHisto=-1)
    assert (bl_tooOld is False)
