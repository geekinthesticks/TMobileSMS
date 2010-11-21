#!/usr/bin/python

##   Copyright (C) 2009 Ian Barton.
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 3, or (at your option)
##   any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.

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

        # Apache generated unique tag. Need to post this with the rest of the form.
        self.tagstr = r"""(<input type="hidden" name="org.apache.struts.taglib.html.TOKEN" value="(.*)">)"""

        # urls of the various T-Mobile pages we need.
        self.tmobile_url = "http://www.t-mobile.co.uk/"
        self.login_url = 'https://www.t-mobile.co.uk:443/service/your-account/login/'
        self.webtext_prepare_url = "https://www.t-mobile.co.uk/service/your-account/private/wgt/send-text-preparing/"
        self.send_text_url = "https://www.t-mobile.co.uk/service/your-account/private/wgt/send-text-processing/"
        self.webtext_success_url = "https://www.t-mobile.co.uk/service/your-account/private/wgt/sent-confirmation/"

    def send_message(self, message_data):
        """
        Send a text message.
        """

        cookiejar = cookielib.LWPCookieJar()

        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        urllib2.install_opener(opener)

        # Get initial session cookie. Now required.
        tmobile = opener.open(self.tmobile_url)
        response = tmobile.read()
        if (message_data['debug']):
            print tmobile.info()
	else:
	    print "Step 1 of 3."

        if (message_data['deliveryReport']):
            values = {'username' : message_data['user'],
                      'password' : message_data['password'],
                      'sendDeliveryReport' : '1',
                      'submit' : 'Login'}

        else:    
            values = {'username' : message_data['user'],
                      'password' : message_data['password'],
                      'submit' : 'Login'}

        data = urllib.urlencode(values)
        
        # Login
        loginpage = opener.open(self.login_url,  data)
        response = loginpage.read()
        login_redirect = loginpage.geturl()

        if message_data['debug']:
            print loginpage.info()
	else:
	    print "Step 2 of 3."

        # Check if login was successful.
        searchstr = r"""^https://www.t-mobile.co.uk/service/your-account/private/home/"""
        compile_obj = re.compile(searchstr)
        match_obj = compile_obj.search(login_redirect)

        if not(match_obj):
            return "Login failed!"

        # Go to the send a webtext page.
        textpage = opener.open( self.webtext_prepare_url )
        response = textpage.read()

        if message_data['debug']:
            print textpage.geturl()
            print textpage.info()
	else:
	    print "Step 3 of 3."

        if not(textpage.geturl() == self.webtext_prepare_url):
            return "Redirect to webtext page failed."

        if message_data['debug']:
            print "textpage.geturl(): ", textpage.geturl()

        # Get the apache struct cookie from the page.
        compile_obj = re.compile(self.tagstr)
        match_obj = compile_obj.search(response)

        # Get matching regexp group.
        apache_token = match_obj.group(2)

        self.message = {'org.apache.struts.taglib.html.TOKEN' : apache_token,
           'selectedRecipients' : message_data['recipient'],
           'message' : message_data['message'],
           'submit' : 'Send'}

        
        messagedata = urllib.urlencode(self.message)

        textpage = opener.open(self.send_text_url, messagedata)
        response = textpage.read()

        if message_data['debug']:
            print textpage.info()
            print textpage.geturl()
        
        if not(textpage.geturl() == self.webtext_success_url):
            return "There was a problem sending your message."
            
        return "Message sent."
