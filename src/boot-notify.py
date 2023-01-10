#!/usr/bin/python3
#
# Script to send email when Pi boots.
# Systemd service invokes script here:
#   /etc/systemd/system/boot-notify.service

from BootNotifyModules import BotEmail as bt
from BootNotifyModules import logger as lg
from BootNotifyModules import config
from datetime import datetime, timezone
import getopt
import sys

# Globals
# Default INI location
INI_FILE = 'BotSettings.ini'

def init_logger(logger, conf):
  '''
  Inits logger with values from the INI.
  
      Parameters:
          logger (logger.Logger): Logging functionality
          config (configparser.SectionProxy): Config logging settings
      
      Returns:
          None
  '''
  
  try:
    logger.setConsoleLogging(bool(int(conf['log_to_console'])))
  except:
    pass
    
  try:
    logger.setFileLogging(bool(int(conf['log_to_file'])))
  except:
    pass
    
  try:
    logger.setMaxLogLen(int(conf['max_log_len']))
  except:
    pass
  
  try:
    logger.setLogFile(conf['log_folder_path'], conf['log_file_name'])
  except:
    pass

def usage():
  '''
  Print usage statement.
  
      Parameters:
          None
      
      Returns:
          None
  '''

  print('\npython3 boot-notify.py [-i ini] [-h]')
  print('  -i ini:  Override default INI path.')
  print('  -h:      Print usage.\n')


if __name__ == '__main__':
  # Get input args
  try:
    opts, args = getopt.getopt(sys.argv[1:], "i:h")
  except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

  # Check input args
  for o, a in opts:
    if o == '-i':
      INI_FILE = a
    elif o == '-h':
      usage()
      sys.exit()

	# Read ini file for bot settings
  config = config.ConfigSettings(INI_FILE)
  if not config.readConfigFile():
    sys.exit("ERROR: {} not found, corrupt, or may not be installed.".format(INI_FILE))
  
  # Set up logging
  logger = lg.Logger()
  init_logger(logger, config.logging)

  # Get email details
  try:
    email_login = config.email['bot_email_login']
    email_paswd = config.email['bot_email_paswd']
    recipient   = config.email['recipient_email']
  except:
    logger.log("Email details missing from the INI.", event_type=lg.ERROR)
    logger.log('[END OF SCRIPT]')
    sys.exit(2);

  # Get device details
  try:
    device = config.info['device']
    name = config.info['name']
  except:
    logger.log("Device type and/or name missing from INI. Using defaults.", event_type=lg.WARNING)
    device = 'RPi'
    name = 'Node 1'

  # Get date/time booted, UTC
  boot_utc_time = datetime.now(timezone.utc).strftime("%d %b, %Y %H:%M:%S UTC")
  logger.log('Booted at {}.'.format(boot_utc_time))

  # Setup email
  email = bt.BotEmail(email_login, email_paswd)
  subject = device + ' ' + name + ' Booted'
  body = device + ' ' + name + ' booted at ' + boot_utc_time + '.'

  # Send email
  if email.send(subject, body, recipient):
    logger.log('Notification email sent to {}.'.format(recipient))
  else:
    logger.log('Failed to send notification email to {}.'.format(recipient), event_type=lg.ERROR) 

  # Insert gap into log for readability
  logger.log('[END OF SCRIPT]')
