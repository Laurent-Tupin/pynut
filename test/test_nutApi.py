import pytest
try:
    import nutApi as api
except:
    print('Online Test...')
    from pyNut import nutApi as api


# # =============================================================================
# # UNIT TEST
# # =============================================================================
# def test_selClass_openClose():
#     # ----------------------------------------------------
#     # To use Chrome Driver
#     #  Go to chromedriver.chromium.org || https://sites.google.com/a/chromium.org/chromedriver/downloads
#     #  Chose an older version (like the 92 as of August 2021)
#     #  download and UnZip the folder
#     #  Move ||chromedriver.exe||  to Users/local/bin
#     # ----------------------------------------------------
#     str_url = 'https://www.yuantaetfs.com/tradeInfo/pcf/0050'
#     inst_sel = api.c_Selenium_InteractInternet(str_url)
#     inst_sel.sel_quit()
#
#
# def test_selClass_clic():
#     # One true Clic
#     str_url = 'https://www.yuantaetfs.com/tradeInfo/pcf/0050'
#     str_buttonName = 'Select Funds'
#     str_button_selectFunds = '/html/body/div/div/div/section/div/div/div[2]/div[1]/a/span'
#     inst_sel = api.c_Selenium_InteractInternet(str_url)
#     inst_sel.clic(str_buttonName, str_button_selectFunds, [])
#     inst_sel.sel_quit()
#     assert inst_sel.realButtonName == str_buttonName
#
#
# def test_selClass_clicSecond():
#     # Several try on wrong button
#     str_url = 'https://www.yuantaetfs.com/tradeInfo/pcf/0050'
#     str_buttonName = 'Select Funds'
#     str_button_selectFunds = '/html/body/div/div/div/section/div/div/div[2]/div[1]/a/span'
#     str_button_expExcel = '/html/body/div/div/div/section/div/div/div[2]/div[2]/div/div[1]/div[2]/span'
#     inst_sel = api.c_Selenium_InteractInternet(str_url)
#     inst_sel.clic(str_buttonName, str_button_expExcel, [str_button_selectFunds])
#     inst_sel.sel_quit()
#     assert inst_sel.realButtonName == str_buttonName
#
#
# def test_selenium_clicLaunch():
#     str_url = 'https://www.yuantaetfs.com/tradeInfo/pcf/0050'
#     str_buttonName = 'Select Funds'
#     str_button_selectFunds = '/html/body/div/div/div/section/div/div/div[2]/div[1]/a/span'
#     bl_return = api.selenium_clicLaunch(str_url, str_button_selectFunds, str_buttonName)
#     assert bl_return == True
