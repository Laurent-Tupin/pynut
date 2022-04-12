from time import sleep
# import pytest
try:
    import nutOther as oth
except:
    print('Online Test...')
    from pyNut import nutOther as oth


@oth.dec_singletonsClass
class C_Example:
    def __init__(self, Param1):
        self.Param1 = Param1

@oth.dec_getTimePerf(1)
def fct1():
    sleep(0.1)
    return True
@oth.dec_getTimePerf(1)
def fct2():
    sleep(1.1)
    return True

@oth.dec_stopProcessTimeOut(int_secondesLimit = 1, returnIfTimeOut = False)
def fct3():
    sleep(0.1)
    return True
@oth.dec_stopProcessTimeOut(int_secondesLimit = 1, returnIfTimeOut = False)
def fct4():
    sleep(1.1)
    return True



#=============================================================================
# UNIT TEST
#=============================================================================
def test_dec_singletonsClass():
    instance1 = C_Example('Input 1')
    instance2 = C_Example('Input 2')
    assert (instance1.Param1 == instance2.Param1 )

def test_dec_getTimePerf():
    ret1 = fct1()
    ret2 = fct2()
    assert (ret1 is True)
    assert (ret2 is True)

def test_dec_getTimePerf():
    ret1 = fct3()
    ret2 = fct4()
    assert (ret1 is True)
    assert (ret2 is False)
