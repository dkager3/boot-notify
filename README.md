# boot-notify
A systemd service geared toward Raspberry Pi boards that provides an email notification once the board has booted. This is primarily used to verify that a headless board has booted.

## Features
* Easy to install/remove
* Email notification when the board has been booted
* Configurable INI file

## Installation
Follow the steps below for installing the boot-notify service.

1. Clone the repo
```
git clone https://github.com/dkager3/boot-notify.git
```
2. Go into the new boot-notify directory and run the install script as root
```
cd boot-notify
sudo ./install.sh
```
3. Update the BotSettings.ini file in **boot-notify/src/** to set the bot email login/password as well as the recipient's email address. See the INI section for more details on the INI file.
4. Next the device is booted, an email will be sent to the one listed in BotSettings.ini.

## Removal
To remove the boot-notify service, simply run the remove.sh script.
```
sudo ./remove.sh
```

## Start/Stop
The boot-notify service can be disabled without uninstalling it. To temporarily stop the service from emailing when the board boots up, run:
```
sudo systemctl disable boot-notify
```
To re-enable the service again, simply run:
```
sudo systemctl enable boot-notify
```

## INI
### INI Fields
| Field              | Default Value          | Description                                                                                    |
|--------------------|------------------------|------------------------------------------------------------------------------------------------|
| device             | RPi Zero               | Type of device, used in the email                                                              |
| name               | Node 1                 | Name of the device, used in the email                                                          |
| log_to_console     | 1                      | 1 - Logs printed to console; 0 - No logs printed to console                                    |
| log_to_file        | 1                      | 1 - Logs saved in log file; 0 - No logs saved in log file                                      |
| log_max_len        | 80                     | Maximum characters for log message                                                             |
| log_file_name      | run.log                | Log file name                                                                                  |
| log_folder_path    | \<path\>                 | Path to log file folder, set automatically during installation                                 |
| bot_email_login    | \<Bot Email Here\>       | Replace this with the email address you're using to send the notification emails from          |
| bot_email_password | \<Bot Password Here\>    | Replace this with the password for the email you're using to send the notification emails from |
| recipient_email    | \<Recipient Email Here\> | Replace this with the email address you want notifications to go to                            |

By default, the INI has the device listed as "RPi Zero" and "Node 1". Feel free to change these to represent what device/name you'd like to use in your notifications.

### Modifying the INI
After installation, you can modify the INI by editing **boot-notify/src/BotSettings.ini**. Simply update any of the values you'd like, but be careful! The Python script (boot-notify.py) expects certain data types/format from the INI and could misbehave if you enter something that doesn't make sense. Don't fret, you can always change the INI back to its original state by uninstalling and reinstalling the service.

Some lines are commented out. You can uncomment them by removing the semicolon at the front of the line, then edit the placeholder value stuck there. For instance:
```
[bot_settings.email]
;bot_email_login = <Bot Email Here>
;bot_email_paswd = <Bot Password Here>
;recipient_email = <Recipient Email Here> 
```
Can be edited to something like this:
```
[bot_settings.email]
bot_email_login = some.email@gmail.com
bot_email_paswd = 136465465165
recipient_email = janedoe@example.com
```

### Email Configuration
In order for the boot-notify service to work, the INI needs to be configured with an email login, password, and email address of the recipient. A separate Gmail account is required. Once you make an account, you need to get an [app password](https://support.google.com/accounts/answer/185833) to use to login with the service.

Modify the **[bot_settings.email]** section of the INI to give the required details (bot_email_login, bot_email_paswd, and recipient_email).
