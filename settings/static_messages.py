from config import *

WELCOME_MESSAGE = f"""
Hello, NAME! I am your friendly {COIN_NAME} Airdrop bot

Total tokens allocated to airdrop:  *50,000,000 ${COIN_SYMBOL}*

⭐️ For Joining - Get *{AIRDROP_AMOUNT}* point
⭐️ For each referral - Get *{REFERRAL_REWARD}* point

📘_By Participating you are agreeing to the {COIN_NAME} (Airdrop) Program Terms and Conditions. Please see pinned post for more information.
Click "🚀 Join Airdrop" to proceed_
"""

PROCEED_MESSAGE = f"""
📢*Airdrop Rules*

✏️ *Mandatory Tasks*:
- Join our Telegram group(s)
- Follow our Twitter page(s)

😡*Prohibited by the rules*: 
- Unsubscribe from the channel
- Leave the project chat

_NOTE: Users found cheating would be disqualified & banned immediately._

{WEBSITE_URL}
"""

MAKE_SURE_TELEGRAM = f"""
🔹 Subscribe to our channel and join the chat room
{TELEGRAM_LINKS}
"""

FOLLOW_TWITTER_TEXT = f"""
🔹 Follow our Twitter page
{TWITTER_LINKS}
"""

SUBMIT_BEP20_TEXT = f"""
Type in your Wallet Address

Please make sure your wallet supports the *{AIRDROP_NETWORK}*

Example:
UQBxCOstPWvIADbaYYBapGhwfRZCEZUui5p2OEFHU0a\_wWem

_Incorrect Details? Use /restart command to start over_
"""

JOINED = f"""
*Thank you!*

Rewards would be sent out automatically to your {AIRDROP_NETWORK} address

*Don't forget to*:
🔸 Stay in the telegram channels
🔸 Follow all the social media channels for the updates

Your personal referral link (+*{REFERRAL_REWARD}* point for each referral)
REPLACEME
"""
