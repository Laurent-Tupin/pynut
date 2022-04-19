try:
    from . import _lib as lib
    from . import nutOther as oth
except:
    try:
        import _lib as lib
        import nutOther as oth
    except:
        from pyNut import _lib as lib
        from pyNut import nutOther as oth
os          = lib.os()
time        = lib.time()
pd          = lib.pandas()
re          = lib.re()
requests    = lib.requests()
# from urllib.request import urlopen, urlretrieve
BeautifulSoup = lib.BeautifulSoup()
unicodedata = lib.unicodedata()
try:
    selenium_webdriver = lib.selenium_webdriver()
except:
    from selenium import webdriver as selenium_webdriver



#---------------------------------------------------------------
#------------- CLASS API ----------------------------
#---------------------------------------------------------------
class C_API:
    """ The class allows the user to read an URL and get back a dataframe from JSON format"""
    def __init__(self, d_auth={}, d_headers={}):
        # d_headers = {'User-Agent': 'Chrome/71.0.3578.98'}
        # d_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) Safari/605.1.15",
        #            "Accept-Language": "en-gb",
        #            "Accept-Encoding":"br, gzip, deflate",
        #            "Accept":"test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #            "Referer":"http://www.google.com/"}
        # d_headers = {'Authorization': '...'}
        self.d_credentials = {}
        self.d_headers =    d_headers
        self.d_auth =       d_auth
    def api_connect_json(self, str_url, bl_raiseErrorIfNoPage = True, bl_verify = True):
        # Existing Connection
        str_auth =      oth.fDic_GetStrFromDic(self.d_auth)
        str_headers =   oth.fDic_GetStrFromDic(self.d_headers)
        if (str_url, str_auth, str_headers) in self.d_credentials:
            self.j_resp = self.d_credentials[ (str_url, str_auth, str_headers) ]
            return self.j_resp
        # NEW Connection
        self.__url = str_url
        self.__verify = bl_verify
        # Process
        self.api_connect()
        self.api_checkConnexion(bl_raiseIfFalse = bl_raiseErrorIfNoPage)
        self.api_jsonBuild()
        # Save for later
        d_credentials = self.d_credentials
        d_credentials[ (str_url, str_auth, str_headers) ] = self.j_resp
        return self.j_resp
    def api_connect(self):
        d_param = {}
        if not self.d_auth == {}:       d_param['auth'] = self.d_auth
        if not self.d_headers == {}:    d_param['headers'] = self.d_headers
        if self.__verify is False:      d_param['verify'] = False
        try:
            o_page = requests.get(self.__url, **d_param)
        except Exception as err:
            print(' ERROR in api_connect: requests.get(str_url)')
            print(' - Type of error: ', type(err).__name__)
            print(' - ', err)
            print(' - ', self.__url)
            print(' - ', oth.fDic_GetStrFromDic(d_param), '\n')
            raise
        self.o_page = o_page
        return o_page
    def api_checkConnexion(self, bl_raiseIfFalse = False):
        try:
            if self.o_page.status_code == 200:
                return True
        except Exception as err:
            print('  ** ERROR in api_checkConnexion: {}'.format(err))
        print(' ERROR in api_checkConnexion, Connexion close for the status code of the page is not 200')
        print(' - Status code of the page is: {}'.format(self.o_page.status_code))
        print(' - URL is: ', self.__url, '\n')
        # Retour
        if bl_raiseIfFalse is True: raise
        else:                       return False
    def api_jsonBuild(self):
        try:
            j_resp = self.o_page.json()
        except:
            print(' ERROR in api_jsonBuild: json')
            print(' - ', self.__url, '\n')
            raise
        self.j_resp = j_resp
        return j_resp
    # -------------------------------------------------------------------

    def api_returnDataFrame(self, l_url_keyword=[], str_furtherSplit = ''):
        self.bl_errorOnRoll = False
        self.api_rollOnKeyword(l_url_keyword)
        self.api_rollOn_List_ofDic(str_furtherSplit)
        self.api_jsonToDataframe()
        return self.df_return
    def api_rollOnKeyword(self, l_url_keyword=[]):
        self.l_url_keyword = l_url_keyword
        j_resp = self.j_resp
        j_tableau = j_resp
        try:
            if l_url_keyword:
                for keyW in l_url_keyword:
                    if not keyW == '':
                        j_tableau = j_tableau[keyW]
        except:
            print(' INFO (API): there is no data on URL: {}'.format(self.__url))
            print('     *** with the keyword: |{}|'.format('|'.join(l_url_keyword)), '\n')
            self.bl_errorOnRoll = True
            return False
        self.j_tableau = j_tableau
    def api_rollOn_List_ofDic(self, str_furtherSplit=''):
        if str_furtherSplit == '':
            return True
        str_keyOfDestDic =  str_furtherSplit.split(':')[-1]
        str_furtherSplit =  str_furtherSplit.split(':')[0]
        str_key =           str_furtherSplit.split('=')[0]
        str_valueToChoose = str_furtherSplit.split('=')[1]
        j_list = self.j_tableau
        l_result = []
        try:
            for elem in j_list:
                if isinstance(elem, dict):
                    if elem[str_key] == str_valueToChoose:
                        d_result = elem[str_keyOfDestDic]
                        for k, v in d_result.items():
                            l_result.append({str_valueToChoose : k, str_keyOfDestDic : v})
                        self.j_tableau = l_result
                        return True
                else:   print('   ***INFO : api_rollOnList_ofDic only works with List of dictionary')
        except:
            print(' WARNING : api_rollOnList_ofDic,  str_key: |{}| and the value: |{}|'.format(str_key, str_valueToChoose))
            print('  - URL: |{}|'.format(self.__url), '\n')
            self.bl_errorOnRoll = True
            return False
        return True

    def api_jsonToDataframe(self):
        if self.bl_errorOnRoll is True:
            df_returnError = pd.DataFrame(columns=range(0, 3))
            df_returnError.loc[len(df_returnError)] = [self.__url, str('||'.join(self.l_url_keyword)), 'NULL']
            self.df_return = df_returnError
            return df_returnError
        # Transform to DATAFRAME
        try:
            try:
                df_return = pd.DataFrame(self.j_tableau)
            except ValueError:
                df_return = pd.DataFrame(self.j_tableau, index=[0])
        except Exception as err:
            print(' ERROR in api_jsonToDataframe: pd.DataFrame')
            print(' - Type of error: ', type(err).__name__)
            print(' - ', err)
            print(' - ', self.__url)
            print(' - ', self.l_url_keyword, '\n')
            raise
        self.df_return = df_return
        return df_return
#______________________________________________________________________________


#@oth.dec_singletonsClass
class C_API_simple(C_API):
    """ The class inherit from C_API
        allows the user to read an URL and get back a dataframe from JSON format
    Is decorated to be a singleton"""
    def __init__(self, d_auth={}, d_headers={}):
        super().__init__(d_auth, d_headers)


#@oth.dec_singletonsClass
class C_API_checkIndex(C_API):
    """ The class inherit from C_API
            allows the user to read an URL and get back a dataframe from JSON format
        Is decorated to be a singleton
        Check Data within
        """
    def __init__(self, d_auth={}, d_headers={}):
        super().__init__(d_auth, d_headers)
    def api_con_Check(self, str_url, bl_raiseErrorIfNoPage = True, bl_verify = True, d_check = {}):
        self.d_check = d_check
        self.api_connect_json(str_url, bl_raiseErrorIfNoPage = bl_raiseErrorIfNoPage, bl_verify = bl_verify)
        self.api_checkIndexPos()
        return self.j_resp
    def api_checkIndexPos(self):
        d_check = self.d_check
        try:
            if d_check:
                bl_check = self.fBl_Check_indexPosition(self.j_resp, d_check = d_check)
                if not bl_check:    print(' - ', self.__url)
        except Exception as err:
            print(' ERROR in api_checkIndexPos: Check')
            print(' - Type of error: ', type(err).__name__)
            print(' - ', err)
            print(' - ', self.__url)
            print(' - ', d_check, '\n')
    def fBl_Check_indexPosition(self, j_resp, l_url_keyword=['result', 'indexPositions'], d_check = {}):
        str_indexRic = d_check['str_indexRic']
        dte_url = d_check['dte_url']
        if l_url_keyword:
            for keyW in l_url_keyword:
                j_resp = j_resp[keyW]
        df_index_positions = pd.DataFrame(j_resp)
        dte_pos_isopen = df_index_positions.loc[df_index_positions['Ric'] == str_indexRic, 'IsOpen'].values[0]
        dte_pos_pubdate = \
        df_index_positions.loc[df_index_positions['Ric'] == str_indexRic, 'AsAtDate'].reset_index(drop=True)[0]
        if dte_pos_isopen != 1:
            print('\n WARNING: dte_pos_isopen is not 1 \n')
            return False
        elif dte_url != dte_pos_pubdate:
            print('\n WARNING: Index publication date incorrect for Underlying Index: ', dte_pos_pubdate, dte_url)
            print(type(dte_pos_pubdate), type(dte_url), '\n')
            return False
        else:
            return True
#______________________________________________________________________________




#=============================================================================
# Launch the CLASS
#=============================================================================
def fDf_Launch_APIclass(str_url, d_auth = {}, d_headers = {}, l_url_keyword = [], str_furtherSplit = '', bl_raiseErrorIfNoPage = True, bl_verify = True, d_check = {}):
    if d_check == {}:
        inst_getAPI = C_API_simple(d_auth, d_headers)
        inst_getAPI.api_connect_json(str_url, bl_raiseErrorIfNoPage = bl_raiseErrorIfNoPage, bl_verify = bl_verify)
    else:
        inst_getAPI = C_API_checkIndex(d_auth, d_headers)
        inst_getAPI.api_con_Check(str_url, bl_raiseErrorIfNoPage=bl_raiseErrorIfNoPage, bl_verify=bl_verify, d_check = d_check)
    inst_getAPI.api_returnDataFrame(l_url_keyword = l_url_keyword, str_furtherSplit = str_furtherSplit)
    df = inst_getAPI.df_return
    return df

@oth.dec_stopProcessTimeOut(int_secondesLimit = 30, returnIfTimeOut = False)
def fDf_Launch_APIclass_timeout(str_url, d_auth = {}, d_headers = {}, l_url_keyword = [], str_furtherSplit = '',bl_raiseErrorIfNoPage = True, bl_verify = True, d_check = {}):
    df = fDf_Launch_APIclass(str_url, d_auth = d_auth, d_headers = d_headers, l_url_keyword = l_url_keyword, str_furtherSplit = str_furtherSplit,
                             bl_raiseErrorIfNoPage = bl_raiseErrorIfNoPage, bl_verify = bl_verify, d_check = d_check)
    return df






#=============================================================================
# FUNCTION
#=============================================================================
def Act_WaitTranslation(int_sec = 5):
    print('  * Wait for Translation {} secondes ...'.format(str(int_sec)))
    time.sleep(int_sec)

def fBl_ChineseInString(str_stringToTest):
    l_result = re.findall(r'[\u4e00-\u9fff]+', str_stringToTest)
    if l_result:    return True
    return False

def fBL_checkConnexion(o_page):
    try: 
        if o_page.status_code == 200: 
            return True
        else: 
            print(' Connexion close for the status code of the page is not 200 ' )
            print(' - Status code of the page is: ' + o_page.status_code)
    except: 
        print('  ERROR in fBL_checkConnexion: Connexion fails because the input is not a page')
    return False



#==============================================================================
# BEAUTIFUL SOUP
#==============================================================================
def fDf_htmlGetArray_Soup(str_url, bl_th = False, bl_waitForTranslation = False, int_waitTime = 0, bl_cleanXA0 = True, int_waitTimeLimit = 5):  
    arr_result = []
    try:
        d_headers = {'User-Agent': 'Chrome/71.0.3578.98'}
        o_page = requests.get(str_url, headers = d_headers)
        if bl_waitForTranslation and int_waitTime != 0:     Act_WaitTranslation(int_waitTime)
    except:
        print(' ERROR in fDf_htmlGetArray_Soup: requests.get(str_url)')
        print(' -  ', str_url)
        raise
    if not fBL_checkConnexion(o_page): 
        print(' ERROR in fDf_htmlGetArray_Soup: fBL_checkConnexion(o_page): ')
        print(' -  ', str_url)
        return False    
    try:
        bs_soup = BeautifulSoup(o_page.content, "html.parser")      # lxml   # html5lib
        #bs_soup = bs_soup.replace(u'\xa0', ' ')
        #bs_soup.prettify(formatter = lambda x: x.replace(u'\xa0', ' '))
        #bs_soup.prettify(formatter = lambda x: x.replace(r'&nbsp;', ' '))
    except:
        print(' ERROR in fDf_htmlGetArray_Soup: BeautifulSoup(o_page.content, "html.parser")')
        print(' -  ', str_url)
        raise
    try:
        l_doublon = []
        for o_table in  bs_soup.find_all('table'):
            for o_row in o_table.find_all('tr'):
                # Remove doublons
                if o_row in l_doublon:
                    break
                l_doublon.append(o_row)
                # Balise Th = Text / Titre
                o_th = [o_cell.text.strip() for o_cell in o_row.find_all('th')]                
                if bl_th and o_th:      o_cells = o_th
                else:                   o_cells = []
                # Balise TD = Chiffre
                o_td = [o_cell.text.strip() for o_cell in o_row.find_all('td')]
                if o_td:                o_cells = o_cells + o_td
                elif o_th:              o_cells = o_th
                else:                   o_cells = []    
                # Clean Cells
                if bl_cleanXA0:
                    o_cells = [unicodedata.normalize("NFKD",cel_Text) for cel_Text in o_cells]
                    o_cells = [cel_Text.replace('\n', '  ').replace('\r', '') for cel_Text in o_cells]
                # add the row to result
                if o_cells:   arr_result.append(o_cells)
                # Chinese Translation - Recursive                
                if bl_waitForTranslation:
                    for cell in o_cells:
                        if fBl_ChineseInString(cell):
                            if int_waitTime > int_waitTimeLimit:
                                print('   *_* ERROR : still Chinese within Result: ', cell)
                                print('   *_!!!_* Cannot wait anymore, Do it manually: ')
                                print('   *_URL_* ', str_url)
                                break
                            else:
                                int_waitTime = (int_waitTime + 1)*2
                            print('   *_* ERROR : still Chinese in Result: ', cell)
                            df_return = fDf_htmlGetArray_Soup(str_url, bl_th, True, int_waitTime)
                            return df_return
        df = pd.DataFrame(arr_result)
        l_doublon = []
    except Exception as err:
        print(' ERROR in fDf_htmlGetArray_Soup: LOOP on tables / rows / cells')
        print(' - ', str_url)
        print(' -  Erreur: ', err)
        raise
    return df



#==============================================================================
# SELENIUM
#==============================================================================
class c_Selenium_InteractInternet:
    #----------------------------------------------------
    # To use Chrome Driver
    #  Go to chromedriver.chromium.org
    #  download and UnZip the folder
    #  Move it to Users/local/bin
    #----------------------------------------------------
    def __init__(self, str_url):
        o_options = self.getOptions_stopMessage()
        self.driver = selenium_webdriver.Chrome(options = o_options)
        self.driver.get(str_url)
        self.realButtonName = ''
        
    def getOptions_stopMessage(self):
        options = selenium_webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return options
        
    def findElementByXpath(self, str_buttonxPath):
        time.sleep(1)
        try:    btn_click = self.driver.find_element_by_xpath(str_buttonxPath)
        except Exception as err:
            print(' INFO : Could not do the clic {}   ... Will wait 5 secondes'.format(err))
            time.sleep(5)
            btn_click = self.driver.find_element_by_xpath(str_buttonxPath)
        return btn_click
   
    def clic(self, str_buttonName, str_buttonxPath, l_buttonIfFailed):
        #----------------------------------------------------
        # Right click on the button and chose Inspect
        # Spot the button Type
        # Right Click and Copy XPath, You get the XPATH
        #----------------------------------------------------
        btn_click = self.findElementByXpath(str_buttonxPath)
        realButtonName = str(btn_click.text)
        self.realButtonName = realButtonName
        if not str_buttonName.lower() in realButtonName.lower():
            print('Link found was not |{}| but: |{}|'.format(str_buttonName,realButtonName))
            for xPath in l_buttonIfFailed:
                time.sleep(5)
                self.clic(str_buttonName, xPath, [x for x in l_buttonIfFailed if x != xPath])
                # btn_click = self.driver.find_element_by_xpath(xPath)
                # print('Link is: {}'.format(btn_click.text))
                # btn_click.click()
        else:   btn_click.click()
        
    def fillUp(self, str_buttonxPath, str_textToFill):
        time.sleep(2)
        fld_toFill = self.driver.find_element_by_xpath(str_buttonxPath)
        fld_toFill.send_keys(str_textToFill)
    
    def changeWindow(self, int_nbWindow):
        self.baseWindow = self.driver.window_handles[0]
        int_nbWindow = int_nbWindow % len(self.driver.window_handles)
        self.newWindow = self.driver.window_handles[int_nbWindow]
        self.driver.switch_to.window(self.newWindow)
        
    def changeWindowBack(self):
        try:        self.driver.switch_to.window(self.baseWindow)
        except:
            print('Could not go back to Base Window... Wron use of changeWindowBack... Make sure u used changeWindow before')
            self.driver.switch_to.window(self.driver.window_handles[0])

    def sel_quit(self):
        time.sleep(1)
        try:                        self.driver.close()
        except Exception as err:    print(' WARNING: selenium could not close: {}'.format(err))
        try:                        self.driver.quit()
        except Exception as err:    print(' WARNING: selenium could not quit: {}'.format(err))

def selenium_clicLaunch(str_url, str_buttonxPath, str_buttonName):
    try:
        inst_sel = c_Selenium_InteractInternet(str_url)
        inst_sel.clic(str_buttonName, str_buttonxPath, [])
        inst_sel.sel_quit()
        return True
    except Exception as err:
        print(' ERROR in selenium_clicLaunch: {}'.format(err))
        print(' -  str_url: {}'.format(str_url))
        print(' -  str_buttonxPath: {}'.format(str_buttonxPath))
        print(' -  str_buttonName: {}'.format(str_buttonName))
        try:    inst_sel.sel_quit()
        except: pass
        return False
