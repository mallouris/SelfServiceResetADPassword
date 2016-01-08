# -*- coding: cp1253 -*-
#!/usr/bin/env python
# Dependencies pyad, httplib2  and pywin32 modules
# Created by Stephanos Mallouris 7-Sept-2015
# will only run on windows machine. It is not cross-platform

import pyad.adquery
import pyad.pyad
import pyad.aduser
import time
import os
import string
import httplib2
import shelve



def CYTA_Web_SMS(mobilenumber):
    XmlValidSmsMessage = 'Use the following word to validate your self and reset your password:\n' + str(gen_random_password(length=10))
    PostData = '<?xml version="1.0" encoding="UTF-8" ?> ' \
               "<websmsapi>" \
               " <version>1.0</version>" \
               " <username>fill in username</username>" \
               " <secretkey>fill in secret key</secretkey>" \
               " <recipients>" \
               " <count>1</count>" \
               " <mobiles>" \
               " <m>" + str(mobilenumber) + "</m>" \
               " </mobiles>"  \
               " </recipients>" \
               " <message>" + XmlValidSmsMessage + "</message>" \
               " <language>en</language>" \
               "</websmsapi>"
    print PostData

    url='https://www.cyta.com.cy/cytamobilevodafone/dev/websmsapi/sendsms.aspx'
    #print 'Full message length' +str(len(PostData))
    
    myheader = { "Content-Type" : "application/xml; charset=utf-8", 'content-length':str(len(PostData)) }
    httpconnect = httplib2.Http()
    responce, content = httpconnect.request(url,'POST', headers=myheader, body=PostData)
    print '\n'
    print PostData
    print '\n'
    
    print 'Server Responce:' + str(responce)
    print '\nContent:' + str(content)    




def ReplicateAD():
    pyad.pyad.set_defaults(ldap_server='', ldap_port=389, \
                           username='', password='') ## it is necessary to provide the necessary credentials
                                                                 ## to connect to AD, and have permissions to reset passwords

    q = pyad.adquery.ADQuery()
    q.execute_query(
            attributes = ["distinguishedName", "displayName","type","mailNickname","mail","mobile","extensionAttribute1","employeeNumber"],
            where_clause = "objectClass = 'user'",
            base_dn = "DC=, DC=, DC=" #
            )

    Ad_Results=q.get_results()
    Ad_data_in_shelve=shelve.open('AD_Replica.dat', writeback=True)
    Ad_dictionary={}
        
    for row in Ad_Results:
       Ad_dictionary[str(row['mail'])]=[row['distinguishedName'],row['displayName'],row['mobile'],row['extensionAttribute1'],row['employeeNumber']]
       

    Ad_data_in_shelve['Ad']=Ad_dictionary
    Ad_data_in_shelve.close()



def verifyADuser(useremail, ID, mobile):
    
    pyad.pyad.set_defaults(ldap_server='', ldap_port=389, \
                           username='', password='') ## it is necessary to provide the necessary credentials
                                                                 ## to connect to AD, and have permissions to reset passwords
    usermailnick=string.split(useremail,'@',1)
    print usermailnick[0]
    
    Ad_dictionary={}
    Ad_data_in_shelve=shelve.open('AD_Replica.dat', writeback=False)
    Ad_Dictionary=Ad_data_in_shelve['Ad']
    Ad_data_in_shelve.close()

    

    user_located=True
    user_verified=False
    print useremail   
    if str(Ad_Dictionary.get(useremail)) == str('None'):
        user_located=False
    print str(user_located)
    print str(Ad_Dictionary.get(useremail))

    user_dn=''
    if user_located==True:
        
                 
        print 'DN : ' + str(Ad_Dictionary.get(useremail)[0])
        print 'Display Name : ' + str(Ad_Dictionary.get(useremail)[1])
        print 'ID : ' +  str(Ad_Dictionary.get(useremail)[4])
        print 'Mobile number:' + str(Ad_Dictionary.get(useremail)[2])
         
        user_dn=str(Ad_Dictionary.get(useremail)[0])
        if str(Ad_Dictionary.get(useremail)[2]) == mobile and str(Ad_Dictionary.get(useremail)[4]) == ID:
           user_verified==True
           print "User " + str(Ad_Dictionary.get(useremail)[1]) + " has been verified."
           print "Procceding with password reset"
           newpass=gen_random_password()                  
           resetUserPassword(str(Ad_Dictionary.get(useremail)[0]),newpass)
           print newpass
                       
        else:
           user_verified==False
           print "Failed on the attempt to identify user " + str(Ad_Dictionary.get(useremail)[1])       
           
    
    return user_verified, user_dn
    exit(0)
    


    
def gen_random_password(length=10):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    password = ''
    for i in range(length):
        password += chars[ord(os.urandom(1)) % len(chars)]
    #print 'Generated Password :' + password        
    return password



def resetUserPassword(dn,newpassword):
   aduser1=pyad.aduser.ADUser.from_dn(dn)
   aduser1.set_password(newpassword)
   print 'Password Reset on user : ' + dn



if __name__ == '__main__':    
    print 'Starting Up.... only for debuging, testing purposes'
    starttime=time.time()       
    #verifyADuser('john.doe@unknown.org','0000005761','3444344')
    #CYTA_Web_SMS(9999999)
    elapsedtime=time.time()-starttime
    print '\nTotal time to complete script ' +str(elapsedtime) + ' seconds.'  
    print 'done'

    


