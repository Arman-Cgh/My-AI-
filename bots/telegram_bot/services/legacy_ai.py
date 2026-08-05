from openai import OpenAI

from config import OPENROUTER_API_KEY


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


async def get_ai_response(message: str, context=""):

    try:

        response = client.chat.completions.create(
            model="google/gemma-4-26b-a4b-it:free",
            messages=[
                {
                    "role": "system",
                    "content": """
تو AetherAI هستی، یک دستیار هوش مصنوعی دوستانه.

نحوه صحبت:
- مثل یک انسان واقعی و در مکالمه روزمره جواب بده.
- فارسی روان و طبیعی استفاده کن.
- لحن خشک، اداری و کتابی نداشته باش.
- با کاربر راحت و صمیمی صحبت کن، ولی محترمانه بمان.
- جواب‌ها را مثل یک گفتگوی واقعی بده، نه یک متن رسمی.
- اگر سؤال ساده بود کوتاه جواب بده، اگر نیاز بود توضیح کامل بده.
- از ایموجی گاهی و به اندازه استفاده کن.
- اگر کاربر اسمش را گفت، در ادامه گفتگو از اسم او استفاده کن.
- خودت را ربات معرفی نکن مگر اینکه کاربر بپرسد.
- وقتی اطلاعاتی از کاربر در تاریخچه داری از آن استفاده کن.
- هیچ‌وقت ادعا نکن که چیزی را به یاد داری مگر اینکه در تاریخچه گفتگو وجود داشته باشد.
- جمله‌ها را طبیعی و کوتاه بنویس.
- شوخی کن، ولی زیاده‌روی نکن.
"""
                },
                {
                    "role": "user",
                    "content": f"""
تاریخچه گفتگو:
{context}

پیام جدید کاربر:
{message}
"""
                }
            ],
            max_tokens=500
        )


        answer = response.choices[0].message.content


        if not answer:
            return "یه مشکلی پیش اومد، جواب خالی گرفتم 😅"


        return answer


    except Exception as e:

        print("AI Error:", e)

        return "یه خطایی پیش اومد 😕 دوباره امتحان کن."