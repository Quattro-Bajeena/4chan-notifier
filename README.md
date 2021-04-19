# 4chan-notifier
Python scripts that check if there are 4chan threads with specific keywords, on chosen boards.
Compare them with the previous check to find out if any of them are new.
Then send a notification about them through Pushover app.

They were designed to work with [Pushover](https://pushover.net/) service, which is used to create push notification to your devies using web API.
Using it personally on one device only cost single $5 payment.

Enabling debug mode in config.yml will print the message to the standard output. 


# TODO:
- better configurability, ex. specify especific keywords for certain boards individually
- more standalone mode, without using Pushover.