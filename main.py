from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from datetime import datetime, timedelta
from main import FEATURE_WIND_SPEED, FEATURE_RAIN

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '7407643213:AAHUshpeAYZQAM34SmdrkR2BNvMWeKzgq4U'

# Define constants for user_data keys
WAITING_FOR_LOCATION = 'waiting_for_location'
REQUESTED_FEATURE = 'requested_feature'

# Feature identifiers
FEATURE_TEMPERATURE = 'temperature'
FEATURE_HUMIDITY = 'humidity'
FEATURE_WIND_SPEED ='wind_speed'
FEATURE_RAIN = 'rain'
# Local image path (Replace this with your actual file path)
LOCAL_IMAGE_PATH_W = r"C:\Users\NoteBook\Pictures\Weather bot\Design 8.png"
LOCAL_IMAGE_PATH_WI =r"C:\Users\NoteBook\Pictures\Weather bot\Design 9.png"
LOCAL_IMAGE_PATH_H =r"C:\Users\NoteBook\Pictures\Weather bot\Design 10.png"
LOCAL_IMAGE_PATH_R =r"C:\Users\NoteBook\Pictures\Weather bot\Design 11.png"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Welcome! Use /weather to get the weather update.'
    )


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[WAITING_FOR_LOCATION] = True
    context.user_data[REQUESTED_FEATURE] = FEATURE_TEMPERATURE

    location_keyboard = [[KeyboardButton("Send Location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Please share your location to get the weather update.', reply_markup=reply_markup)


async def humidity_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[WAITING_FOR_LOCATION] = True
    context.user_data[REQUESTED_FEATURE] = FEATURE_HUMIDITY

    location_keyboard = [[KeyboardButton("Send Location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Please share your location to get the humidity data.', reply_markup=reply_markup)


async def wind_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[WAITING_FOR_LOCATION] = True
    context.user_data[REQUESTED_FEATURE] = FEATURE_WIND_SPEED

    location_keyboard = [[KeyboardButton("Send Location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Please share your location to get the wind speed data.', reply_markup=reply_markup)


async def rain_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[WAITING_FOR_LOCATION] = True
    context.user_data[REQUESTED_FEATURE] = FEATURE_RAIN

    location_keyboard = [[KeyboardButton("Send Location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Please share your location to check the rain forecast.', reply_markup=reply_markup)



async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get(WAITING_FOR_LOCATION):
        context.user_data[WAITING_FOR_LOCATION] = False

        user_location = update.message.location
        latitude = user_location.latitude
        longitude = user_location.longitude

        requested_feature = context.user_data.get(REQUESTED_FEATURE)

        if requested_feature == FEATURE_TEMPERATURE:
            api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&forecast_days=1"
            response = requests.get(api_url)
            data = response.json()
            temperature = data['hourly']['temperature_2m'][0]

            # Open the local image file and send it
            with open(LOCAL_IMAGE_PATH_W, 'rb') as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=f'The current temperature at your location is {temperature}°C.'
                )
        elif requested_feature == FEATURE_HUMIDITY:
            api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=relative_humidity_2m&forecast_days=1"
            response = requests.get(api_url)
            data = response.json()
            humidity = data['hourly']['relative_humidity_2m'][0]

            with open(LOCAL_IMAGE_PATH_H, 'rb') as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=f'The current humidity at your location is {humidity}%.'
                )
        elif requested_feature == FEATURE_WIND_SPEED:
            api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=wind_speed_10m&forecast_days=1"
            response = requests.get(api_url)
            data = response.json()
            wind_speed = data['hourly']['wind_speed_10m'][0]

            with open(LOCAL_IMAGE_PATH_WI, 'rb') as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=f'The current wind speed at your location is {wind_speed}km/h.'
                )

        elif requested_feature == FEATURE_RAIN:
            api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&forecast_days=7"
            response = requests.get(api_url)
            data = response.json()

            rain_data = data['hourly']['rain']
            timestamps = data['hourly']['time']

            # Initialize dictionary to store rain data by date
            rain_forecast = {}

            # Loop through the rain data and aggregate by day
            for i, rain_amount in enumerate(rain_data):
                if rain_amount > 0:
                    date_str = timestamps[i][:10]  # Extract the date part from the timestamp
                    if date_str not in rain_forecast:
                        rain_forecast[date_str] = 0
                    rain_forecast[date_str] += rain_amount

            # Generate the response message based on the rain forecast
            if rain_forecast:
                response_message = "It's going to rain on the following days:\n"
                for date, total_rain in rain_forecast.items():
                    date_obj = datetime.strptime(date, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%A, %B %d')
                    response_message += f"{formatted_date}: {total_rain:.2f} mm of rain.\n"
                    with open(LOCAL_IMAGE_PATH_R, 'rb') as image_file:
                        await context.bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=image_file,
                            caption=f"{formatted_date}: {total_rain:.2f} mm of rain.\n"
                        )
            else:
                response_message = "No rain is expected in the next week."
                with open(LOCAL_IMAGE_PATH_R, 'rb') as image_file:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=image_file,
                        caption="No rain is expected in the next week."
                    )
            await update.message.reply_text(response_message)

        else:
            await update.message.reply_text(
                "Please use the /weather, /humidity, /wind, or /rain command first to request an update.")
    else:
        await update.message.reply_text(
            "Please use the /weather, /humidity, /wind, or /rain command first to request an update.")


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("humidity", humidity_command))
    application.add_handler(CommandHandler("wind", wind_command))
    application.add_handler(CommandHandler("rain", rain_command))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))

    application.run_polling()


if __name__ == '__main__':
    print('Bot is running...')
    main()

