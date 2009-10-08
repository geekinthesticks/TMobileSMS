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

# Dictionary for recipients.
recipients = {'anne' : '44123456',
              'ian' : '44123456',
              'john' : '44123456'
              }

# Username and password for T-Mobile web site.
username = "username"
password = "password"


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
    
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-r", "--recipient", dest = "recipient")
    parser.add_option("-m", "--message", dest = "message")
    parser.add_option("-d", "--debug", dest = "debug")
    parser.add_option("-t", "--delivery-report", dest = "delivery_report")
    (options, args) = parser.parse_args()
    parser.check_required("-r")
    parser.check_required("-m")


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
    messageData['user'] = username
    messageData['password'] = password
    messageData['deliveryReport'] = 'False'
    messageData['debug'] = 'False'


    retval = mysms.send_message(messageData)
    print retval


if __name__ == "__main__":
    main()
