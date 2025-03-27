import asyncio
import requests
from pyrofork import Client, filters

# ✅ Configuration
API_ID = 25024171
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"
BOT_TOKEN = "7594137088:AAG8jqqkTVGJn2kzICqxdR3vEzd32oY1rk4"
SMS_ACTIVATE_API_KEY = "015912ef48Bed5B702d2e8c9ec044859"

app = Client("OTPBOT", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# 💰 Get Account Balance
def get_balance():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getBalance"
    response = requests.get(url).text
    return response if response else "❌ Failed to fetch balance."


# 🌍 Get Available Countries
def get_countries():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getCountries"
    response = requests.get(url).json()
    return response if response else {}


# 📱 Get Available Services
def get_services():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getServices"
    response = requests.get(url).json()
    return response if response else {}


# 🛒 Buy a Number for OTP
def buy_number(service, country):
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getNumber&service={service}&country={country}"
    response = requests.get(url).text
    if response.startswith("ACCESS_NUMBER"):
        _, activation_id, phone_number = response.split(":")
        return activation_id, phone_number
    return None, None


# 🔄 Check for OTP
def check_otp(activation_id):
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getStatus&id={activation_id}"
    response = requests.get(url).text
    if response.startswith("STATUS_OK"):
        return response.split(":")[1]  # Extract OTP
    return None


# ❌ Cancel Order (If not needed)
def cancel_order(activation_id):
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=setStatus&id={activation_id}&status=8"
    response = requests.get(url).text
    return response


# 🚀 Start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Welcome to OTP Bot! Use /help for available commands.")


# 📖 Help Command
@app.on_message(filters.command("help"))
async def help(client, message):
    help_text = """
🛠 **Available Commands:**
/balance - 💰 Check account balance
/services - 📱 Get available services
/countries - 🌍 Get available countries
/buy <service_id> <country_id> - 🛒 Buy a number
/checkotp <activation_id> - 🔑 Check OTP
/cancel <activation_id> - ❌ Cancel order
"""
    await message.reply_text(help_text)


# 💰 Check Balance Command
@app.on_message(filters.command("balance"))
async def balance(client, message):
    balance = get_balance()
    await message.reply_text(f"💰 **Your Balance:** `{balance} RUB`")


# 📱 Get Services Command
@app.on_message(filters.command("services"))
async def services(client, message):
    services = get_services()
    if not services:
        await message.reply_text("❌ No services available.")
        return

    service_list = "\n".join([f"{key}: {value['russian']}" for key, value in services.items()])
    await message.reply_text(f"📱 **Available Services:**\n{service_list}")


# 🌍 Get Countries Command
@app.on_message(filters.command("countries"))
async def countries(client, message):
    countries = get_countries()
    if not countries:
        await message.reply_text("❌ No countries available.")
        return

    country_list = "\n".join([f"{key}: {value['russian']}" for key, value in countries.items()])
    await message.reply_text(f"🌍 **Available Countries:**\n{country_list}")


# 🛒 Buy a Number Command
@app.on_message(filters.command("buy"))
async def buy_number_command(client, message):
    try:
        args = message.text.split()

        # 🛑 Ensure correct command format
        if len(args) != 3:
            await message.reply_text("⚠️ Usage: `/buy <service_id> <country_id>`\nExample: `/buy vk 6`")
            return

        _, service_id, country_id = args  # ✅ Unpack properly
        activation_id, phone_number = buy_number(service_id, country_id)

        if activation_id:
            await message.reply_text(f"✅ **Number Purchased:** `{phone_number}`\n📩 **Waiting for OTP...**\n\nUse `/checkotp {activation_id}` to check OTP.")
        else:
            await message.reply_text("❌ Failed to buy a number. Try again later.")

    except Exception as e:
        await message.reply_text(f"⚠️ **Error:** `{e}`")


# 🔄 Check OTP Command
@app.on_message(filters.command("checkotp"))
async def check_otp_command(client, message):
    try:
        args = message.text.split()

        # 🛑 Ensure correct command format
        if len(args) != 2:
            await message.reply_text("⚠️ Usage: `/checkotp <activation_id>`\nExample: `/checkotp 123456`")
            return

        _, activation_id = args  # ✅ Unpack properly
        otp = check_otp(activation_id)

        if otp:
            await message.reply_text(f"🔑 **OTP Received:** `{otp}`")
        else:
            await message.reply_text("⏳ OTP not received yet. Try again later.")

    except Exception as e:
        await message.reply_text(f"⚠️ **Error:** `{e}`")


# ❌ Cancel Order Command
@app.on_message(filters.command("cancel"))
async def cancel_command(client, message):
    try:
        args = message.text.split()

        # 🛑 Ensure correct command format
        if len(args) != 2:
            await message.reply_text("⚠️ Usage: `/cancel <activation_id>`\nExample: `/cancel 123456`")
            return

        _, activation_id = args  # ✅ Unpack properly
        response = cancel_order(activation_id)

        if response == "ACCESS_CANCEL":
            await message.reply_text(f"✅ **Order Cancelled:** `{activation_id}`")
        else:
            await message.reply_text(f"❌ **Failed to cancel order.** Response: `{response}`")

    except Exception as e:
        await message.reply_text(f"⚠️ **Error:** `{e}`")


# 🚀 Run the bot
print("🔥 OTP Bot is Running...")
app.run()
