#!/usr/bin/python


##   Copyright (C) 2009 Ian Barton.
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2, or (at your option)
##   any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.



from tmobilesms import *
import optparse, sys
import ConfigParser

# Recipient data and T-Mobile user name and password are
# stored in ~/tmobilesms.
# Note the phone number format. Number is preceeded
# by country code without 00 or + symbol.

def read_config():
    """
    Read the configuration data.
    """
    user_data = {}
    recipient_data = []
    recipients = {}
    
    config = ConfigParser.ConfigParser()
    
    config.read(os.path.expanduser("/home/ian/.tmobilesms"))
    if config == None:
        print "Unable to read configuration file: /home/ian/.tmobilesms."
        sys.exit(2)

    try:
        user_data["user"] = config.get("tmobile", "user")
        user_data["password"] = config.get("tmobile", "password")

        recipient_data = config.items("recipients")
        for key, value in recipient_data:
            recipients[key] = value
            
    except ConfigParser.NoSectionError:
        print "Error parsing file."
        sys.exit(2)
        
    return user_data, recipients

 

class OptionParser (optparse.OptionParser):

    def check_required (self, opt):
      option = self.get_option(opt)

      # Assumes the option's 'default' is set to None!
      if getattr(self.values, option.dest) is None:
          self.error("%s option not supplied" % option)


def truncate(string,target):
    """
    Truncate messages to 160 characters.
    """
    if len(string) > target:
        return string[:(target-3)] + "..."
    else:
        return string


def main():

    user_data = {}
    recipients = {}    
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-r", "--recipient", dest = "recipient", help = "Recipent name")
    parser.add_option("-m", "--message", dest = "message", help = "Message (max. 160 chars)")
    parser.add_option("-d", "--debug", dest = "debug", help = "Print debug information.")
    parser.add_option("-t", "--delivery-report", action = "store_true", dest = "delivery_report", default = False, help = "Send a delivery report.")


    (options, args) = parser.parse_args()
    parser.check_required("-r")
    parser.check_required("-m")

    user_data, recipients = read_config()

    mysms = TMobileSMS()

    # Trim message to 160 characters.
    message = truncate(options.message, 160)


    if not(options.recipient in recipients):
        print "User: %s not known" % (options.recipient)
        sys.exit()

    #print message
    messageData = {}
    messageData['recipient'] = recipients[options.recipient]
    messageData['message'] = message
    messageData['user'] =  user_data['user']
    messageData['password'] = user_data['password']
    messageData['deliveryReport'] = 'False'
    messageData['debug'] = 'False'


    retval = mysms.send_message(messageData)
    print retval


if __name__ == "__main__":
    main()
