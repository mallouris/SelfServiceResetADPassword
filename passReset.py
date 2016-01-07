# -*- coding: cp1253 -*-
#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import AD_User_Pass_Reset2


tornado.options.define("port", default=8888, help="app port", type=int)


class VerificationHandler(tornado.web.RequestHandler):
    def post(self):
        form_data = [ self.get_argument('email',''),self.get_argument('civil-id',''),\
                      self.get_argument('student-id',''),self.get_argument('phone',''),\
                      self.get_argument('smsword','')]

        user_verified = False  
        user_verified, user_dn = AD_User_Pass_Reset2.verifyADuser(form_data[0],form_data[2],form_data[3])
        

        ####
        ###reset cookie to something unknown to the end user (stop back-fwd multiple try)
        self.set_secure_cookie("smsword", AD_User_Pass_Reset2.gen_random_password(4))
        if user_verified==True and  self.get_secure_cookie('smsword')== form_data[4]:            
            newpass=AD_User_Pass_Reset2.gen_random_password()
            #Uncomment on production to reset password
            #AD_User_Pass_Reset.resetUserPassword(user_dn,newpass)
            print 'successfuly generated a new password :' +  newpass
            AD_User_Pass_Reset2.CYTA_Web_SMS(form_data[3], "The new generated password is:" + newpass + \
                                                           "\nYou may now access the organizations IT systems. We advice you to change it asap.")
            self.render("verify.html",phone=form_data[3])

        else :
            print 'failed to generate a new password'
            self.render("failure.html")
            


        #for debugging purposes                     
        print 'secure cookie from form:' + form_data[4]
        print 'secure cookie from cookie:' + self.get_secure_cookie('smsword')
        #self.render("verify.html",phone=form_data[3])
        



class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_secure_cookie("smsword", AD_User_Pass_Reset2.gen_random_password(4))
        
##        if not self.get_secure_cookie("smsword"):
##            self.set_secure_cookie("smsword", AD_User_Pass_Reset.gen_random_password(4))
##            print "Your cookie was not set yet!"
##        else:
##            print "Your cookie was set!" + self.get_secure_cookie("smsword")
        #self.write("URI: " + self.request.uri)
        self.render("index.html")


class RequestHandler(tornado.web.RequestHandler):   

    def post(self):
       
        form_data = [ self.get_argument('email',''),self.get_argument('civil-id',''),\
                      self.get_argument('student-id',''),self.get_argument('phone','')]

        user_verified = False  
        user_verified, _ = AD_User_Pass_Reset2.verifyADuser(form_data[0],form_data[2],form_data[3])
        print 'user verified' +  str(user_verified) + "  " + form_data[0] + "\n" + form_data[2] + "\n" + form_data[3]
        print 'secret_cookie:' + self.get_secure_cookie('smsword')


        if user_verified == True:            
            MesgA = 'The system has successfully verified your identity . You will have by now received an '\
                    'SMS to your mobile phone. Fill in the secret word bellow and the system will generate a new ' \
                    'password and send it through SMS to your mobile phone. :  ' + form_data[3]
            MesgB = 'Secret word on you mobile :'
            Button_Msg = 'Get me a new password'
            MesgHide=' '
            AD_User_Pass_Reset2.CYTA_Web_SMS(form_data[3],'Use the following word to validate your self : ' + self.get_secure_cookie('smsword'))
        else:
            MesgA = 'Failed to verify your identity. Go back, correct the information needed and try again!!!'\
                    'Have in mind that all attempts are beeing logged and monitor by the Organization\'s IT Systems!'
            MesgB = ' '
            Button_Msg = 'Get back to STEP 1'
            MesgHide = 'hide'
                    
    
        
        self.render("result.html",data_to_Form=form_data, MesgA=MesgA, MesgB=MesgB, MesgHide=MesgHide)
        

def main():
    settings = {"cookie_secret":"61oETzSaLaMmANtArgEmGePPFuYh7EQnp2zrtP1o/Vo=",\
                "template_path": "html","static_path": "static", "debug": True}                     
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/results.html", RequestHandler),
        (r"/verify.html", VerificationHandler),
        (r"/images/(.*)", tornado.web.StaticFileHandler,{"path": "./images"},)        
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
