import os
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
    l_files =   fl.fL_listFile(myFolder)
    fileName =  fl.fStr_myFileName(__file__)
    assert (fileName in fileName)


@pytest.mark.parametrize("fileName, expectedReturn, bl_exactNumb",
                         [('file_{*}_1.zip', 'file_*_1.zip', False),
                          ('file_{XXXX}.zip', 'file_????.zip', True),
                          ('file_{XXXX}.zip', 'file_*.zip', False)])
def test_fStr_TransformFilName_fromXXX_forGlobFunction(fileName, expectedReturn, bl_exactNumb):
    str_newName = fl.fStr_TransformFilName_fromXXX_forGlobFunction(fileName, bl_exactNumberX = bl_exactNumb)
    assert str_newName == expectedReturn


@pytest.mark.parametrize("fileName_X, bl_searchOnly, bl_exactNb, exp_fileName",
                         [('test_{XXX}Files.py', False, True, None),
                          # ('test_{XX}Files.py', False, False, None),
                          # ('test_{*}Files.py', False, True, None),
                          # ('test_{X}Files.py', False, True, None),
                          # ('abc_{XXX}_abc.py', True, None, 'abc_{XXX}_abc.py')
                          ])
def test_fL_GetFileListInFolder(fileName_X, bl_searchOnly, bl_exactNb, exp_fileName):
    myFolder =  fl.fStr_myPath(__file__)
    if exp_fileName is None:    fileName = fl.fStr_myFileName(__file__)
    else:                       fileName = exp_fileName
    L_filIn =   fl.fL_GetFileListInFolder(myFolder, fileName_X, bl_searchOnly, bl_exactNb)
    assert (fileName in L_filIn)


