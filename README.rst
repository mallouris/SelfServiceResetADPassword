1-2-3 Self Service Reset Password Tool for MS Active Directory using SMS messages
=================================================================================


Introduction
============

A small web application, that will provide the simple functionality *(in three steps) for a secure self service password reset on a Microsoft Active Directory Users Repository.


Requirements
============		

SelfServiceResetADPassword requires pywin32, pyAD, httplib2, tornado web server, bootstrap3 framework, windows 7 or 2008R2, python 2.7, SMS gateway (Implementation for the CYTA sms gateway is now available).


How it works
============
Password reset is accomplished through the use of short message service (sms). A two factor authentication method is implemented since
it is necessary for the user to enter personal information like Civil-ID, employee-ID, mobile phone number in step 1. After verification of the entered information by the system a unique 4 digitword is send to the user's mobile number, this is step 2. Upon enering this unique 4 digitword to the application a new password is generated and send to user's mobile number, this is step 3, completing the task of a secure self service password.


Configuration
=============
After cloning this repository it is necessary for configuration changes for the web app to work correctly.

A. Edit the passReset.py file

Find the main() function and set the parameter cookie_secret to a unique secret string. Replace the default
secret word *61oETzSaLaMmANtArgEmGePPFuYh7EQnp2zrtP1o/Vo=*. 

Save changes.

B. Edit the AD_User_Pass_Reset.py

Find  the CYTA_Web_SMS(mobileNumber) function and replace the *fill in username* and *fill in secret key*
with your provided data so you will be able to use the CYTA SMS gateway.

Find the ReplicateAD() function and fill in the necessary data on *pyad.pyad.set_defaults(ldap_server='',....*

Also fill in the necessary data on the *q.execute_query(......, base_dn= "DC=,DC=DC=")*

Find the verifyADuser(useremail, ID, mobile) function and and fill in the necessary data on *pyad.pyad.set_defaults(ldap_server='',....*

Save changes.

Initialization - First Run
==========================
It is essential that after configuration you run the *AD_Replication.py* file. It will take from seconds to a couple of minutes
to localy replicate necessary information on a local file shelve. This is necessary for not directly quering the AD, causing traffic and possibly a denial of service situation. After completion the newly created file *AD_Replica.dat* will be placed on current directory.

Normal Operation
================
Web application should be started by running the *passReset.py*, tornado web server will start listening to requests.
It is also recomended that you schedule a task that will run the *AD_Replication.py* at least once per day so any changes
will sync to the local *AD_Replica.dat* file.


License
=======
SelfServiceResetADPassword is licensed under the GNU ver. 3 License.
