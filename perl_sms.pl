#!/usr/bin/perl -w
# sms.pl
# First install libwww-mechanize-perl and libcrypt-ssleay-perl 

# Sends an SMS via T-Mobile's webtext service. This will only work if you have
# an account with T-Mobile, and have proven that you can successfully send text
# messages when using the webtext service manually. If/when T-Mobile change
# the structure of the webtext part of their site, this script is likely to
# break. Before you can use this, you need to:
# 
# 1. Rename the file from "sms.pl.txt" to "sms.pl"
# 2. Change the $username and $password variables.
# 3. Enter some telephone numbers and shortcuts in the section that begins
#    "my $recipientNumber =..." (see comments below).
# 4. Make the script executable, e.g. using "chmod +x sms.pl".
#
# Usage is then something like:
#
#    sms.pl heloise "I have bad news about Abelard."
# 
# OR,
#
#    sms.pl heloise
#      ...and then enter the message when prompted.
#
# (I have also set up "sms" as an alias for "sms.pl", so that I can just type
# 'sms heloise "What's up, sugar pie?"', to make usage more natural.)
#
# KNOWN BUGS
# ----------
# - Weird things happen when you use exclamation marks in your message. This
#   is not a problem with my usually deadpan SMS style, but could be worrisome
#   for joy freaks and caffeine addicts. Must investigate -- probably just needs
#   escaping -- but I don't really want to delve any deeper into Perl. It would
#   be much nicer if I could get Mechanize to work in Python.
#
# Version 3. 2008-06-01.
#            No major code changes -- just a distro release with extra comments
#            and some rearrangement of variable definitions.
#
# Version 2. 2008-04-26.
#            Some changes required after script broke following upgrade to
#            Ubuntu version Hardy Heron, which also presumably updated to the
#            latest version of mechanize.pl. Had to change methods "form" to
#            "form_name", and "follow" to "follow_link". Also had to install
#            Crypt::SSLeay.
#
# Version 1. Date lost in the mists of time.

use strict;
use POSIX qw(ceil);
use Crypt::SSLeay; #new

use WWW::Mechanize;
# http://search.cpan.org/~petdance/WWW-Mechanize-1.34/lib/WWW/Mechanize.pm
# http://www.perl.com/pub/a/2003/01/22/mechanize.html
# http://search.cpan.org/dist/WWW-Mechanize/lib/WWW/Mechanize/FAQ.pod
# http://search.cpan.org/~petdance/WWW-Mechanize-1.34/lib/WWW/Mechanize.pm#$mech-%3Eclick_button(_..._)

my $username = "igbarton";
my $password = "aYcNPYUo23";


my $recipientShortcut=shift;
my $message=shift;

unless ($recipientShortcut) {
	print "\nUsage: $0 <recipient shortcut name> <message>\n\n";
	exit(1);
}

my $recipientNumber = "";
# Define telephone numbers with their shortcut codes by following the pattern
# below. The value of $recipientNumber should be formatted like this: 
# "00", then the country code ("44" for the UK), then the number that you would
# normally dial, *but with the initial "0" removed*. E.g., if the normal number
# is 07841123456, then the number that you should enter would be
# 00447841123456.  

if($recipientShortcut eq "abelard") {
  $recipientNumber = "00447841123456";
}
# To add more numbers, copy from HERE...
elsif($recipientShortcut eq "ian") {
  $recipientNumber = "447989385393";
}
# ...to HERE, then paste below.

unless ($recipientNumber) {
	print "\nSorry, could not translate shortcut to number.\n\n";
	exit(1);
}

unless ($message) {
  print "\nPlease enter message: ";
  $message = <STDIN>;
  chomp $message;
}

unless ($message) {
	print "\nEmpty message. Try again.\n\n";
	exit(1);
}



#print "Thanks.\n";
my $numTexts = ceil(length($message) / 160);
print "\nYour message has a length of " . length($message) . " characters, which will cost you $numTexts text";
unless($numTexts == 1){ print "s"};
print ".\n\n";

if( $numTexts > 1 && length($message) % 160 != 0 ) {
  print "You could save a text message if you reduced your message by ";
  print length($message) % 160 . " characters.\n\n"
}

my $abjadic = $message;
$abjadic =~ tr/aeiouAEIOU//d; # Remove all vowels from the message.
$abjadic =~ s/  / /g;         # Convert any double spaces (resulting from the 
               # above) to a single space. s is for substitute, g is for global.
$numTexts = ceil(length($abjadic) / 160);
print "Want to go abjadic? Without vowels your message would be " . length($abjadic) . " chars long and would cost you $numTexts text";
unless($numTexts == 1){ print "s"};
print ". It would look like this:\n\n[ $abjadic ]\n\n";


print "Send message? (f=full; a=abjadic; n=no) ";
chomp(my $answer = <STDIN>);

$answer = lc($answer);

unless ( $answer eq "f" || $answer eq "a"){
  print "OK, aborting.\n";
  exit(1);
}

if ( $answer eq "a" ){
  $message = $abjadic;
}

my $mech = WWW::Mechanize->new( autocheck => 1 );

$mech->get("http://www.t-mobile.co.uk/");

# login page
print "\nFound " . $mech->uri;
$mech->form_name("MTMUserLoginForm"); # was just "form"
$mech->field("username", $username);
$mech->field("password", $password);
$mech->click();

# your-account page
if ( index($mech->uri, 'your-account/private/home') == -1 ){
  print "\nSorry, could not log in.\n\nPlease wait a minute and try again.\n\n";
	exit(1);
}
print "\nLogged in.";
# $mech->follow("Send a Webtext"); # old
$mech->follow_link( text => 'Send a webtext', n => 1 ); # new: follow first link with that name

# send-text-preparing page
if ( index($mech->uri, 'send-text-preparing') == -1 ){
  print "\nSorry, could not reach send-text-preparing page.\n\nPlease wait a minute and try again.\n\n";
	exit(1);
}
print "\nPreparing text message.";
$mech->form_name("sendTextForm");
$mech->field("selectedRecipients", $recipientNumber);
$mech->field("message", $message);
$mech->click("submit");

# send-text-processing page (Done)
if ( index($mech->uri, 'send-text-processing') == -1 ){
  print "\nSorry, could not send message.\n\nPlease wait a minute and try again.\n\n";
	exit(1);
}
print "\nMessage sent.\n\n"; # Would be better also to check for confirmation message.
# $mech->follow("Log out"); # Gives an error message.

