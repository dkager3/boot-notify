#!/usr/bin/python3
import configparser

# Status Codes
READ_FAIL = 0 # Failed to read config file
READ_SUCC = 1 # Config file read successfully

class ConfigSettings:
  """
  Class to store config settings from INI file.
  
  Attributes
  ----------
  ini_file : str
    Path to bot settings INI file
  info : configparser.SectionProxy
    Device type and name
  logging : configparser.SectionProxy
    Logging settings section in INI file
  email : configparser.SectionProxy
    Email settings section in INI file
  
  Methods
  -------
  readConfigFile()
    Reads bot settings INI file and stores sections
  """
  
  def __init__(self, ini_file):
    """
    Constructor.
    
    Parameters
    ----------
      ini_file : str
        Path to bot settings INI file
    """
    
    self.ini_file = ini_file
    self.info     = None
    self.logging  = None
    self.email    = None
    
  def readConfigFile(self):
    """
    Validate INI exists and read it.
    
    Paramters
    ---------
      None
    
    Returns
    -------
      Read status : int
    """

    # Read INI
    config = configparser.ConfigParser()
    try:
      if not config.read(self.ini_file):
        return READ_FAIL
    except:
      return READ_FAIL

    # Extract device info from INI
    try:
      self.info = config['bot_settings.info']
    except:
      pass
    
    # Extract log settings from INI    
    try:
      self.logging = config['bot_settings.logging']
    except:
      pass
     
    # Extract email settings from INI     
    try:
      self.email = config['bot_settings.email']
    except:
      pass
    
    return READ_SUCC
