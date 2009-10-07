#!/usr/bin/python

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

    retval = mysms.send_message(recipients[options.recipient], message, username, password)
    print retval


if __name__ == "__main__":
    main()
