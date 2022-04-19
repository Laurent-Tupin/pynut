try:
    from . import _lib as lib
    from . import nutFiles as fl
    from . import nutDate as dat
    from . import nutOther as oth
except:
    import _lib as lib
    import nutFiles as fl
    import nutDate as dat
    import nutOther as oth
os  = lib.os()
math =lib.math()
pd  = lib.pandas()
np  = lib.numpy()
win32       = lib.win32()
pythoncom   = lib.pythoncom()
Credentials = lib.Credentials()
Account     = lib.Account()
DELEGATE    = lib.DELEGATE()
EWSTimeZone = lib.EWSTimeZone()
EWSDateTime = lib.EWSDateTime()
Configuration = lib.Configuration()
FileAttachment = lib.FileAttachment()




#=============================================================================
# DESIGN PATTERN: BUILDER for OUTLOOK / EXCHANGELIB
#=============================================================================
class c_email:
    """Product: Define the Email Param here"""
    def __init__(self, **dic_param):
        self.dic_param = dic_param
        if 'bl_test' in dic_param:  self.bl_test = dic_param['bl_test']
        else:                       self.bl_test = False
    # GET the Param
    def __str__(self):
        # str_return = ''
        # for k, v in self.dic_param.items():
        #     str_return = '\r  -{}: {}'.format(str(k), str(v))
        return str(self.dic_param)
    def paramMail_Send(self, o_mail = None):
        dic_p = self.dic_param
        try:
            # Param to be used in the Concrete Builder (just save the param...)
            if 'bl_draft' in dic_p:         self.bl_draft = dic_p['bl_draft']
            else:                           self.bl_draft = True
            if 'l_pathAttach' in dic_p:     self.l_pathAttach = dic_p['l_pathAttach']
            else:                           self.l_pathAttach = None
            if 'str_from' in dic_p:         self.SentOnBehalfOfName =   dic_p['str_from']
            if 'str_to' in dic_p:           self.To =       dic_p['str_to']
            if 'str_cc' in dic_p:           self.Cc =       dic_p['str_cc']
            if 'str_subject' in dic_p:      self.Subject =  dic_p['str_subject']
            if 'str_bcc' in dic_p:          self.Bcc =      dic_p['str_bcc']
            if 'str_message' in dic_p:      self.Body =     dic_p['str_message']
            # Change the email object itself and return it 
            if not o_mail is None:
                if 'str_from' in dic_p:     o_mail.SentOnBehalfOfName = dic_p['str_from']
                if 'str_to' in dic_p:       o_mail.To =     dic_p['str_to']
                if 'str_cc' in dic_p:       o_mail.Cc =     dic_p['str_cc']
                if 'str_subject' in dic_p:  o_mail.Subject =dic_p['str_subject']
                if 'str_bcc' in dic_p:      o_mail.Bcc =    dic_p['str_bcc']
                if 'str_message' in dic_p:  o_mail.Body =   dic_p['str_message']
        except Exception as err:
            print(' ERROR in c_email paramMail_Send: Cannot define the Params')
            print(' - ', str(err))
            raise
        return o_mail
    def paramMail_Dwld(self):
        dic_p = self.dic_param
        try:
            if 'str_outAcctName' in dic_p:  self.str_outAcctName = dic_p['str_outAcctName']
            else:                           self.str_outAcctName = ''
            if 'str_pwd' in dic_p:          self.str_pwd = dic_p['str_pwd']
            else:                           self.str_pwd = ''
            if 'str_inbox' in dic_p:        self.str_inbox = dic_p['str_inbox']
            else:                           self.str_inbox = ''
            if 'l_folders' in dic_p:        self.l_folders = dic_p['l_folders']
            else:                           self.l_folders = []
            if 'str_subject' in dic_p:      self.str_subject = dic_p['str_subject']
            else:                           self.str_subject = ''
            if 'str_emailTime' in dic_p:    self.str_emailTime = dic_p['str_emailTime']
            else:                           self.str_emailTime = ''
            if 'dte_date' in dic_p:         self.dte_date = dic_p['dte_date']
            else:                           self.dte_date = ''
            if 'str_to' in dic_p:           self.str_to = dic_p['str_to']
            else:                           self.str_to = ''
            if 'str_cc' in dic_p:           self.str_cc = dic_p['str_cc']
            else:                           self.str_cc = ''
            if 'str_File_startW' in dic_p:  self.str_File_startW = dic_p['str_File_startW']
            else:                           self.str_File_startW = ''
            if 'str_File_endW' in dic_p:    self.str_File_endW = dic_p['str_File_endW']
            else:                           self.str_File_endW = ''
            if 'str_folder' in dic_p:       self.str_folder = dic_p['str_folder']
            else:                           self.str_folder = ''
            if 'l_folder_dest' in dic_p:    self.l_folder_dest = dic_p['l_folder_dest']
            else:                           self.l_folder_dest = ''
        except Exception as err:
            print(' ERROR in c_email paramMail_Dwld: Cannot define the Params')
            print(' - ', str(err))
            raise
        return 1
#_______________________________________            


class c_otlk_Director():
    def __init__(self, builder):
        self._builder = builder 
    def SendMail(self):
        self._builder.Define_App()
        self._builder.Define_Email()
        self._builder.Attach_files()
        self._builder.Send_eMail()
    def Download_fMail(self):
        self._builder.Define_App()
        self._builder.Define_Email()
        self._builder.Dwld_docFromEmail()
    def Move_Email(self):
        self._builder.Define_App()
        self._builder.Define_Email()
        self._builder.MoveEmail()
#_______________________________________        


class c_Outlook():
    """Abstract Builder: Build the outlook object here"""
    def __init__(self, str_nameSpace = 'MAPI'):
        self.o_outlook =        None
        self.o_emails =         None
        self.o_latestMail =     None
        self.str_nameSpace =    str_nameSpace
    def Define_App(self):
        if self.o_outlook is None:
            pythoncom.CoInitialize()
            if self.str_nameSpace == '':
                self.o_outlook = win32.Dispatch('Outlook.Application')
            else:
                self.o_outlook = win32.Dispatch('Outlook.Application').GetNamespace(self.str_nameSpace)
        return self.o_outlook
    def getAccount(self, str_outAcctName = ''):
        # Default value: User email Address
        if str_outAcctName == '':
            str_outAcctName = fl.fStr_GetUserEmail('@ihsmarkit.com')
        self.str_outAcctName = str_outAcctName
        # Define the Mailbox Sola (first Folder)
        try:    
            o_Acct = self.o_outlook.Folders(self.str_outAcctName)
        except:
            str_ErrorMsg = ' ERROR in getAccount | Cannot find the Outlook Account \n'
            str_ErrorMsg += '  - Folder wanted: {} \n'.format(str_outAcctName)
            str_ErrorMsg += '  - Folder Available on this machine : \n'
            # Loop on all account user has
            for __fol in self.o_outlook.Folders:
                __fol = str(__fol)
                str_ErrorMsg += '    - {}  \n'.format(__fol)
                l_condition = [__fol.lower() == str_outAcctName.lower()]
                if [x for x in l_condition if x == True] != []:
                    self.str_outAcctName = __fol
                    break
            # Loop on all account user has
            try:    o_Acct = self.o_outlook.Folders(self.str_outAcctName)
            except Exception as err:
                print(str_ErrorMsg, '\r - ', str(err))
                raise
        self.o_Acct = o_Acct
        return o_Acct
    def getInbox(self, str_inbox = ''):
        # Default value: User email Address
        if str_inbox == '':
            str_inbox = 'Inbox'
        self.str_inbox = str_inbox
        # Define the Inbox (2nd Folder)
        try:
            o_inbox = self.o_Acct.Folders[str_inbox]
        except Exception as err:
            print(' ERROR in getInbox: Cannot find the Box: |{}|'.format(self.str_inbox))
            print(' - ', str(err))
            raise
        self.o_inbox = o_inbox
        return o_inbox
    def getFolders(self, l_folders = []):
        self.l_folders = l_folders
        try:
            o_folder = self.o_inbox
            for _fol in l_folders:
                if not _fol == '':
                    o_folder = o_folder.Folders[_fol]
        except Exception as err:
            print(' ERROR in getFolders: Cannot find the Folder: ')
            print(' - |{}|', '|'.join(l_folders))
            print(' - ', str(err))
            raise
        self.o_folder = o_folder
        return o_folder  
    #---------------------------------
    # Archive Email: PB, depends on Define_Email in (c_Outlook_dwld)
    #---------------------------------
    def MoveEmail(self):
        # Define the folder where to move the email...
        l_folder_dest = self.o_emailParam.l_folder_dest
        if l_folder_dest == []:
            return 'No Folder to move to...'
        o_folder_dest = self.getFolders_destination(l_folder_dest)
        # Move
        try:    
            self.o_latestMail.Move(o_folder_dest)
        except Exception as err:
            print(' ERROR in MoveEmail || {}'.format(str(err)))
            raise
    def getFolders_destination(self, l_folder_dest = []):
        self.l_folder_dest = l_folder_dest
        try:
            o_folder_dest = self.o_inbox
            for _fol in l_folder_dest:
                if not _fol == '':
                    o_folder_dest = o_folder_dest.Folders[_fol]
        except Exception as err:
            print(' ERROR in getFolders_destination: Cannot find the Folder: ')
            print(' - |{}|', '|'.join(l_folder_dest))
            print(' - ', str(err))
            raise
        self.o_folder_dest = o_folder_dest
        return o_folder_dest  
    #---------------------------------
    # Just for info (method should not be used for quick operation on large Email)
    #---------------------------------
    def getEmails(self):
        self.o_emails = self.o_folder.Items
    def getLastEmails(self):
        o_emails = self.o_emails.Sort("[ReceivedTime]", True)
        self.o_emails = o_emails[:50]
#_______________________________________
    

class c_Outlook_dwld(c_Outlook):
    """Concrete Builder --> provides methods to Download Docs from Emails """
    def __init__(self, **dic_param):
        self.str_nameSpace = 'MAPI'
        super(c_Outlook_dwld, self).__init__(str_nameSpace = self.str_nameSpace)
        self.o_emailParam = c_email(**dic_param)
        
    def Define_Email(self):
        self.o_emailParam.paramMail_Dwld()
        self.getAccount(self.o_emailParam.str_outAcctName)      # GET account (name@mail.com)
        self.getInbox(self.o_emailParam.str_inbox)              # GET Inbox
        self.getFolders(self.o_emailParam.l_folders)            # GET Folders
        self.getEmails_Restict()
        self.filterEmails_ToCc()
        self.filterEmails_attachName()
        self.getTheLastEmail()
        
    def Dwld_docFromEmail(self):
        # Will Allow Unit Test to stop before downloading
        if self.o_emailParam.bl_test is True:
            return True
        self.download_PJ()
        return self.bl_success
                
    def getEmails_Restict(self):
        try:
            o_folder = self.o_folder
            # Get the Param
            str_subject = self.o_emailParam.str_subject
            str_emailTime = self.o_emailParam.str_emailTime
            # No Subject Filter
            if str_subject == '':
                o_emails = o_folder.Items
            else:
                str_sql = "@SQL=(urn:schemas:httpmail:subject LIKE '%{}%')".format(str_subject)
                o_emails = o_folder.Items.Restrict(str_sql)
                if len(o_emails) == 0:
                    print('   WARNING (out): We could not find the email with the subject |{}|'.format(str_subject))
                    raise
            #---------------------------------
            # Time of the EMAIL - str_emailTime
            if not str_emailTime == '':
                d_emailTime =   eval(str_emailTime)
                str_date =      self.o_emailParam.dte_date
                str_start_time, str_end_time  = fStr_GetDtTimeBracket(str_date, d_emailTime['start'], d_emailTime['end'])                
                str_bracket =   "[ReceivedTime] >= '{}' And [ReceivedTime] <= '{}'".format(str_start_time, str_end_time)
                o_emails_time = o_emails.Restrict(str_bracket)
                if len(o_emails_time) == 0:
                    print('   WARNING: We could not find the email with the email Time |{}|'.format(str_emailTime))
                    print('     ... Subject is : |{}|'.format(str_subject))
                    print('     ... Bracket is : |{}|'.format(str_bracket)) 
                else:
                    o_emails = o_emails_time
                    print('   *|* INFO: you have filled the Param |outlook_emailTime|, which means you will restrict the email by time')
                    print('     ... str_bracket is : |{}|'.format(str_bracket))  
            #---------------------------------
        except Exception as err:
            print(' ERROR in getEmails_Restict: |{}|'.format(err))
            print(' - Email Param: ', self.o_emailParam)
            raise
        self.o_emails = o_emails
        
    def filterEmails_ToCc(self):
        try:
            o_emails = self.o_emails
            # TO
            str_to = self.o_emailParam.str_to
            if not str_to == '':
                # TODO: Meetings can make the test fails (no To in othe object than email)                
                o_emails_sub = [o_mail for o_mail in o_emails if str_to.lower() in o_mail.To.lower()]
                if len(o_emails_sub) == 0:
                    print(' ... Empty on filterEmails_ToCc with To: {} || Subject: {}'.format(str_to, self.o_emailParam.str_subject))
                    # Does not raise error in case he dont find with the To: Tolerance to that (except if no subject)
                    if self.o_emailParam.str_subject == '':
                        raise                    
                else:   o_emails = o_emails_sub
            # Cc
            str_cc = self.o_emailParam.str_cc
            if not str_cc == '':
                o_emails_sub = [o_mail for o_mail in o_emails if str_cc.lower() in o_mail.Cc.lower()]
                if len(o_emails_sub) == 0:
                    print(' ... Empty on filterEmails_ToCc with CC: {} || Subject: {}'.format(str_cc, self.o_emailParam.str_subject))
                    # Does not raise error in case he dont find with the Cc: Tolerance to that
                    if self.o_emailParam.str_subject == '':
                        raise  
                else:   o_emails = o_emails_sub
        except Exception as err:
            print(' ERROR in filterEmails: |{}|'.format(err))
            print(' - Email Param: ', self.o_emailParam)
            raise
        self.o_emails = o_emails
        
    def filterEmails_attachName(self):
        try:
            o_emails = self.o_emails
            str_File_startW = self.o_emailParam.str_File_startW
            # PJ name start
            if not str_File_startW == '':
                o_emails_sub = [o_mail for o_mail in o_emails if str_File_startW.lower() in 
                                [str(o_attach).lower()[:len(str_File_startW)] for o_attach in o_mail.Attachments]]
                if len(o_emails_sub) == 0:
                    print(' ... Empty maill list, str_File_startW: |{}|, Subject: |{}|'.format(str_File_startW, self.o_emailParam.str_subject))
                    for o_mail in o_emails[:5]:
                        print([str(o_attach) for o_attach in o_mail.Attachments])
                    raise
                else:   o_emails = o_emails_sub
            # PJ name end       
            str_File_endW = self.o_emailParam.str_File_endW
            if not str_File_endW == '':
                o_emails_sub = [o_mail for o_mail in o_emails if str_File_endW.lower() in 
                                [str(o_attach).lower()[-len(str_File_endW):] for o_attach in o_mail.Attachments]]
                if len(o_emails_sub) == 0:
                    print(' ... Empty maill list, str_File_endW: |{}|, Subject: |{}|'.format(str_File_endW, self.o_emailParam.str_subject))
                    raise
                else:   o_emails = o_emails_sub      
        except Exception as err:
            print(' ERROR in filterEmails_attachName: |{}|'.format(err))
            print(' - Email Param: ', self.o_emailParam)
            raise
        self.o_emails = o_emails
        
    def getTheLastEmail(self):
        o_emails = self.o_emails
        try:
            i_indexMail = int(np.argmax([_mail.Senton for _mail in o_emails]))
            o_latestMail = o_emails[i_indexMail]
        except Exception as err:
            print(' ERROR in getTheLastEmail: |{}|'.format(err))
            raise
        self.o_latestMail = o_latestMail
        
    def download_PJ(self):
        o_mail = self.o_latestMail
        str_File_startW = self.o_emailParam.str_File_startW
        str_File_endW = self.o_emailParam.str_File_endW
        str_folder = self.o_emailParam.str_folder
        bl_success = False
        try:
            for o_attach in o_mail.Attachments:
                str_attachName = str(o_attach).lower()
                if not str_File_startW == '':
                    if not str_File_startW.lower() == str_attachName[:len(str_File_startW)]:
                        continue # Ignore the file
                if not str_File_endW == '':
                    if not str_File_endW.lower() == str_attachName[-len(str_File_endW):]:
                        continue # Ignore the file
                o_attach.SaveAsFile(os.path.join(str_folder, str(o_attach)))
                bl_success = True
        except Exception as err:
            print(' ERROR in download_PJ: |{}|'.format(err))
            print(' - Folder: ', str_folder)
            print(' - Mail Subject: ', self.self.o_emailParam.str_subject)
            print(' - fileName: ', str_File_startW, str_File_endW)
            print(' - Email Param: ', self.o_emailParam)
            raise
        self.bl_success = bl_success
#_____________________________________________________________________
    
class c_Outlook_send(c_Outlook):
    """Concrete Builder --> provides methods to Send the Emails """
    def __init__(self, **dic_param):
        self.str_nameSpace = ''
        super(c_Outlook_send, self).__init__(str_nameSpace = self.str_nameSpace)
        self.o_emailParam = c_email(**dic_param)
        
    def Define_Email(self):
        try:
            o_mail = self.o_outlook.CreateItem(0)
            o_mail = self.o_emailParam.paramMail_Send(o_mail)
        except Exception as err:
            print(' ERROR in Define_Email (Send): |{}|'.format(err))
            print(' - Email Param: ', self.o_emailParam, '\n')
            raise
        self.o_mail = o_mail
        
    def Attach_files(self):
        self.bl_success = True
        try:
            l_pathAttach =  self.o_emailParam.l_pathAttach
            if not l_pathAttach is None:
                for attach in l_pathAttach:
                    if fl.fBl_FileExist(attach):
                        self.o_mail.Attachments.Add(attach)
                    else:
                        self.bl_success = False
                        print('{} WARNING in Attach_files'.format('\n'))
                        print(' ==> The file that could not be JOINED to the email is: |{}| \n\n'.format(str(attach)))
                        # We do not raise error as it will be only warning !!!
        except Exception as err:
            print(' ERROR in Attach_files: |{}|'.format(err))
            print(' - Email Param: ', self.o_emailParam, '\n')
            #raise
        return self.bl_success
    
    def Send_eMail(self):
        try:
            if self.o_emailParam.bl_draft is False:
                self.o_mail.Send()
            else:
                self.o_mail.Display(True)
        except Exception as err:
            print(' ERROR in Send_eMail: |{}|'.format(err))
            print(' - Email Param: ', self.o_emailParam, '\n')
            raise
        return self.bl_success
#_____________________________________________________________________


class c_Webmail():
    """Abstract Builder: Build the Webmail object here"""
    def __init__(self):
        self.o_Acct =   None
        self.o_inbox = None
        self.o_folder = None
        self.o_emails = None
        self.o_latestMail = None
        
    def Define_App(self):
        # We need the information included in c_email so we need to wait for Concrete Class to be launch
        pass
        
    def getAccount(self, str_outAcctName = '', str_pwd = ''): 
        # Default value: User email Address
        if str_outAcctName == '':
            str_outAcctName =   fl.fStr_GetUserEmail('@ihsmarkit.com')
        self.str_outAcctName =  str_outAcctName
        # Quick variables
        self.str_emailEnd =     str_outAcctName.split('@')[-1]
        str_username =          str_outAcctName
        # Define the Credentials
        o_cred = Credentials(username = str_username, password = str_pwd)
        # Define the Account
        try:
            o_Acct = Account(credentials = o_cred, primary_smtp_address = str_outAcctName, 
                             autodiscover = True, access_type = DELEGATE)
        except Exception as err:
            # print('\n INFO, we got an error (getAccount): |{}|'.format(err))
            print('\n INFO, we got an error (getAccount)')
            o_Acct = self.getAccount_wConfig(o_cred)
        self.o_Acct = o_Acct
        return self.o_Acct
        
    def getAccount_wConfig(self, o_cred):
        str_server = 'http://eumail.{}'.format(self.str_emailEnd)
        print('  *** Account did not directly, we need to define the server: |{}| in a config obj'.format(str_server))
        try:
            o_config = Configuration(credentials = o_cred, server = str_server)
            o_Acct = Account(config = o_config, primary_smtp_address = self.str_outAcctName, access_type = DELEGATE)
        except:
            print('  **** We need auth_type = NTLM')
            o_config_NTLM = Configuration(credentials = o_cred, service_endpoint = str_server, auth_type = 'NTLM')
            o_Acct = Account(config = o_config_NTLM, primary_smtp_address = self.str_outAcctName, access_type = DELEGATE)
        self.o_Acct = o_Acct
        return self.o_Acct
    
    def getInbox(self, str_inbox = ''):
        # Default value: User email Address
        if str_inbox == '':
            str_inbox = 'Inbox'
        self.str_inbox = str_inbox
        # Define the Inbox
        try:
            if str_inbox.lower() == 'inbox':
                o_inbox = self.o_Acct.inbox
            else:
                print(' ERROR in getInbox: You are not in INBOX ??!!??')
        except Exception as err:
            print(' ERROR in getInbox: Cannot find the Box: |{}|'.format(self.str_inbox))
            print(' - ', str(err))
            raise
        self.o_inbox = o_inbox
        return o_inbox
        
    def getFolders(self, l_folders = []):
        self.l_folders = l_folders
        try:
            o_folder = self.o_inbox
            for _fol in l_folders:
                if not _fol == '':
                    o_folder = o_folder / _fol
        except Exception as err:
            print(' ERROR in getFolders: Cannot find the Folder: ')
            print(' - |{}|', '|'.join(l_folders))
            print(' - ', str(err))
            raise
        self.o_folder = o_folder
        return o_folder  
    
    #---------------------------------
    # Just for info (method should not be used for quick operation on large Email)
    #---------------------------------
    def getEmails(self):
        self.o_emails = self.o_folder.all()
    def getLastEmails(self, int_nbEmails = 50):
        o_emails = self.o_emails.order_by('-datetime_received')[:int_nbEmails]
        self.o_emails = o_emails
#_______________________________________

class c_Webmail_dwld(c_Webmail):
    """Concrete Builder --> provides methods to Download Docs from Emails """
    def __init__(self, **dic_param):
        super(c_Webmail, self).__init__()
        self.o_emailParam = c_email(**dic_param)
        
    def Define_Email(self):
        self.o_emailParam.paramMail_Dwld()
        self.getAccount(self.o_emailParam.str_outAcctName, self.o_emailParam.str_pwd)
        self.getInbox(self.o_emailParam.str_inbox)              # GET Inbox
        self.getFolders(self.o_emailParam.l_folders)            # GET Folders
        self.getEmails_Restict()
        self.filterEmails_ToCc()
        self.filterEmails_attachName()
        self.getTheLastEmail()
        
    def Dwld_docFromEmail(self):
        # Will Allow Unit Test to stop before downloading
        if self.o_emailParam.bl_test is True:
            return True
        self.download_PJ()
        return self.bl_success
                
    def getEmails_Restict(self):
        try:
            o_folder = self.o_folder
            # Get the Param
            str_subject = self.o_emailParam.str_subject
            str_emailTime = self.o_emailParam.str_emailTime
            d_paramFilter = {}
            # Build the conditions
            if not str_subject == '': 
                d_paramFilter['subject__icontains'] = str_subject
            if not str_emailTime == '':
                try:
                    d_emailTime = eval(str_emailTime)
                    str_date = self.o_emailParam.dte_date
                    dt_start_time, dt_end_time = fStr_GetDtTimeBracket(str_date, d_emailTime['start'], d_emailTime['end'], bl_dateReturn = True)
                    tz = EWSTimeZone.localzone()
                    tz_start =  EWSDateTime.from_datetime(dt_start_time).astimezone(tz)
                    tz_end =    EWSDateTime.from_datetime(dt_end_time).astimezone(tz)
                    d_paramFilter['datetime_received__range'] = (tz_start, tz_end)
                except Exception as err:
                    print('  ERROR in getEmails_Restict with Time: |{}|'.format(err))
                    print('    - str_emailTime: ', str_emailTime)
                    print('    - Bracket: ', tz_start, tz_end)
            # Filtering
            if any(d_paramFilter):          # IF NOT EMPTY
                o_emails = o_folder.filter(**d_paramFilter)
            else:
                self.getEmails()
                o_emails = self.o_emails
            # ERROR in case its empty
            if len(list(o_emails)) == 0:
                if str_emailTime != '':
                    print(' WARNING: We could not find the email with the EMAIL time |{}|'.format(str_emailTime))
                    print('   ... with the subject |{}|'.format(str_subject))
                    print('   ... Bracket: ', tz_start, tz_end)
                    # TODO: Look if you launch back up again the search with just SUBJECT like with OUTLOOK
                elif str_subject != '': 
                    print(' WARNING (exclib): We could not find the email with the subject |{}|'.format(str_subject))
                raise
        except Exception as err:
            print(' ERROR in getEmails_Restict: |{}|'.format(err))
            print(' - str_subject: ', str_subject)
            print(' - str_emailTime: ', str_emailTime)
            try:    print(' - Bracket: ', tz_start, tz_end)
            except: pass
            # print(' - Email Param: ', self.o_emailParam)
            raise
        self.o_emails = o_emails
        
    def filterEmails_ToCc(self):
        try:
            o_emails = self.o_emails
            # TO
            str_to = self.o_emailParam.str_to
            if not str_to == '':
                o_emails_sub = [o_mail for o_mail in o_emails if str_to.lower() in o_mail.display_to.lower()]
                if len(o_emails_sub) == 0:
                    print(' ... Empty on filterEmails_ToCc with To: {} || Subject: {}'.format(str_to, self.o_emailParam.str_subject))
                    # Does not raise error in case he dont find with the To: Tolerance to that (except if no subject)
                    if self.o_emailParam.str_subject == '':
                        raise                    
                else:   o_emails = o_emails_sub
            # Cc
            str_cc = self.o_emailParam.str_cc
            if not str_cc == '':
                o_emails_sub = [o_mail for o_mail in o_emails if str_cc.lower() in o_mail.display_cc.lower()]
                if len(o_emails_sub) == 0:
                    print(' ... Empty on filterEmails_ToCc with CC: {} || Subject: {}'.format(str_cc, self.o_emailParam.str_subject))
                    # Does not raise error in case he dont find with the Cc: Tolerance to that
                    if self.o_emailParam.str_subject == '':
                        raise  
                else:   o_emails = o_emails_sub
        except Exception as err:
            print(' ERROR in filterEmails: |{}|'.format(err))
            print(' - Email Param: ', self.o_emailParam)
            raise
        self.o_emails = o_emails
        
    def filterEmails_attachName(self):
        try:
            o_emails = self.o_emails
            str_File_startW = self.o_emailParam.str_File_startW
            # PJ name start
            if not str_File_startW == '':
                o_emails_sub = [o_mail for o_mail in o_emails if str_File_startW.lower() in 
                                [str(o_attach.name).lower()[:len(str_File_startW)] for o_attach in o_mail.attachments]]
                if len(o_emails_sub) == 0:
                    print(' ... Empty mail list, str_File_startW: |{}|, Subject: |{}|'.format(str_File_startW, self.o_emailParam.str_subject))
                    self.getTheLastEmail()
                    self.print_EmailInfo(self.o_latestMail)
                    raise
                else:   o_emails = o_emails_sub
            # PJ name end       
            str_File_endW = self.o_emailParam.str_File_endW
            if not str_File_endW == '':
                o_emails_sub = [o_mail for o_mail in o_emails if str_File_endW.lower() in 
                                [str(o_attach.name).lower()[-len(str_File_endW):] for o_attach in o_mail.attachments]]
                if len(o_emails_sub) == 0:
                    print(' ... Empty mail list, str_File_endW: |{}|, Subject: |{}|'.format(str_File_endW, self.o_emailParam.str_subject))
                    self.getTheLastEmail()
                    self.print_EmailInfo(self.o_latestMail)
                    raise
                else:   o_emails = o_emails_sub      
        except Exception as err:
            print(' ERROR in filterEmails_attachName: |{}|'.format(err))
            print(' - Email Param: ', self.o_emailParam)
            raise
        self.o_emails = o_emails
        
    def getTheLastEmail(self):
        o_emails = self.o_emails
        try:
            # o_emails can be a list or an object if no other filter has been applied
            if isinstance(o_emails, list):
                i_indexMail = int(np.argmax([_mail.datetime_sent for _mail in o_emails]))
                o_latestMail = o_emails[i_indexMail]
            else:
                o_latestMail = o_emails.order_by('-datetime_received')[0]
        except Exception as err:
            print(' ERROR in getTheLastEmail: |{}|'.format(err))
            raise
        self.o_latestMail = o_latestMail
        
    def print_EmailInfo(self, o_mail):
        print('   ** Last EMail: ')
        print('     - From ', o_mail.sender)
        print('     - To', o_mail.display_to)
        print('     - Cc', o_mail.display_cc)
        print('     - Date', o_mail.datetime_received)
        print('     - List of Attachements (last EMail): ', [str(o_attach.name) for o_attach in o_mail.attachments])
        
    def download_PJ(self):
        o_mail = self.o_latestMail
        str_File_startW = self.o_emailParam.str_File_startW
        str_File_endW = self.o_emailParam.str_File_endW
        str_folder = self.o_emailParam.str_folder
        bl_success = False
        try:
            for o_attach in o_mail.attachments:
                str_attachName = str(o_attach.name)
                if isinstance(o_attach, FileAttachment):
                    if not str_File_startW == '':
                        if not str_File_startW.lower() == str_attachName[:len(str_File_startW)].lower():
                            continue # Ignore the file
                    if not str_File_endW == '':
                        if not str_File_endW.lower() == str_attachName[-len(str_File_endW):].lower():
                            continue # Ignore the file
                    with open(os.path.join(str_folder, str_attachName), 'wb') as f:
                        f.write(o_attach.content)
                    bl_success = True
                else:
                    print(' WARNING in download_PJ, file is not an attachment: |{}|'.format(str_attachName))
        except Exception as err:
            print(' ERROR in download_PJ: |{}|'.format(err))
            print(' - Folder: ', str_folder)
            print(' - Mail Subject: ', self.self.o_emailParam.str_subject)
            print(' - fileName: ', str_File_startW, str_File_endW)
            print(' - Email Param: ', self.o_emailParam)
            raise
        self.bl_success = bl_success
#_____________________________________________________________________


# END DESIGN PATTERN
#=============================================================================            





#---------------------------------------------------------------
#------ Launch an email to send ------------------
#---------------------------------------------------------------  
def fBl_SendMail_desPatt(**dic_param):
    o_builder_emailSend =   c_Outlook_send(**dic_param)
    o_otlk_Director =       c_otlk_Director(o_builder_emailSend)
    o_otlk_Director.SendMail()
    bl_success = o_otlk_Director._builder.bl_success
    return bl_success


#---------------------------------------------------------------
# ------ Additional Function ------------------
#---------------------------------------------------------------  
def fStr_GetDtTimeBracket(str_date, int_start = 0, int_end = 0, str_datFormat = '%Y-%m-%d %H:%M %p', bl_dateReturn = False):
    dt_start_time = dat.fDte_formatToDate(str_date, str_dateFormat = '%Y-%m-%d', bl_stopLoop = True)
    dt_end_time = dt_start_time
    dt_start_time = dat.fDte_AddHour(dt_start_time, int_start)
    dt_end_time = dat.fDte_AddHour(dt_end_time, int_end)
    if bl_dateReturn:
        return dt_start_time, dt_end_time
    else:
        str_start_time = dt_start_time.strftime(str_datFormat)
        str_end_time = dt_end_time.strftime(str_datFormat)
    return str_start_time, str_end_time







