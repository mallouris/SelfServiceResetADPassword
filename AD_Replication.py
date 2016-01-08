# -*- coding: cp1253 -*-
#!/usr/bin/env python

import pyad.adquery
import pyad.pyad
import pyad.aduser
import time
import shelve
import AD_User_Pass_Reset


if __name__== '__main__':   
    print 'Starting Up Active Directory replication to a local shelve....'
    print 'Please wait, upon the size of tha AD it might take a few minutes to complete the replication...'
    starttime=time.time()   
    AD_User_Pass_Reset.ReplicateAD()
    elapsedtime=time.time()-starttime
    print '\nTotal time to complete script ' +str(elapsedtime) + ' seconds.'  
    print 'done replication.'



