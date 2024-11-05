import asyncio
import logging
import sys
import uuid
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineQuery, InlineQueryResultVoice, InputFile
from sqlalchemy import select, insert

from converter import convert_mp3_to_ogg
from db import SessionLocal, Voice, engine, Base, User

TOKEN = getenv("BOT_TOKEN")
CHANNEL_ID = getenv("CHANNEL_ID")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, motherfucker!")


@dp.inline_query()
async def inline_query_handler(inline_query: InlineQuery):
    query_text = inline_query.query.strip()  # Get user input
    results = []

    # Establish a session with the database
    async with SessionLocal() as session:
        is_exists = await session.execute(select(User).where(User.tg_id == inline_query.from_user.id))
        is_exists = is_exists.scalar()
        if not is_exists:
            user = {
                "tg_id": inline_query.from_user.id,
                "username": inline_query.from_user.username,
                "full_name": inline_query.from_user.full_name
            }
            await session.execute(insert(User).values(**user))
            await session.commit()

        stmt = select(Voice).where(Voice.name.ilike(f"%{query_text}%")).order_by(Voice.times_used.desc()).limit(10)
        voices = await session.execute(stmt)
        voices = voices.scalars().all()  # Extract result objects

        for voice in voices:
            result_id = str(uuid.uuid4())
            title = voice.name if voice.name else "Untitled Audio"

            result = InlineQueryResultVoice(
                id=result_id,
                voice_url=voice.file_id,
                title=title,  # Ensure title is provided
                caption=f"Times used: {voice.times_used}"  # Optional caption
                )
            results.append(result)

            voice.times_used += 1
            await session.commit()

    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)


@dp.message()
async def store_voice_file_ids(message: Message) -> None:
    if message.from_user.id == 1152654889:
        if message.voice:
            file_id = message.voice.file_id
        elif message.audio:
            audio_file_id = message.audio.file_id
            audio_file = await bot.get_file(audio_file_id)
            file_path = f"{message.audio.file_unique_id}.mp3"
            await bot.download_file(audio_file.file_path, file_path)
            await message.answer(text="Downloaded file, now converting")
            converted_file_path = convert_mp3_to_ogg(file_path)
            voice_message = InputFile(converted_file_path)
            sent_message = await message.answer_voice(voice_message)
            file_id = sent_message.audio.file_id
        else:
            return
        file_name = message.caption

        async with SessionLocal() as session:
            # Check if this file_id already exists in the database
            stmt = select(Voice).where(Voice.file_id == file_id)
            result = await session.execute(stmt)
            audio = result.scalar_one_or_none()

            if not audio:
                # Add a new record if it doesn't exist
                new_audio = Voice(
                    file_id=file_id,
                    name=file_name,
                    times_used=0
                )
                session.add(new_audio)
                await session.commit()
                await message.reply(f"Audio file saved with file_id: {file_id}")
            else:
                await message.reply("This audio file is already in the database.")
    else:
        await message.answer('fuck you bitch')


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())