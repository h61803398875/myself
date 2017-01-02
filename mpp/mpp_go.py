# -*- encoding:utf8 -*-

import win32com.client

doc = 'C:/hey_girl.mpp'
try:
    mpp = win32com.client.Dispatch("MSProject.Application")
    mpp.Visible = 1

    try:

        mpp.FileOpen(doc)
        proj = mpp.ActiveProject
        print proj.BuiltinDocumentProperties(11), ",", proj.BuiltinDocumentProperties(12)

    except Exception, e:
        print "Error", e

    mpp.FileSave()
    mpp.Quit()

except Exception, e:
    print "Error opening file", e
