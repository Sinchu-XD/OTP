import asyncio
import requests
import json
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
    response = requests.get(url)

    try:
        data = response.json()
        if not data:
            return {}

        country_list = {key: value.get("eng", "Unknown Country") for key, value in data.items()}
        return country_list
    except Exception as e:
        print(f"⚠️ API Error (Countries): {e}")
        return {}


# 📱 Get Available Services (Fixed)
def get_services():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getTopCountriesByService"
    response = requests.get(url)

    try:
        print(f"🔍 API Raw Response: {response.text}")  # Debugging output

        data = response.json()

        if not isinstance(data, dict) or "data" not in data:
            print("⚠️ Unexpected API response format.")
            return {}

        return data["data"]  # Return only the data part

    except json.JSONDecodeError:
        print("⚠️ API Error: Failed to decode JSON.")
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
    services_data = get_services()

    if not services_data:
        await message.reply_text("❌ No services available.")
        return

    try:
        formatted_services = []
        for country_id, country_data in services_data.items():
            country_name = country_data.get("cName", "Unknown Country")
            services_list = country_data.get("services", {})

            if not services_list:
                continue  # Skip empty service lists

            service_names = ", ".join([f"{key}: {value}" for key, value in services_list.items()])
            formatted_services.append(f"**{country_name}**:\n`{service_names}`\n")

        if not formatted_services:
            await message.reply_text("❌ No services found in the API response.")
            return

        services_text = "\n".join(formatted_services)

        await message.reply_text(f"📱 **Available Services:**\n\n{services_text}")

    except Exception as e:
        await message.reply_text(f"⚠️ Error parsing services: {e}")


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
