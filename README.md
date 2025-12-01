# binaryw0rm Telegram-channels

# Multi-Department Telegram Bot — One Bot for Sales, Projects & Support

**One bot — three channels — zero missed leads**

A clean, reliable Telegram bot that handles inquiries from three separate company channels:
- Sales Department
- Projects Department  
- Customer Support

Users click a button in the channel → instantly start a chat with the bot → leave a request → managers receive a perfectly formatted message with the exact department.

Demo bot: https://t.me/example_sales_bot

## How it works for the user

1. User sees a pinned post with a button in the channel  
   **Contact Sales Team**
2. Clicks the button → opens private chat with the bot
3. Bot greets:  
   **You’ve reached us from the “Sales Department” channel**
4. User selects “Leave a request” → types message
5. All managers instantly receive:
New request from Sales Department
From: Madlen (@madlen_example)
User ID: 898365589
Need consultation about Pro plan
Phone: +7 (999) 123-45-67

## Key Features

| Feature                                      | Status |
|----------------------------------------------|--------|
| Single bot serving 3+ departments           | Done   |
| Automatic department detection via deep link | Done   |
| Remembers department even in private chat    | Done   |
| Never loses requests (error-proof sending)   | Done   |
| Shows user ID & username to managers         | Done   |
| Runs 24/7 on Ubuntu with systemd             | Done   |
| Graceful handling of invalid manager IDs    | Done   |
| Easy to adapt to any number of channels      | Done   |

## Setup in 5 minutes

### Step 1 — Create your channels
- Sales Department
- Projects Department
- Customer Support

### Step 2 — Add the bot as admin to all channels
(Must have “Can read messages” permission)

### Step 3 — Add a pinned post with inline button in each channel

Example post text:
Sales Department — your personal assistant
Have a question? Contact us right now!
textInline button setup:

| Channel             | Button text                  | Bot URL                                             |
|---------------------|------------------------------|-----------------------------------------------------|
| Sales Department    | Contact Sales                | `https://t.me/example_sales_bot?start=sales`        |
| Projects Department | Contact Projects             | `https://t.me/example_sales_bot?start=projects`     |
| Customer Support    | Contact Support              | `https://t.me/example_sales_bot?start=support`      |

### Step 4 — Configure `.env`
```
.env
BOT_TOKEN=123456789:AAFExampleTokenHereDoNotCopy
MANAGER_IDS=123456789,987654321
```
### Step 5 — Deploy (systemd included)

```
git clone https://github.com/yourname/multi-department-bot.git
cd multi-department-bot
cp .env.example .env
nano .env                    # paste your real token & manager IDs
pip install -r requirements.txt
sudo cp sales-bot.service /etc/systemd/system/
sudo systemctl enable --now sales-bot.service
```
Done! Bot is live 24/7.

## Project Structure

├── bot.py               # main logic (fully commented)

├── .env.example         # template

├── requirements.txt

├── sales-bot.service    # systemd service file

└── README.md            # ← you are here



## Screenshots 

<p align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://github.com/binaryw0rm/Telegram-bot-for-a-few-channels/blob/main/image.JPG?raw=true" width="250"><br>
        <sub>Channel button</sub>
      </td>
      <td align="center">
        <img src="https://github.com/binaryw0rm/Telegram-bot-for-a-few-channels/blob/main/image3.JPG?raw=true" width="250"><br>
        <sub>User welcome</sub>
      </td>
      <td align="center">
        <img src="https://github.com/binaryw0rm/Telegram-bot-for-a-few-channels/blob/main/image2.JPG?raw=true" width="250"><br>
        <sub>Manager notification</sub>
      </td>
    </tr>
  </table>
</p>

---

Author — @binaryw0rm

Available for similar custom bots (100-150$) · DM me on Telegram

Made with love 
