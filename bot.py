import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

"""Globals"""
token = "token"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}!")
    await message.answer("Доступные команды: /weather (погода в Тюмени на текущий момент).")


@dp.message(Command("weather"))
async def weather(message: types.Message):
    key = "b33823ba5c311e5dc4f1d6b1212be3ee"

    # Latitude and Longitude from Geocoding API
    geocode_response = \
        requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q=Tyumen&limit=5&appid={key}").json()[0]
    lat = geocode_response["lat"]
    lon = geocode_response["lon"]

    # Request to OpenWeatherApi and response
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}").json()

    # Extraction data from response to answer
    weather_data = response["weather"]
    description = weather_data[0]["description"]

    main_data = response["main"]
    temp = main_data["temp"] - 273.15
    feels_like = main_data["feels_like"] - 273.15

    await message.answer(f"Температура: {temp:0.0f}°C"
                         f"\nЧувствуется как {feels_like:0.0f}°C"
                         f"\nОписание: {description}")


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
