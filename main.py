import logging
import sys
import asyncio
import io
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp.web_fileresponse import content_type
from rembg import remove
from PIL import Image

from config import TOKEN

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    username = message.from_user.username
    await message.answer_sticker("CAACAgIAAxkBAAEx1E5nsvnarsArGA6lEdSG-WuhpDTZUAACMhcAAjIp2ElVz-fxiTWL8zYE")
    await message.answer(
        f"""Hi @{username},
I am a bot created by @java_editi0n.
I can remove the background from your image.
Just send me a photo!"""
    )

# @router.message()
# async def check_photo(message: Message, bot: Bot):
#     if message.photo:
#         photo = message.photo[-1]
#         file_info = await bot.get_file(photo.file_id)
#         file_path = file_info.file_path
#
#         destination = f"photos/{photo.file_id}.jpg"
#         await bot.download(file=photo, destination=destination)
#         await message.reply("Вы отправили фото!")
#
#     else:
#         await message.reply("Это не фото.")

@router.message()
async def remove_bg_handler(message: types.Message, bot: Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path

    image_bytes = await bot.download(file)
    image = Image.open(io.BytesIO(image_bytes.read()))

    output_image = remove(image)

    output_io = io.BytesIO()
    output_image.save(output_io, format="PNG")
    output_io.seek(0)

    await message.answer_photo(types.BufferedInputFile(output_io.getvalue(), filename="output.png"))

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
