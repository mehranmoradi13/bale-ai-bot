import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bale import Bot, Message


# توکن ربات خود را اینجا قرار دهید
TOKEN = "1376112"

# بارگذاری داده‌های JSON
def load_data():
    with open("questions_answers.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data["questions"]

# تابع جستجوی پاسخ بر اساس مشابهت متنی
def find_answer_from_json(user_input):
    # بارگذاری سوالات و پاسخ‌ها از فایل JSON
    questions_data = load_data()

    # ایجاد یک لیست از سوالات
    questions = [item["question"] for item in questions_data]

    # اضافه کردن سوال ورودی به لیست سوالات
    questions.append(user_input)

    # استفاده از TfidfVectorizer برای تبدیل سوالات به وکتورهای TF-IDF
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(questions)

    # محاسبه شباهت کسینوسی بین سوال ورودی و سوالات موجود
    similarities = cosine_similarity(question_vectors[-1], question_vectors[:-1])

    # پیدا کردن اندیس سوالی که بیشترین شباهت را با سوال ورودی دارد
    best_match_index = similarities.argmax()

    # اگر شباهت بیش از حد آستانه‌ای باشد، پاسخ را باز می‌گرداند
    if similarities[0][best_match_index] > 0.3:
        return questions_data[best_match_index]["answer"]
    else:
        return "متاسفانه من نمی توانم به این سوال پاسخ دهم، اما می توانم کمک کنم که راهنمایی بیشتری دریافت کنید."

# ایجاد یک شیء از کلاس Bot
client = Bot(token=TOKEN)

# رویداد زمانی که یک پیام دریافت می‌شود
@client.event
async def on_message(message: Message):
    if message.text:  # اگر پیام متنی باشد
        user_input = message.text  # متن پیام کاربر
        response = find_answer_from_json(user_input)  # یافتن پاسخ
        await message.reply(response)  # ارسال پاسخ به کاربر

# اجرای ربات
client.run()
