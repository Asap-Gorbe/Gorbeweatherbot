from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import requests
from datetime import datetime

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '7407643213:AAHUshpeAYZQAM34SmdrkR2BNvMWeKzgq4U'

# Define constants for user_data keys
WAITING_FOR_LOCATION = 'waiting_for_location'
REQUESTED_FEATURE = 'requested_feature'

# Feature identifiers
FEATURE_SEVEN_DAY_FORECAST = 'seven_day_forecast'
FEATURE_TEMPERATURE = 'temperature'
FEATURE_HUMIDITY = 'humidity'
FEATURE_WIND_SPEED = 'wind_speed'
FEATURE_RAIN = 'rain'


LOCAL_IMAGE_PATH_W =r"C:\Users\NoteBook\Pictures\Weather bot\Design 8.png"    # Weather
LOCAL_IMAGE_PATH_WI =r"C:\Users\NoteBook\Pictures\Weather bot\Design 9.png"   # Wind
LOCAL_IMAGE_PATH_H = r"C:\Users\NoteBook\Pictures\Weather bot\Design 10.png"   # Humidity
LOCAL_IMAGE_PATH_R = r"C:\Users\NoteBook\Pictures\Weather bot\Design 11.png"  # Rain



# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Get Weather", callback_data='weather')],
        [InlineKeyboardButton("Get Humidity", callback_data='humidity')],
        [InlineKeyboardButton("Get Wind Speed", callback_data='wind')],
        [InlineKeyboardButton("Check Rain Forecast", callback_data='rain')],
        [InlineKeyboardButton("Get Seven Day Forecast", callback_data='seven_day_forecast')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Welcome! Choose an option below:',
        reply_markup=reply_markup
    )


# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'weather':
        await weather_command(query, context)
    elif query.data == 'humidity':
        await humidity_command(query, context)
    elif query.data == 'wind':
        await wind_command(query, context)
    elif query.data == 'rain':
        await rain_command(query, context)
    elif query.data == 'seven_day_forecast':
        await seven_day_forecast(query, context)


# Weather command
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    if latitude is None or longitude is None:
        # Ask for location
        context.user_data[WAITING_FOR_LOCATION] = True
        context.user_data[REQUESTED_FEATURE] = FEATURE_TEMPERATURE
        location_keyboard = [[KeyboardButton("Send Location", request_location=True)],
                             [KeyboardButton("Enter Custom Location")]]
        reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
        await update.message.reply_text('Please share your location to get the weather update.', reply_markup=reply_markup)
    else:
        # Handle weather request
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(api_url)
        data = response.json()

        # Check if temperature exists in the response
        if 'temperature' in data['current_weather']:
            current_temp = data['current_weather']['temperature']
            weather_message = f"The current temperature is {current_temp}°C."
        else:
            weather_message = "Sorry, temperature data is not available for the provided location."

        # Send weather image and message
        with open(LOCAL_IMAGE_PATH_W, 'rb') as image_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_file,
                caption=weather_message
            )
            keyboard = [
                [InlineKeyboardButton("Get Weather", callback_data='weather')],
                [InlineKeyboardButton("Get Humidity", callback_data='humidity')],
                [InlineKeyboardButton("Get Wind Speed", callback_data='wind')],
                [InlineKeyboardButton("Check Rain Forecast", callback_data='rain')],
                [InlineKeyboardButton("Get Seven Day Forecast", callback_data='seven_day_forecast')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                'Need any thing else ?',
                reply_markup=reply_markup
            )

# Humidity command
async def humidity_command(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    if latitude is None or longitude is None:
        context.user_data[WAITING_FOR_LOCATION] = True
        context.user_data[REQUESTED_FEATURE] = FEATURE_HUMIDITY
        location_keyboard = [[KeyboardButton("Send Location", request_location=True)],
                             [KeyboardButton("Enter Custom Location")]]
        reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
        await update.message.reply_text('Please share your location to get the humidity data.', reply_markup=reply_markup)
    else:
        # Handle humidity request
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(api_url)
        data = response.json()

        # Check if 'humidity' exists in the response
        if 'humidity' in data['current_weather']:
            humidity = data['current_weather']['humidity']
            humidity_message = f"The current humidity is {humidity}%."
        else:
            humidity_message = "Sorry, humidity data is not available for the provided location."

        # Send the humidity image and message
        with open(LOCAL_IMAGE_PATH_H, 'rb') as image_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_file,
                caption=humidity_message
            )
            keyboard = [
                [InlineKeyboardButton("Get Weather", callback_data='weather')],
                [InlineKeyboardButton("Get Humidity", callback_data='humidity')],
                [InlineKeyboardButton("Get Wind Speed", callback_data='wind')],
                [InlineKeyboardButton("Check Rain Forecast", callback_data='rain')],
                [InlineKeyboardButton("Get Seven Day Forecast", callback_data='seven_day_forecast')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                'Need any thing else ?',
                reply_markup=reply_markup
            )

# Wind speed command
async def wind_command(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    if latitude is None or longitude is None:
        context.user_data[WAITING_FOR_LOCATION] = True
        context.user_data[REQUESTED_FEATURE] = FEATURE_WIND_SPEED
        location_keyboard = [[KeyboardButton("Send Location", request_location=True)],
                             [KeyboardButton("Enter Custom Location")]]
        reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
        await update.message.reply_text('Please share your location to get the wind speed data.', reply_markup=reply_markup)
    else:
        # Handle wind speed request
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(api_url)
        data = response.json()

        # Check if 'windspeed' exists in the response
        if 'windspeed' in data['current_weather']:
            wind_speed = data['current_weather']['windspeed']
            wind_message = f"The current wind speed is {wind_speed} m/s."
        else:
            wind_message = "Sorry, wind speed data is not available for the provided location."

        # Send wind image and message
        with open(LOCAL_IMAGE_PATH_WI, 'rb') as image_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_file,
                caption=wind_message
            )
            keyboard = [
                [InlineKeyboardButton("Get Weather", callback_data='weather')],
                [InlineKeyboardButton("Get Humidity", callback_data='humidity')],
                [InlineKeyboardButton("Get Wind Speed", callback_data='wind')],
                [InlineKeyboardButton("Check Rain Forecast", callback_data='rain')],
                [InlineKeyboardButton("Get Seven Day Forecast", callback_data='seven_day_forecast')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                'Need any thing else ?',
                reply_markup=reply_markup
            )

# Rain forecast command
async def rain_command(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    if latitude is None or longitude is None:
        context.user_data[WAITING_FOR_LOCATION] = True
        context.user_data[REQUESTED_FEATURE] = FEATURE_RAIN
        location_keyboard = [[KeyboardButton("Send Location", request_location=True)],
                             [KeyboardButton("Enter Custom Location")]]
        reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
        await update.message.reply_text('Please share your location to check the rain forecast.', reply_markup=reply_markup)
    else:
        # Handle rain forecast request
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=auto"
        response = requests.get(api_url)
        data = response.json()

        # Check if 'precipitation_sum' exists in the response
        if 'precipitation_sum' in data['daily']:
            rain_forecast = data['daily']['precipitation_sum'][0]
            rain_message = f"The forecasted rain for today is {rain_forecast} mm."
        else:
            rain_message = "Sorry, rain data is not available for the provided location."

        # Send rain image and message
        with open(LOCAL_IMAGE_PATH_R, 'rb') as image_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_file,
                caption=rain_message
            )
            keyboard = [
                [InlineKeyboardButton("Get Weather", callback_data='weather')],
                [InlineKeyboardButton("Get Humidity", callback_data='humidity')],
                [InlineKeyboardButton("Get Wind Speed", callback_data='wind')],
                [InlineKeyboardButton("Check Rain Forecast", callback_data='rain')],
                [InlineKeyboardButton("Get Seven Day Forecast", callback_data='seven_day_forecast')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                'Need any thing else ?',
                reply_markup=reply_markup
            )

# 7 day forecast command
async def seven_day_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude=None, longitude=None) -> None:
    if latitude is None or longitude is None:
        context.user_data[WAITING_FOR_LOCATION] = True
        context.user_data[REQUESTED_FEATURE] = FEATURE_SEVEN_DAY_FORECAST
        location_keyboard = [[KeyboardButton("Send Location", request_location=True)],
                             [KeyboardButton("Enter Custom Location")]]
        reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
        await update.message.reply_text('Please share your location to get a seven-day forecast.',
                                        reply_markup=reply_markup)
    else:
        await handle_seven_day_forecast(update, context, latitude, longitude)


# Location handler
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get(WAITING_FOR_LOCATION):
        context.user_data[WAITING_FOR_LOCATION] = False
        user_location = update.message.location
        latitude = user_location.latitude
        longitude = user_location.longitude

        requested_feature = context.user_data.get(REQUESTED_FEATURE)

        if requested_feature == FEATURE_TEMPERATURE:
            await weather_command(update, context, latitude, longitude)
        elif requested_feature == FEATURE_HUMIDITY:
            await humidity_command(update, context, latitude, longitude)
        elif requested_feature == FEATURE_WIND_SPEED:
            await wind_command(update, context, latitude, longitude)
        elif requested_feature == FEATURE_RAIN:
            await rain_command(update, context, latitude, longitude)
        elif requested_feature == FEATURE_SEVEN_DAY_FORECAST:
            await handle_seven_day_forecast(update, context, latitude, longitude)


# Example function to handle the seven-day forecast
async def handle_seven_day_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE, latitude: float,
                                    longitude: float) -> None:
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    response = requests.get(api_url)
    data = response.json()

    forecast_data = data['daily']
    dates = forecast_data['time']
    temp_max = forecast_data['temperature_2m_max']
    temp_min = forecast_data['temperature_2m_min']

    forecast_message = "7-Day Forecast:\n"
    for date, max_temp, min_temp in zip(dates, temp_max, temp_min):
        forecast_message += f"{date}: Max Temp: {max_temp}°C, Min Temp: {min_temp}°C\n"

    with open(LOCAL_IMAGE_PATH_W, 'rb') as image_file:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image_file,
            caption=forecast_message
        )
        keyboard = [
            [InlineKeyboardButton("Get Weather", callback_data='weather')],
            [InlineKeyboardButton("Get Humidity", callback_data='humidity')],
            [InlineKeyboardButton("Get Wind Speed", callback_data='wind')],
            [InlineKeyboardButton("Check Rain Forecast", callback_data='rain')],
            [InlineKeyboardButton("Get Seven Day Forecast", callback_data='seven_day_forecast')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            'Need any thing else ?',
            reply_markup=reply_markup
        )

# Main function
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))  # Handle button clicks
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("humidity", humidity_command))
    application.add_handler(CommandHandler("wind", wind_command))
    application.add_handler(CommandHandler("rain", rain_command))
    application.add_handler(CommandHandler('forecast', seven_day_forecast))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))

    application.run_polling()


if __name__ == '__main__':
    print('on')
    main()
