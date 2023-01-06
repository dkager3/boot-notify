#/usr/bin/sh

SVCNAME='boot-notify'
SVCPATH1='/etc/systemd/system/boot-notify.service'
SVCPATH2='/usr/lib/systemd/system/boot-notify.service'
NOTIFY_INI="$PWD/src/BotSettings.ini"

# Remove INI if exists
if [ -f "$NOTIFY_INI" ]; then
  echo Removing $NOTIFY_INI ...
	rm $NOTIFY_INI
	echo Removed $NOTIFY_INI
  echo
fi

echo Removing $SVCNAME service ...

# Stop the service
if systemctl stop boot-notify.service; then
  echo Stopped $SVCNAME
else
  echo Error stopping $SVCNAME
  exit
fi

# Disable the service
if systemctl disable boot-notify.service; then
  echo Disabled $SVCNAME
else
  echo Error disabling $SVCNAME
  exit
fi

# Remove service
if [ -f $SVCPATH1 ]; then
	rm $SVCPATH1
	echo Removed $SVCPATH1
fi 

# Remove service
if [ -f $SVCPATH2 ]; then
	rm $SVCPATH2
  echo Removed $SVCPATH2
fi

# Reload changed unit files
if systemctl daemon-reload; then
  echo Reloaded changed unit files
else
  echo Failed to reload changed unit files
  exit
fi

# Reset any units from a failed state
if systemctl reset-failed; then
  echo Reset units in failed state
else
  echo Failed to reset units in a failed state
  exit
fi

echo
echo Successfully removed $SVCNAME!
