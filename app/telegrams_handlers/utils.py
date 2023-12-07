from aiogram import types
import os

async def download_media(message: types.Message, media) -> str:
    """
    Download a media file and save it in the specified directory.
    """
    
    # Determine file extension based on media type
    if isinstance(media, types.Voice):
        extension = "mp3" 
    elif isinstance(media, types.PhotoSize):
        extension = "jpg"
    else:
        extension = "dat"
    
    # Get file info
    file_info = await message.bot.get_file(media.file_id)
    
    # Prepare local directory and path
    local_dir = f"static/users/{message.chat.id}"
    local_path = os.path.join(local_dir, f"{media.file_unique_id}.{extension}")

    # Ensure directory exists
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Download the file
    await message.bot.download_file(file_info.file_path, local_path)
    return local_path