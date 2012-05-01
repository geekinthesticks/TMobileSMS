#!/usr/bin/python2


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
# stored in ~/.tmobilesms .
# Note the phone number format. Number is preceeded
# by country code without 00 or + symbol.



def read_config(config_file):
    """
    Read the configuration data.
    """
    user_data = {}
    recipient_data = []
    recipients = {}

    config = ConfigParser.ConfigParser()

    config.read(config_file)
    if config == None:
        print ("Unable to read configuration file: %s ") % (config_file)
        sys.exit(2)

    try:
        user_data["user"] = config.get("tmobile", "user")
        user_data["password"] = config.get("tmobile", "password")

        recipient_data = config.items("recipients")
        for key, value in recipient_data:
            recipients[key] = value

    except ConfigParser.NoSectionError:
        print "Error parsing file.", config_file
        sys.exit(2)

    return user_data, recipients


def read_config(config_file):
    """
    Read the configuration data.
    """
    user_data = {}
    recipient_data = []
    recipients = {}

    config = ConfigParser.ConfigParser()

    # config.read(os.path.expanduser("~/.tmobilesms"))
    config.read(config_file)
    if config == None:
        print ("Unable to read configuration file: %s ") % (config_file)
        sys.exit(2)

    try:
        user_data["user"] = config.get("tmobile", "user")
        user_data["password"] = config.get("tmobile", "password")

        recipient_data = config.items("recipients")
        for key, value in recipient_data:
            recipients[key] = value

    except ConfigParser.NoSectionError:
        print "Error parsing file.", config_file
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

def send_message(messageData={}):
    """
    Send an SMS.
    """
    mysms = TMobileSMS()


    retval = mysms.send_message(messageData)
    print retval


def main():

    user_data = {}
    recipients = {}
    config_file = None

    usage = "usage: %prog [options] arg\nTry `%prog --help' for more information."
    parser = OptionParser(usage)
    parser.add_option("-r", "--recipient", dest = "recipient", help = "Recipent name")
    parser.add_option("-m", "--message", dest = "message", help = "Message (max. 160 chars)")
    parser.add_option("-d", "--debug", action = "store_true", dest = "debug", help = "Print debug information.")
    parser.add_option("-t", "--delivery-report", action = "store_true", dest = "delivery_report", default = False, help = "Send a delivery report.")
    parser.add_option("-p", "--print-recipients", dest = "list_recipients", default = False, action = "store_true", help = "Print the list of stored recipients")
    parser.add_option("-c", "--config-file", dest = "config_file", help = "Configuration file.")


    (options, args) = parser.parse_args()

    if not(options.list_recipients):
        parser.check_required("-r")
        parser.check_required("-m")

    if options.config_file == None:
        print "No config file specified. Using default ~/.tmobilesms"
        options.config_file = os.path.join(os.path.expanduser("~/"), ".tmobilesms")

        user_data, recipients = read_config(options.config_file)
    else:
        print "Using config file: ", options.config_file
        user_data, recipients = read_config(options.config_file)

    if options.list_recipients:
        for key, item in recipients.items():
            #print "Name: %s Tel: %s" % (key, item)
            print "{0:10} {1:10}".format(key, item)
        sys.exit()

    if not(options.recipient in recipients):
        print "User: %s not known" % (options.recipient)
        sys.exit()

    # Trim message to 160 characters.
    message = truncate(options.message, 160)

    messageData = {}
    messageData['recipient'] = recipients[options.recipient]
    messageData['message'] = message
    messageData['user'] =  user_data['user']
    messageData['password'] = user_data['password']
    messageData['deliveryReport'] = options.delivery_report
    messageData['debug'] = options.debug

    send_message(messageData)

if __name__ == "__main__":
    main()
