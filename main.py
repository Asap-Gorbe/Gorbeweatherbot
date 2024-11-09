from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import requests
import sqlite3
from Token import API_KEY_TEST

TOKEN = API_KEY_TEST

# Define constants for user_data keys
WAITING_FOR_LOCATION = 'waiting_for_location'
REQUESTED_FEATURE = 'requested_feature'

# Feature identifiers
FEATURE_SEVEN_DAY_FORECAST = 'seven_day_forecast'
FEATURE_TEMPERATURE = 'temperature'
FEATURE_HUMIDITY = 'humidity'
FEATURE_WIND_SPEED = 'wind_speed'
FEATURE_RAIN = 'rain'

# Local image paths for visual responses
LOCAL_IMAGE_PATH_W = r"C:\Users\NoteBook\Pictures\Weather bot\Design 8.png"  # Weather
LOCAL_IMAGE_PATH_WI = r"C:\Users\NoteBook\Pictures\Weather bot\Design 9.png"  # Wind
LOCAL_IMAGE_PATH_H = r"C:\Users\NoteBook\Pictures\Weather bot\Design 10.png"  # Humidity
LOCAL_IMAGE_PATH_R = r"C:\Users\NoteBook\Pictures\Weather bot\Design 11.png"  # Rain


# Database setup
def initialize_database():
    """Initialize the database with a user_locations table if it doesn't exist."""
    with sqlite3.connect('gorbe_weather.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_locations(
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        user_first_name TEXT,
                        user_last_name TEXT,
                        longitude REAL,
                        latitude REAL
                    )''')
        conn.commit()


initialize_database()

        # added first_name , last_name , username

# Save user location to database
def save_location(user_id: int,username: str,user_first_name:str,user_last_name: str, longitude: float, latitude: float):
    """Save or update user location in the database."""
    with sqlite3.connect('gorbe_weather.db') as conn:
        c = conn.cursor()
        c.execute('''
             INSERT INTO user_locations (user_id, longitude, latitude, first_name, last_name, username)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET 
                latitude = excluded.latitude, 
                longitude = excluded.longitude, 
                first_name = excluded.first_name, 
                last_name = excluded.last_name, 
                username = excluded.username
          ''', (user_id, longitude, latitude, user_first_name, user_last_name, username))
        conn.commit()
        



# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command to provide users with feature options."""
    keyboard = [
        [InlineKeyboardButton("Get Weather", callback_data='weather')],
        [InlineKeyboardButton("Get Humidity", callback_data='humidity')],
        [InlineKeyboardButton("Get Wind Speed", callback_data='wind')],
        [InlineKeyboardButton("Check Rain Forecast", callback_data='rain')],
        [InlineKeyboardButton("Get Seven Day Forecast", callback_data='seven_day_forecast')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Choose an option below:', reply_markup=reply_markup)


# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks and call relevant commands."""
    query = update.callback_query
    await query.answer()
    feature_map = {
        'weather': weather_command,
        'humidity': humidity_command,
        'wind': wind_command,
        'rain': rain_command,
        'seven_day_forecast': seven_day_forecast
    }
    await feature_map[query.data](update, context)


# Weather command
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    """Fetch and send the current weather based on location."""
    if not latitude or not longitude:
        await request_location(update, context, FEATURE_TEMPERATURE, 'weather update')
        return

    try:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(api_url)
        data = response.json()

        current_temp = data['current_weather'].get('temperature')
        weather_message = f"The current temperature is {current_temp}°C." if current_temp else "Temperature data unavailable."

        await send_image_with_message(update, context, LOCAL_IMAGE_PATH_W, weather_message)
    except (requests.RequestException, KeyError) as e:
        await update.message.reply_text("Failed to retrieve weather data. Please try again later.")


# Humidity command
async def humidity_command(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    """Fetch and send the humidity data based on location."""
    if not latitude or not longitude:
        await request_location(update, context, FEATURE_HUMIDITY, 'humidity data')
        return

    try:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(api_url)
        data = response.json()

        humidity = data['current_weather'].get('humidity')
        humidity_message = f"The current humidity is {humidity}%." if humidity else "Humidity data unavailable."

        await send_image_with_message(update, context, LOCAL_IMAGE_PATH_H, humidity_message)
    except (requests.RequestException, KeyError) as e:
        await update.message.reply_text("Failed to retrieve humidity data. Please try again later.")


# Wind speed command
async def wind_command(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    """Fetch and send the wind speed data based on location."""
    if not latitude or not longitude:
        await request_location(update, context, FEATURE_WIND_SPEED, 'wind speed data')
        return

    try:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(api_url)
        data = response.json()

        wind_speed = data['current_weather'].get('windspeed')
        wind_message = f"The current wind speed is {wind_speed} m/s." if wind_speed else "Wind speed data unavailable."

        await send_image_with_message(update, context, LOCAL_IMAGE_PATH_WI, wind_message)
    except (requests.RequestException, KeyError) as e:
        await update.message.reply_text("Failed to retrieve wind speed data. Please try again later.")


# Rain forecast command
async def rain_command(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    """Fetch and send the rain forecast based on location."""
    if not latitude or not longitude:
        await request_location(update, context, FEATURE_RAIN, 'rain forecast')
        return

    try:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=auto"
        response = requests.get(api_url)
        data = response.json()

        rain_forecast = data['daily']['precipitation_sum'][0] if 'precipitation_sum' in data['daily'] else None
        rain_message = f"The forecasted rain for today is {rain_forecast} mm." if rain_forecast else "Rain forecast data unavailable."

        await send_image_with_message(update, context, LOCAL_IMAGE_PATH_R, rain_message)
    except (requests.RequestException, KeyError) as e:
        await update.message.reply_text("Failed to retrieve rain forecast data. Please try again later.")


# 7-day forecast command
async def seven_day_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    """Fetch and send a seven-day forecast based on location."""
    if not latitude or not longitude:
        await request_location(update, context, FEATURE_SEVEN_DAY_FORECAST, 'seven-day forecast')
        return

    try:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        response = requests.get(api_url)
        data = response.json()

        dates = data['daily']['time']
        temp_max = data['daily']['temperature_2m_max']
        temp_min = data['daily']['temperature_2m_min']

        forecast_message = "7-Day Forecast:\n" + "\n".join(
            f"{date}: Max Temp: {max_temp}°C, Min Temp: {min_temp}°C"
            for date, max_temp, min_temp in zip(dates, temp_max, temp_min)
        )

        await send_image_with_message(update, context, LOCAL_IMAGE_PATH_W, forecast_message)
    except (requests.RequestException, KeyError) as e:
        await update.message.reply_text("Failed to retrieve seven-day forecast data. Please try again later.")


# Request location from user
async def request_location(update: Update, context: ContextTypes.DEFAULT_TYPE, feature, purpose):
    """Prompt the user to share location for a specific feature."""
    context.user_data[WAITING_FOR_LOCATION] = True
    context.user_data[REQUESTED_FEATURE] = feature
    location_keyboard = [[KeyboardButton("Send Location", request_location=True)]]#,
                        # [KeyboardButton("Enter Custom Location")]]
    reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)

    # Use the correct message context based on whether the request was made via button or command
    if update.message:
        await update.message.reply_text(f"Please share your location to get the {purpose}.", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(f"Please share your location to get the {purpose}.",
                                                       reply_markup=reply_markup)


# Send an image with a message
async def send_image_with_message(update: Update, context: ContextTypes.DEFAULT_TYPE, image_path, message):
    """Send an image with a message and follow-up keyboard options."""
    with open(image_path, 'rb') as image_file:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image_file,
            caption=message
        )
        await send_follow_up_options(update)


# Send follow-up keyboard options
async def send_follow_up_options(update: Update):
    """Provide users with follow-up options after each response."""
    keyboard = [
        [InlineKeyboardButton("Get Weather", callback_data='weather')],
        [InlineKeyboardButton("Get Humidity", callback_data='humidity')],
        [InlineKeyboardButton("Get Wind Speed", callback_data='wind')],
        [InlineKeyboardButton("Check Rain Forecast", callback_data='rain')],
        [InlineKeyboardButton("Get Seven Day Forecast", callback_data='seven_day_forecast')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Need anything else?', reply_markup=reply_markup)


# Location handler
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user's location input and call the appropriate command."""
    if context.user_data.get(WAITING_FOR_LOCATION):
        context.user_data[WAITING_FOR_LOCATION] = False
        user_location = update.message.location
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        user_first_name = update.message.from_user.first_name
        user_last_name = update.message.from_user.last_name
        print(f'{user_id} , {username} , {user_first_name} , {user_last_name}')
        latitude, longitude = user_location.latitude, user_location.longitude

        # Save user location
        save_location(user_id,username,user_first_name,user_last_name, latitude, longitude)

        # Redirect to the requested feature
        requested_feature = context.user_data.get(REQUESTED_FEATURE)
        feature_map = {
            FEATURE_TEMPERATURE: weather_command,
            FEATURE_HUMIDITY: humidity_command,
            FEATURE_WIND_SPEED: wind_command,
            FEATURE_RAIN: rain_command,
            FEATURE_SEVEN_DAY_FORECAST: seven_day_forecast
        }
        await feature_map[requested_feature](update, context, latitude, longitude)


# Error handler to capture unexpected errors
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and send a friendly message to the user."""
    print(f"Update {update} caused error {context.error}")
    if update.callback_query:
        await update.callback_query.message.reply_text("An unexpected error occurred. Please try again later.")
    elif update.message:
        await update.message.reply_text("An unexpected error occurred. Please try again later.")


# Main function
def main() -> None:
    """Start the Telegram bot and set up command handlers."""
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))

    # Register error handler
    application.add_error_handler(error_handler)

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    print('BOT is running locally')

    main()
