A Self Service Reset Password Tool for MS Active Directory using SMS messages
=============================================================================


Introduction
============

A small web application, that will provide the functionality for a secure self service password reset on a Microsoft Active Directory Users repository.


Requirements
============		

SelfServiceResetADPassword requires pywin32, pyAD, tornado web server, bootstrap3 framework, windows 7 or 2008R2, python 2.7, SMS gateway (Implementation for the CYTA sms gateway is now available)


How it works
============
Password reset is accomplished through the use of short message service (sms). 


Configuration
=============
After cloning this repository it is necessary for configuration changes for the web app to work correctly.

A. Edit the passReset.py file

Find the main() function and set the parameter cookie_secret to a unique secret string. Replace the default
secret word *61oETzSaLaMmANtArgEmGePPFuYh7EQnp2zrtP1o/Vo=*. 

Save changes and exit the editor.


License
=======

SelfServiceResetADPassword is licensed under the GNU ver. 3 License.
