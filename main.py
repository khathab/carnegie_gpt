import logging
import asyncio
import sys
from config import dp, router, bot
import app
async def main() -> None:
    dp.include_router(router=router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
