import pytest
try:
    import nutEmail as Email
except:
    print('Online Test...')
    from pyNut import nutEmail as Email


#=============================================================================
# UNIT TEST
#=============================================================================

# OUTLOOK
def test_c_email_send():
    str_from = 'sgergh'
    str_to = 'aaa@yyy'
    str_cc = 'eee@rty'
    str_bcc = 'eurv@rtyrgheryh.com'
    str_subject = 'EMAIL subghrh'
    l_pathAttach = ['re',2, None]
    bl_draft = True
    dic_param = dict(str_to=str_to, str_cc=str_cc, str_bcc=str_bcc, str_subject=str_subject, l_pathAttach=l_pathAttach,
                     str_message='', str_from=str_from, bl_draft=bl_draft)
    o_mailParam = Email.c_email(**dic_param)
    o_mailParam.paramMail_Send()
    assert o_mailParam.SentOnBehalfOfName == str_from
    assert o_mailParam.To == str_to
    assert o_mailParam.Cc == str_cc
    assert o_mailParam.Bcc == str_bcc
    assert o_mailParam.Subject == str_subject
    assert o_mailParam.l_pathAttach == l_pathAttach
    assert o_mailParam.bl_draft == bl_draft

def test_c_otlk_builder_send_param():
    str_from = 'sgeryjkgh'
    str_to = 'aaa@yyy'
    str_cc = 'eee@rty'
    str_bcc = 'eurv@rtyrgheryh.com'
    str_subject = 'EMAIL subghrh'
    l_pathAttach = ['re', 2, None]
    bl_draft = True
    dic_param = dict(str_from=str_from, str_to=str_to, str_cc=str_cc, str_bcc=str_bcc, str_subject=str_subject, l_pathAttach=l_pathAttach,
                     str_message='', bl_draft=bl_draft)
    o_buil_emailSend = Email.c_Outlook_send(**dic_param)
    o_buil_emailSend.o_emailParam.paramMail_Send()
    assert o_buil_emailSend.o_emailParam.SentOnBehalfOfName == str_from
    assert o_buil_emailSend.o_emailParam.To == str_to
    assert o_buil_emailSend.o_emailParam.Cc == str_cc
    assert o_buil_emailSend.o_emailParam.Bcc == str_bcc
    assert o_buil_emailSend.o_emailParam.Subject == str_subject
    assert o_buil_emailSend.o_emailParam.l_pathAttach == l_pathAttach
    assert o_buil_emailSend.o_emailParam.bl_draft == bl_draft

@pytest.mark.parametrize("l_folders", [([]), (['']), (['Proj - Seita']), (['Side Activities', 'Foot'])])
def test_c_email_dwld(l_folders):
    str_outAcctName = 'sola@google.com'
    str_inbox = 'Inbox'
    dic_param = dict(str_outAcctName = str_outAcctName, str_inbox = str_inbox, l_folders = l_folders)
    o_mailParam = Email.c_email(**dic_param)
    o_mailParam.paramMail_Dwld()
    assert o_mailParam.str_outAcctName == str_outAcctName
    assert o_mailParam.str_inbox == str_inbox
    assert o_mailParam.l_folders == l_folders

@pytest.mark.parametrize("l_folders", [([]), (['']), (['Proj - Seita']), (['Side Activities', 'Foot'])])
def test_c_otlk_builder_dwld_param(l_folders):
    str_outAcctName = 'sola@google.com'
    str_inbox = 'Inbox'
    dic_param = dict(bl_test = True, str_outAcctName=str_outAcctName, str_inbox = str_inbox, l_folders = l_folders)
    o_buil_emailDwld = Email.c_Outlook_dwld(**dic_param)
    o_buil_emailDwld.o_emailParam.paramMail_Dwld()
    assert o_buil_emailDwld.o_emailParam.str_outAcctName == str_outAcctName
    assert o_buil_emailDwld.o_emailParam.str_inbox == str_inbox
    assert o_buil_emailDwld.o_emailParam.l_folders == l_folders

@pytest.mark.parametrize("l_folders", [([]), (['']), (['Proj - Seita']), (['Side Activities', 'Foot'])])
def test_c_otlk_builder_dwld(l_folders):
    str_outAcctName = ''
    str_inbox = 'Inbox'
    dic_param = dict(bl_test = True, str_outAcctName=str_outAcctName, str_inbox=str_inbox, l_folders=l_folders)
    o_buil_emailDwld =  Email.c_Outlook_dwld(**dic_param)
    o_otlk_Director =   Email.c_otlk_Director(o_buil_emailDwld)
    o_otlk_Director.Download_fMail()
    assert o_otlk_Director._builder.o_emailParam.str_outAcctName == str_outAcctName
    assert o_otlk_Director._builder.o_emailParam.str_inbox == str_inbox
    assert o_otlk_Director._builder.o_emailParam.l_folders == l_folders
    o_otlk_Director._builder.getEmails()
    int_nbEmails = len(o_otlk_Director._builder.o_emails)
    assert isinstance(int_nbEmails, int)

@pytest.mark.parametrize("str_subject, str_to, str_cc, str_File_startW, str_File_endW",
                         [('Subject that should fail', '', '', 'Piece jointe',''),
                          ('Subject that should fail:', 'laurent@google.com', '', '', ''),
                          ('Subject that should fail',  'laurent@google.com', '', '', ''),
                          ('Subject that should fail',  'lthjtj@rhgtr.com', '', '', ''),
                          ('Subject that should fail', '', 'lthjtj@rhgtr.com', '', ''),
                          ('', 'Dl-MK-StAff', 'FAKE CONTACT', '', ''),
                          ('', 'FAKE CONTACT', '', '', ''),
                          ('', '', '', 'PJ that does not exist', 'Not existiting.pdf'),
                          ('Shitty Subject that should fail',  '', 'anand@googl.com', '','')])
def test_FAIL_filterRestrict(str_subject, str_to, str_cc, str_File_startW, str_File_endW):
    str_outAcctName = ''
    str_inbox = 'Inbox'
    dic_param = dict(bl_test=True, str_outAcctName=str_outAcctName, str_inbox=str_inbox, str_subject=str_subject,
                     str_to=str_to, str_cc=str_cc, str_File_startW=str_File_startW, str_File_endW=str_File_endW)
    o_buil_emailDwld =  Email.c_Outlook_dwld(**dic_param)
    o_otlk_Director =   Email.c_otlk_Director(o_buil_emailDwld)
    with pytest.raises(Exception):
        o_otlk_Director.Download_fMail()


#------------------------------------------------------------------------------------------------------
# WEBMAIL
#------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("l_folders", [([]), (['']), (['Proj - Seita']), (['Side Activities', 'Foot'])])
def test_c_webmail_builder_dwld_param(l_folders):
    str_outAcctName = 'sola@google.com'
    str_inbox = 'Inbox'
    str_pwd = '***'
    dic_param = dict(bl_test = True, str_outAcctName=str_outAcctName, str_pwd = str_pwd, str_inbox = str_inbox, l_folders = l_folders)
    o_buil_emailDwld =  Email.c_Webmail_dwld(**dic_param)
    o_buil_emailDwld.o_emailParam.paramMail_Dwld()
    assert o_buil_emailDwld.o_emailParam.str_outAcctName == str_outAcctName
    assert o_buil_emailDwld.o_emailParam.str_pwd == str_pwd
    assert o_buil_emailDwld.o_emailParam.str_inbox == str_inbox
    assert o_buil_emailDwld.o_emailParam.l_folders == l_folders

@pytest.mark.parametrize("str_subject, str_to, str_cc, str_File_startW, str_File_endW",
                         [('Subject that should fail', '', '', 'Piece jointe',''),
                          ('Subject that should fail:',  'laurent@google.com', '', '', ''),
                          ('Subject that should fail',  'lthjtj@rhgtr.com', '', '', ''),
                          ('Subject that should fail', '', 'lthjtj@rhgtr.com', '', ''),
                          ('Subject that should fail',  '', 'anand@goo.com', '','')])
def test_FAIL_webmail_filterRestrict(str_subject, str_to, str_cc, str_File_startW, str_File_endW):
    str_outAcctName = 'sola@ihsmarkit.com'
    str_inbox = 'Inbox'
    str_pwd = 'D3lt@0n3'
    l_folders = ['PCF-Received']
    dic_param = dict(bl_test=True, str_outAcctName=str_outAcctName, str_pwd = str_pwd, str_inbox=str_inbox, str_subject=str_subject,
                     str_to=str_to, str_cc=str_cc, str_File_startW=str_File_startW, str_File_endW=str_File_endW, l_folders=l_folders)
    o_buil_emailDwld =  Email.c_Webmail_dwld(**dic_param)
    o_otlk_Director =   Email.c_otlk_Director(o_buil_emailDwld)
    with pytest.raises(Exception):
        o_otlk_Director.Download_fMail()





