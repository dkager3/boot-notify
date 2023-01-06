#!/usr/bin/sh

SVCNAME='boot-notify'

# Template file locations
SVCTEMP="$PWD/template/boot-notify.service.template"
INITEMP="$PWD/template/BotSettings.ini.template"

# Template installation locations
SERVICE="/etc/systemd/system/boot-notify.service"
NOTIFY_INI="$PWD/src/BotSettings.ini"
DEFLT_LOGS_PATH="$PWD/logs"

# Location of boot-notify script
NOTIFY_SCRIPT="$PWD/src/boot-notify.py"

# Validate that the service template exists
if [ ! -f $SVCTEMP ]; then
  echo $SVCTEMP not found!
  exit
fi

# Validate that the INI template exists
if [ ! -f $INITEMP ]; then
  echo $INITEMP not found!
  exit
fi

# Validate that the boot-notify script exists
if [ ! -f $NOTIFY_SCRIPT ]; then
  echo $NOTIFY_SCRIPT not found!
  exit
fi

echo Generating INI ...

# Generate INI from template with correct logs path
if sed "s|<path>|$DEFLT_LOGS_PATH|g" $INITEMP > $NOTIFY_INI;  then
  echo Created $NOTIFY_INI 
  echo
else
  echo Failed to create $NOTIFY_INI 
  exit
fi

echo Installing service ...

# Generate service from template with correct path to notify.py
if sed "s|<notify>|$NOTIFY_SCRIPT -i $NOTIFY_INI|g" $SVCTEMP > $SERVICE;  then
  echo Created $SERVICE 
else
  echo Failed to create $SERVICE
  exit
fi

# Update permissions on the service
if chmod 0644 $SERVICE; then
  echo Update permissions for $SERVICE
else
  echo Failed to update permissions for $SERVICE
fi

# Enable the service
if systemctl enable $SVCNAME; then
  echo Enabled $SVCNAME
else
  echo Error enabling $SVCNAME
  exit
fi

echo
echo $SVCNAME installed successfully!
