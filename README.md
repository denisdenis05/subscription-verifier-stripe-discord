# subscription-verifier-stripe-discord
A discord bot that gives you a certain role if you purchased a subscription on Stripe (or based on a whitelisted mail)

## How does this work:
If you want to create a 'exclusive' discord community based on a subscription, good news! That script is for you! 

### In order to make this work, you will need to insert some info in the `main.py` file:

> Create a [discord bot](https://www.androidpolice.com/how-to-make-discord-bot/), grab the bot's token and insert it on the last line of the code

> Create a stripe account, a subscription plan and grab the Stripe API Key (secret key). Insert that key on line 17 (stripe.api_key = ...). The default key is a test key and won't work if you don't insert your own (kinda optional, the bot works with the test key but you'll miss out the stripe connection feature, the only feature that'll work would be the whitelisted mail one)

> Create a role on a server. Grab [the server id](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-#:~:text=Obtaining%20Server%20IDs%20-%20Mobile%20App,name%20and%20select%20Copy%20ID.), the [role id](https://discordhelp.net/role-id), and introduce them on line 21 and line 25.

> Create a mail and introduce the mail's info in the 219-227 lines. You need to insert a server (for gmail is `smtp.gmail.com`, search the SMTP server for the mail provider you use. Also check the port, if the mail server doesn't use port 587, you'll most likely need to remove line 221 and 222 `server.starttls() server.ehlo()`), a mail and a password.  

> Start the bot and whitelist a mail (if needed) via the `.addwhitelist` command (`.addwhitelist somemail@testmail.com`). Use the `.click` command to send a message with a button that'll start the process


## More in-depth explanation of the process:
The end user wants to join your discord server but he's prompted up with a button. When the user clicks the button, the bot requests his name and email. After the user submits the mail, he will get a confirmation code on the mail. After the user inputs the code (proves that he can access the mail), the bot verifies if the mail is either: 
1. the mail is whitelisted (via the `.addwhitelist` command)
2. the mail was used to buy a subscription and the subscription is active
If one of the previous is confirmed, the user gets the promised role.



### Dependencies:

> Discord.py V2.0 (`pip install discord.py`)

> Requests (`pip install requests`)

> Stripe (`pip install stripe`)
