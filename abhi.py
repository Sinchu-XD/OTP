import requests
from pyrofork import Client, filters

# ✅ Configuration
API_ID = 25024171
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"
BOT_TOKEN = "7594137088:AAG8jqqkTVGJn2kzICqxdR3vEzd32oY1rk4"
SMS_ACTIVATE_API_KEY = "015912ef48Bed5B702d2e8c9ec044859"

app = Client("OTPBOT", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🌍 Get Available Countries
def get_countries():
    url = f"https://sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getCountries"
    response = requests.get(url).json()
    return response.get("countries", {})

# 📱 Get Available Services
def get_services():
    url = f"https://sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getTopServices"
    response = requests.get(url).json()
    return response.get("top_services", {})

# 🛒 Buy a Number for OTP
def buy_number(service, country):
    url = f"https://sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getNumber&service={service}&country={country}"
    response = requests.get(url).text
    if response.startswith("ACCESS_NUMBER"):
        _, activation_id, phone_number = response.split(":")
        return activation_id, phone_number
    return None, None

# 🔄 Check for OTP
def check_otp(activation_id):
    url = f"https://sms-activate.org/stubs/handler_api.php?api_key={SMS_ACTIVATE_API_KEY}&action=getStatus&id={activation_id}"
    response = requests.get(url).text
    if response.startswith("STATUS_OK"):
        return response.split(":")[1]  # Extract OTP
    return None

# 🚀 Start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Welcome to OTP Bot!\nUse /getotp to receive OTPs.")

# 📲 Get OTP Command
@app.on_message(filters.command("getotp"))
async def getotp(client, message):
    countries = get_countries()
    services = get_services()
    
    country_list = "\n".join([f"{key}: {value['rus']}" for key, value in countries.items()])
    service_list = "\n".join([f"{key}: {value['en']}" for key, value in services.items()])
    
    await message.reply_text(f"🌍 **Available Countries:**\n{country_list}\n\n📱 **Available Services:**\n{service_list}\n\nSend `/buy <service_id> <country_id>` to get a number.")

# 🛒 Buy a Number Command
@app.on_message(filters.command("buy"))
async def buy_number_command(client, message):
    try:
        _, service_id, country_id = message.text.split()
        activation_id, phone_number = buy_number(service_id, country_id)
        
        if activation_id:
            await message.reply_text(f"✅ Number Purchased: `{phone_number}`\n📩 Waiting for OTP...\n\nUse `/checkotp {activation_id}` to check OTP.")
        else:
            await message.reply_text("❌ Failed to buy number. Try again.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")

# 🔄 Check OTP Command
@app.on_message(filters.command("checkotp"))
async def check_otp_command(client, message):
    try:
        _, activation_id = message.text.split()
        otp = check_otp(activation_id)
        
        if otp:
            await message.reply_text(f"🔑 OTP Received: `{otp}`")
        else:
            await message.reply_text("⏳ OTP not received yet. Try again later.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")

# 🚀 Run the bot
print("🔥 OTP Bot is Running...")
app.run()
