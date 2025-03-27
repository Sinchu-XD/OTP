import requests
import json
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

    if "ACCESS_BALANCE" in response:
        return response.split(":")[1]  # Extract balance amount
    return f"❌ API Error: {response}"


# 🌍 Get Available Countries
def get_countries():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getCountries"
    response = requests.get(url).text

    try:
        data = json.loads(response)  # Convert to JSON
        return {key: value.get("eng", "Unknown") for key, value in data.items()}
    except json.JSONDecodeError:
        return f"❌ API Error: {response}"


# 📱 Get Available Services (Fully Fixed)
def get_services():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getTopCountriesByService"
    response = requests.get(url).text

    try:
        data = json.loads(response)  # Convert response to JSON
        if not isinstance(data, dict):
            return f"❌ Unexpected API response format: {data}"

        services_list = {}
        for country_id, details in data.items():
            country_name = details.get("cName", "Unknown Country")
            services = details.get("services", {})

            services_list[country_id] = {
                "country": country_name,
                "services": services
            }

        return services_list
    except json.JSONDecodeError:
        return f"❌ API Error: {response}"


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


# 📱 Get Services Command (Fully Fixed)
@app.on_message(filters.command("services"))
async def services(client, message):
    services_data = get_services()

    if isinstance(services_data, str):
        await message.reply_text(services_data)  # API error message
        return

    formatted_services = []
    for country_id, data in services_data.items():
        country_name = data["country"]
        services_list = ", ".join(data["services"].keys()) if data["services"] else "No Services"

        formatted_services.append(f"**{country_name}**:\n`{services_list}`\n")

    services_text = "\n".join(formatted_services)

    # ✅ Ensure message is within Telegram's 4096-character limit
    for chunk in [services_text[i:i + 4000] for i in range(0, len(services_text), 4000)]:
        await message.reply_text(f"📱 **Available Services:**\n\n{chunk}")


# 🌍 Get Countries Command
@app.on_message(filters.command("countries"))
async def countries(client, message):
    countries = get_countries()

    if isinstance(countries, str):
        await message.reply_text(countries)  # API error message
        return

    country_list = "\n".join([f"{key}: {name}" for key, name in countries.items()])
    await message.reply_text(f"🌍 **Available Countries:**\n{country_list}")


# 🚀 Run the bot
print("🔥 OTP Bot is Running...")
app.run()
