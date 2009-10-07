#!/usr/bin/python

import urllib, urllib2, cookielib, os, re

"""
Class to encapsulate sending T-Mobile webtexts.
"""

class TMobileSMS:
    """
    Send SMS via the web using T-Mobile.
    """



    def __init__(self):
        """

        """
        self.message = {}
        self.tagstr = r"""(<input type="hidden" name="org.apache.struts.taglib.html.TOKEN" value="(.*)">)"""

        self.txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

        self.tmobile_url = "http://www.t-mobile.co.uk/"
        self.login_url = 'https://www.t-mobile.co.uk:443/service/your-account/login/'
        self.webtext_prepare_url = "https://www.t-mobile.co.uk/service/your-account/private/wgt/send-text-preparing/"
        self.send_text_url = "https://www.t-mobile.co.uk/service/your-account/private/wgt/send-text-processing/"
        self.webtext_success_url = "https://www.t-mobile.co.uk/service/your-account/private/wgt/sent-confirmation/"


    def send_message(self, recipient, message, user, password):
        """
        Send a text message.
        """

        cookiejar = cookielib.LWPCookieJar()

        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        urllib2.install_opener(opener)

        # Get initial session cookie. Now required.
        tmobile = opener.open(self.tmobile_url)
        response = tmobile.read()
        print tmobile.info()

        values = {'username' : user,
                  'password' : password,
                  'submit' : 'Login'}

        data = urllib.urlencode(values)
        
        # Login
        loginpage = opener.open(self.login_url,  data)
        response = loginpage.read()
        login_redirect = loginpage.geturl()
        #print loginpage.info()

        # Check if login was successful.
        searchstr = r"""^https://www.t-mobile.co.uk/service/your-account/private/home/"""
        compile_obj = re.compile(searchstr)
        match_obj = compile_obj.search(login_redirect)

        if not(match_obj):
            return "Login failed!"

        # Go to the send a webtext page.
        textpage = opener.open( self.webtext_prepare_url )
        response = textpage.read()
        print textpage.geturl()
        print textpage.info()

        #compile_obj = re.compile(rawstr)
        #match_obj = compile_obj.search(response)

        if not(textpage.geturl() == self.webtext_prepare_url):
            return "Redirect to webtext page failed."

        print "textpage.geturl(): ", textpage.geturl()
        print "self.webtext_prepare_url: ", self.webtext_prepare_url

        # Get the apache struct cookie.
        compile_obj = re.compile(self.tagstr)
        match_obj = compile_obj.search(response)

        # Get matching regexp groups.
        all_groups = match_obj.groups()
        apache_token = match_obj.group(2)

        self.message = {'org.apache.struts.taglib.html.TOKEN' : apache_token,
           'selectedRecipients' : recipient,
           'message' : message,
           'submit' : 'Send'}

        
        messagedata = urllib.urlencode(self.message)
        print "messagedata: ", messagedata
        textpage = opener.open(self.send_text_url, messagedata)
        response = textpage.read()
        if not(textpage.geturl() == self.webtext_success_url):
            print "There was a problem sending your message."
            return "There was a problem sending your message."
        return "Message sent."
  

