from . import dp, API_TOKEN, bot
from aiogram import types
import aiohttp


API_LINK = 'http://django:8000/bot'
IMAGE_API_LINK = 'http://django:8000/bot/image'

@dp.message_handler(content_types=types.ContentType.TEXT)
async def main_command(message: types.Message):
    async with aiohttp.ClientSession() as session:
        data = {'id': message.from_user.username,
                'message': message.text}
        async with session.post(API_LINK, json=data) as response:
            result = await response.json()
    print(result)
    answer = result['response']
    await message.reply(answer)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def main_command(message: types.Message):
    async with aiohttp.ClientSession() as session:
        photo_file_id = message.photo[-1].file_id

        file = await bot.get_file(photo_file_id)

        photo_path = file.file_path
        photo_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{photo_path}'

        async with session.get(photo_url) as response_1:
            # Read the image data
            image_data = await response_1.read()

            # Send the image data to the API
            data = {'id': message.from_user.username,
                    'image': image_data}
            async with session.post(IMAGE_API_LINK, data=data) as response:
                result = await response.json()

    print(result)
    answer = result['response']
    await message.reply(answer)
