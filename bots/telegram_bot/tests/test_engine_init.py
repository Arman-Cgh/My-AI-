import sys
import os
import asyncio


# اضافه کردن Root پروژه به Python Path
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)


from services.ai.engine import AIEngine



async def main():

    engine = AIEngine()

    await engine.initialize()

    print("ENGINE INITIALIZE OK")



asyncio.run(main())