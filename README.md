#OVERSEER-Ω
OVERSEER-Ω is a bot I made to moderate the comment section of my Telegram channel. You can find it via @OVERSEER_OMEGA_BOT.

It mainly functions as a moderator, but you can tinker with it to change its behavior to your liking. The current prompt provided is very simple. Also, you'll need an API key, which you can get from @BotFather if you wish to change it.

After creating a bot, maximize its capabilities in groups and enable adding it to any Telegram group. Then you'll have it set up.

The provided functionality is quite limited up until now. It reads each message, and if it detects any toxicity, it issues a permanent mute on the violating user and replies with a random proper error message.

The bot also has a 0.07% chance to either reply to a newly sent message, reminding a user that they are being watched, or to make this announcement for all users (each 0.035% chance).

You can, of course, change these as well. All of these were added only to make the bot spookier and serve no useful purpose.

OVERSEER-Ω uses microsoft/Phi-3-mini-128k-instruct, which is a very simple language model, but since I'm poor and can't afford to pay for an API, this is all I could get. To run it effectively, you would have to use GPUs.

The functionality to do so on your local system is provided in the code, though not guaranteed. I myself run it on Google Colab’s GPUs. However, do note that every session it has to download about 7GB before running, which I'm sure has a fix that I'm unaware of.

You can easily use any model you wish by making adjustments to the code.

There are many functionalities to be added to OVERSEER-Ω, like:

Issuing warnings before banning
Interacting with users
All of which can be added, and I plan to add myself.

The current model's performance can be upgraded by providing it with examples of "OK" and "NOT OK" messages for it to learn and also by providing a more comprehensive prompt.

I will update the bot as time passes by.
