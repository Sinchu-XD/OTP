import asyncio
import requests
from pyrogram import Client, filters

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


# 🌍 Get Available Countries (Fixed)
def get_countries():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getCountries"
    response = requests.get(url)

    try:
        data = response.json()
        if not data:
            return {}

        # ✅ Fix KeyError (Use `.get()` to avoid errors)
        country_list = {key: value.get("eng", "Unknown") for key, value in data.items()}
        return country_list
    except Exception as e:
        print(f"⚠️ API Error (Countries): {e}")
        return {}


# 📱 Get Available Services (Fixed)
def get_services():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getTopServices"
    response = requests.get(url)

    try:
        print(f"🔍 API Response (Services): {response.text}")  # ✅ Print full response

        data = response.json()
        if not data:
            print("❌ API returned an empty response.")
            return {}

        service_list = {key: value.get("eng", "Unknown") for key, value in data.items()}
        return service_list
    except Exception as e:
        print(f"⚠️ API Error (Services): {e}")
        return {}



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
"""
    await message.reply_text(help_text)


# 💰 Check Balance Command
@app.on_message(filters.command("balance"))
async def balance(client, message):
    balance = get_balance()
    await message.reply_text(f"💰 **Your Balance:** `{balance} RUB`")


# 📱 Get Services Command (Fixed)
@app.on_message(filters.command("services"))
async def services(client, message):
    services = get_services()
    
    if not services:
        await message.reply_text("❌ No services available.")
        return

    service_list = "\n".join([f"{key}: {name}" for key, name in services.items()])
    await message.reply_text(f"📱 **Available Services:**\n{service_list}")


# 🌍 Get Countries Command (Fixed)
@app.on_message(filters.command("countries"))
async def countries(client, message):
    countries = get_countries()
    
    if not countries:
        await message.reply_text("❌ No countries available.")
        return

    country_list = "\n".join([f"{key}: {name}" for key, name in countries.items()])
    await message.reply_text(f"🌍 **Available Countries:**\n{country_list}")


# 🚀 Run the bot
print("🔥 OTP Bot is Running...")
app.run()
