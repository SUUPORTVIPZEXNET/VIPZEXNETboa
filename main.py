import asyncio
import json
import aiohttp
from rubka.asynco import Robot, Message, filters
from rubka.button import InlineBuilder

# ربات اصلی با توکن ترکیبی
bot = Robot(
    token="DAJFF0VUCVZPZBNHHIEERSDMKRCXTCOBWPFTHJKGFJWNPWNUMNRROTJLCVBYRXPK",
    show_progress=True,
    timeout=900
)

# داده‌های مربوط به مدیریت گروه
DATA_FILE = "group_locks.json"

locks_fa = {
    "لینک": "links",
    "عکس": "photo",
    "ویدیو": "video",
    "صوت": "audio",
    "ویس": "voice",
    "استیکر": "stickers",
    "فایل": "document",
    "آرشیو": "archive",
    "اجرایی": "executable",
    "فونت": "font",
    "نظرسنجی": "polls",
    "کانتکت": "contacts",
    "لوکیشن": "locations",
    "فوروارد": "forwarded"
}
default_locks = {v: False for v in locks_fa.values()}

# داده‌های مربوط به هوش مصنوعی
user_modes = {}

COMPREHENSIVE_CRYPTO_LIST = [
    {'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'btc', 'aliases': ['btc', 'bitcoin', 'xbt']},
    {'id': 'ethereum', 'name': 'Ethereum', 'symbol': 'eth', 'aliases': ['eth', 'ethereum']},
    {'id': 'tether', 'name': 'Tether', 'symbol': 'usdt', 'aliases': ['usdt', 'tether']},
    {'id': 'usd-coin', 'name': 'USD Coin', 'symbol': 'usdc', 'aliases': ['usdc', 'usd coin']},
    {'id': 'binancecoin', 'name': 'BNB', 'symbol': 'bnb', 'aliases': ['bnb', 'binancecoin', 'binance coin']},
]

# توابع مدیریت داده‌های گروه
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# توابع هوش مصنوعی
async def fetch_and_reply(message: Message, mode: str, delete: bool = False):
    base_url = {
        "iron": "https://v3.api-free.ir/codern-gpt/",
        "gpt": "https://v3.api-free.ir/openai/"
    }

    url = (
        f"{base_url[mode]}?text={message.text}"
        f"&token=d619ccac72b765923508c79da83951cf"
        f"&chat_id={message.sender_id}"
    )

    if delete:
        url += "&delete=true"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    if mode == "iron":
                        data = await resp.json()
                        result = data.get("result", "وب‌سرویس پاسخی برنگرداند!")
                    else:  
                        result = await resp.text()
                    await message.reply(result.strip())
                else:
                    await message.reply(f"خطا در دریافت پاسخ: {resp.status}")
    except Exception as e:
        await message.reply(f"خطا در ارتباط با وب‌سرویس: {e}")

def find_crypto(query: str):
    if not query or not isinstance(query, str):
        return None
        
    clean_query = query.lower().strip()

    for crypto in COMPREHENSIVE_CRYPTO_LIST:
        if clean_query in crypto['aliases']:
            return crypto
    
    return None

# ========== هندلر استارت ==========

@bot.on_message(filters=filters.text_equals("start"))
@bot.on_message(filters=filters.text_equals("help"))
@bot.on_message(filters=filters.text_equals("راهنما"))
async def handle_start(bot: Robot, message: Message):
    # آدرس عکس
    photo_url = "https://zaya.io/fbj55"
    
    if message.is_group:
        # کپشن عکس برای گروه - فقط متن مشخص شده
        caption = (
            "🤖 ربات چندمنظوره مدیریت گروه و هوش مصنوعی 🤖\n\n"
            
            "✨ بخش مدیریت گروه:\n"
            "• تنظیم ادمین - تنظیم شما به عنوان ادمین\n"
            "• حذف ادمین - حذف ادمین فعلی\n"
            "• راهنما - نمایش راهنمای کامل\n"
            "• وضعیت - نمایش وضعیت قفل‌ها\n"
            "• قفل [نام] - قفل کردن یک مورد\n"
            "• باز [نام] - باز کردن یک مورد\n"
            "• سخنگو روشن/خاموش - کنترل سخنگو\n\n"
            
            "🔹 لیست قفل‌ها:\n"
            "   • لینک\n"
            "   • عکس\n"
            "   • ویدیو\n"
            "   • صوت\n"
            "   • ویس\n"
            "   • استیکر\n"
            "   • فایل\n"
            "   • آرشیو\n"
            "   • اجرایی\n"
            "   • فونت\n"
            "   • نظرسنجی\n"
            "   • کانتکت\n"
            "   • لوکیشن\n"
            "   • فوروارد\n\n"
            
            "==================================================\n\n"
            
            "✨ بخش هوش مصنوعی:\n"
            "🔹 دستورات هوش مصنوعی:\n"
            "   🟢 iron / آیرون → Codern GPT\n"
            "   🔵 gpt / جی‌پی‌تی → OpenAI GPT-4\n\n"
            "📌 دستورات کاربردی:\n"
            "   ✨ zekr / ذکر → دریافت یک ذکر تصادفی\n"
            "   📈 chart / چارت btc → مشاهده قیمت لحظه‌ای ارزهای دیجیتال\n"
            "   🗑️ delete / پاک کردن → پاک کردن حافظه گفتگو\n"
            "   🎬 rubino / روبینو → دانلود پست روبینو\n\n"
            "⚡ از تجربه‌ی هوش مصنوعی لذت ببرید! ⚡"
        )
        
        # ارسال عکس با کپشن کامل
        await message.reply_image(photo_url, text=caption)
    else:
        # کپشن عکس برای پیوی
        caption = "🤖✨ به ربات هوش مصنوعی خوش آمدید!"
        
        # راهنمای پیوی
        help_text = (
            "🔹 دستورات هوش مصنوعی:\n"
            "   🟢 iron / آیرون → Codern GPT\n"
            "   🔵 gpt / جی‌پی‌تی → OpenAI GPT-4\n\n"
            "📌 دستورات کاربردی:\n"
            "   ✨ zekr / ذکر → دریافت یک ذکر تصادفی\n"
            "   📈 chart / چارت btc → مشاهده قیمت لحظه‌ای ارزهای دیجیتال (btc, eth, ...)\n"
            "   🗑️ delete / پاک کردن → پاک کردن حافظه گفتگو\n"
            "   🎬 rubino / روبینو → دانلود پست روبینو\n\n"
            "⚡ از تجربه‌ی هوش مصنوعی لذت ببرید! ⚡"
        )
        
        # ارسال عکس با کپشن کوتاه
        await message.reply_image(photo_url, text=caption)
        # ارسال متن راهنما
        await message.reply(help_text)

# ========== دستورات هوش مصنوعی (بدون اسلش) ==========

@bot.on_message(filters=filters.text_equals("iron"))
@bot.on_message(filters=filters.text_equals("آیرون"))
async def handle_iron(bot: Robot, message: Message):
    user_modes[message.sender_id] = "iron"
    await message.reply("✅ حالت روی Codern GPT تنظیم شد.")

@bot.on_message(filters=filters.text_equals("gpt"))
@bot.on_message(filters=filters.text_equals("جی‌پی‌تی"))
async def handle_gpt(bot: Robot, message: Message):
    user_modes[message.sender_id] = "gpt"
    await message.reply("✅ حالت روی OpenAI GPT-4 تنظیم شد.")

@bot.on_message(filters=filters.text_equals("delete"))
@bot.on_message(filters=filters.text_equals("پاک کردن"))
async def handle_delete(bot: Robot, message: Message):
    mode = user_modes.get(message.sender_id, "iron")
    await fetch_and_reply(message, mode, delete=True)
    await message.reply("🗑️ حافظه چت شما پاک شد.")

@bot.on_message(filters=filters.text_startswith("rubino"))
@bot.on_message(filters=filters.text_startswith("روبینو"))
async def handle_rubino(bot: Robot, message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply("❗ لطفا لینک پست روبینو را وارد کنید\nمثال: rubino https://rubika.ir/post/XXXX")

        post_url = parts[1]
        api_url = f"https://api-free.ir/api/rubino-dl.php?url={post_url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("ok"):
                        result = data.get("result", {})

                        caption = result.get("caption", "بدون کپشن")
                        video_url = result.get("url")
                        page_username = result.get("page_username", "نامشخص")
                        like_count = result.get("like", 0)
                        comment_count = result.get("comment", 0)
                        view_count = result.get("view", 0)
                        follower_page = result.get("follower_page", 0)

                        text = (
                            f"🎬 ویدیو دانلود شد!\n\n"
                            f"📝 کپشن:\n{caption}\n\n"
                            f"👤 پیج: @{page_username}\n"
                            f"👥 فالوور: {follower_page}\n\n"
                            f"👍 لایک‌ها: {like_count}\n"
                            f"💬 کامنت‌ها: {comment_count}\n"
                            f"👁️ بازدید: {view_count}"
                        )

                        await bot.send_video(message.chat_id, video_url, text=text, reply_to_message_id=message.message_id)
                    else:
                        await message.reply("❌ خطا در دریافت اطلاعات از روبینو!")
                else:
                    await message.reply(f"❌ خطا در اتصال ({resp.status})")
    except Exception as e:
        await message.reply(f"❌ خطا: {e}")

@bot.on_message(filters=filters.text_equals("zekr"))
@bot.on_message(filters=filters.text_equals("ذکر"))
async def handle_zekr(bot: Robot, message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://v3.api-free.ir/zekr/") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await message.reply(f"📿 ذکر امروز:\n\n{data.get('zekr')}")
                else:
                    await message.reply("خطا در دریافت ذکر!")
    except Exception as e:
        await message.reply(f"❌ خطا: {e}")

@bot.on_message(filters=filters.text_startswith("chart"))
@bot.on_message(filters=filters.text_startswith("چارت"))
async def handle_chart(bot: Robot, message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply("❗ لطفا نماد یا نام ارز را وارد کنید.\nمثال: chart shiba")

        user_query = parts[1]
        crypto_info = find_crypto(user_query)

        if not crypto_info:
            return await message.reply(f"❌ ارز «{user_query}» پشتیبانی نمی‌شود یا نامعتبر است.")

        crypto_id_for_api = crypto_info['id']
        await message.reply(f"✅ {crypto_info['name']} ({crypto_info['symbol'].upper()}) یافت شد. در حال دریافت اطلاعات...")

        api_url = f"http://v3.api-free.ir/arz2/?crypto={crypto_id_for_api}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("ok"):
                        result = data.get("result", {})

                        name = result.get("name", "نامشخص")
                        symbol = result.get("symbol", "---")
                        price_usd = result.get("current_price_usd", 0)
                        change_24h = result.get("price_change_percentage_24h", 0)
                        high_24h = result.get("24h_high", 0)
                        low_24h = result.get("24h_low", 0)
                        volume = result.get("total_volume_usd", 0)
                        market_cap = result.get("market_cap_usd", 0)
                        chart_url = result.get("chart_7d_url", "")

                        change_emoji = "📈" if float(change_24h) >= 0 else "📉"

                        reply_text = (
                            f"📊 اطلاعات لحظه‌ای {name} ({symbol.upper()})\n\n"
                            f"💵 قیمت دلاری: ${price_usd}\n"
                            f"{change_emoji} تغییرات ۲۴ساعت: {round(change_24h, 2)}%\n"
                            f"📈 بالاترین ۲۴ساعت: ${high_24h}\n"
                            f"📉 پایین‌ترین ۲۴ساعت: ${low_24h}\n"
                            f"💹 حجم معاملات: ${volume:,}\n"
                            f"🏦 ارزش بازار: ${market_cap:,}"
                        )

                        if chart_url:
                            await message.reply_image(chart_url, text=reply_text)
                        else:
                            await message.reply(reply_text)
                    else:
                        await message.reply("❌ وب‌سرویس اطلاعاتی برای این ارز پیدا نکرد.")
                else:
                    await message.reply(f"❌ خطا در اتصال به وب‌سرویس قیمت ارز ({resp.status})")
    except Exception as e:
        await message.reply(f"❌ یک خطای پیش‌بینی نشده رخ داد: {e}")

# ========== هندلرهای مدیریت گروه (فقط در گروه) ==========

@bot.on_message_group(filters=filters.text_equals("راهنما"))
async def help_group(_: Robot, message: Message):
    help_text = "🤖 ربات چندمنظوره مدیریت گروه و هوش مصنوعی 🤖\n\n"
    
    help_text += "✨ بخش مدیریت گروه:\n"
    help_text += "• تنظیم ادمین - تنظیم شما به عنوان ادمین\n"
    help_text += "• حذف ادمین - حذف ادمین فعلی\n"
    help_text += "• راهنما - نمایش راهنمای کامل\n"
    help_text += "• وضعیت - نمایش وضعیت قفل‌ها\n"
    help_text += "• قفل [نام] - قفل کردن یک مورد\n"
    help_text += "• باز [نام] - باز کردن یک مورد\n"
    help_text += "• سخنگو روشن/خاموش - کنترل سخنگو\n\n"
    
    help_text += "🔹 لیست قفل‌ها:\n"
    for fa_name in locks_fa.keys():
        help_text += f"   • {fa_name}\n"
    
    help_text += "\n" + "="*50 + "\n\n"
    
    help_text += "✨ بخش هوش مصنوعی:\n"
    help_text += "🔹 دستورات هوش مصنوعی:\n"
    help_text += "   🟢 iron / آیرون → Codern GPT\n"
    help_text += "   🔵 gpt / جی‌پی‌تی → OpenAI GPT-4\n\n"
    help_text += "📌 دستورات کاربردی:\n"
    help_text += "   ✨ zekr / ذکر → دریافت یک ذکر تصادفی\n"
    help_text += "   📈 chart / چارت btc → مشاهده قیمت لحظه‌ای ارزهای دیجیتال\n"
    help_text += "   🗑️ delete / پاک کردن → پاک کردن حافظه گفتگو\n"
    help_text += "   🎬 rubino / روبینو → دانلود پست روبینو\n\n"
    help_text += "⚡ از تجربه‌ی هوش مصنوعی لذت ببرید! ⚡"
    
    await message.reply(help_text)

# سایر دستورات مدیریت گروه
@bot.on_message_group(filters=filters.text_equals("تنظیم ادمین"))
async def set_admin(_: Robot, message: Message):
    chat_id = message.chat_id
    chat_data = data.get(chat_id, {"locks": default_locks.copy(), "talker": False})
    if "admin" not in chat_data:
        chat_data["admin"] = message.sender_id
        data[chat_id] = chat_data
        save_data(data)
        await message.reply("✅ شما به عنوان ادمین گروه انتخاب شدید!")
    else:
        await message.reply("⚠️ ادمین قبلی هنوز فعال است!")

@bot.on_message_group(filters=filters.text_equals("حذف ادمین"))
async def remove_admin(_: Robot, message: Message):
    chat_id = message.chat_id
    chat_data = data.get(chat_id)
    if not chat_data or "admin" not in chat_data:
        await message.reply("⚠️ هیچ ادمینی برای گروه تنظیم نشده است!")
        return
    if message.sender_id != chat_data["admin"]:
        await message.reply("❌ فقط ادمین فعلی می‌تواند این کار را انجام دهد!")
        return
    del chat_data["admin"]
    data[chat_id] = chat_data
    save_data(data)
    await message.reply("✅ ادمین گروه با موفقیت حذف شد!")

@bot.on_message_group(filters=filters.text_equals("وضعیت"))
async def status_group(bot: Robot, message: Message):
    chat_id = message.chat_id
    chat_data = data.get(chat_id, {"locks": default_locks.copy(), "talker": False})
    admin_id = chat_data.get("admin")
    
    status_text = "📌 وضعیت قفل‌های گروه 📌\n\n"
    for fa_name, key in locks_fa.items():
        status_text += f"🔹 {fa_name}: {'🔒 بسته' if chat_data['locks'].get(key) else '🔓 باز'}\n"
    status_text += f"🔹 سخنگو: {'✅ روشن' if chat_data.get('talker') else '❌ خاموش'}\n"
    status_text += f"🔹 ادمین: {'✅ تنظیم شده' if admin_id else '❌ تنظیم نشده'}\n"
    status_text += "\n✨ برای قفل کردن: قفل <نام قفل>\n✨ برای باز کردن: باز <نام قفل>"
    await message.reply(status_text)

@bot.on_message_group()
async def lock_commands(bot: Robot, message: Message):
    chat_id = message.chat_id
    chat_data = data.get(chat_id, {"locks": default_locks.copy(), "talker": False})
    admin_id = chat_data.get("admin")
    if not admin_id or message.sender_id != admin_id:
        return

    text = (message.text or "").strip()

    if text == "سخنگو روشن":
        chat_data["talker"] = True
        data[chat_id] = chat_data
        save_data(data)
        await message.reply("✅ سخنگو روشن شد!")
        return
    elif text == "سخنگو خاموش":
        chat_data["talker"] = False
        data[chat_id] = chat_data
        save_data(data)
        await message.reply("❌ سخنگو خاموش شد!")
        return

    for fa_name, key in locks_fa.items():
        if text.startswith(f"قفل {fa_name}"):
            chat_data["locks"][key] = True
            data[chat_id] = chat_data
            save_data(data)
            await message.reply(f"🔒 {fa_name} با موفقیت قفل شد!")
            return
        elif text.startswith(f"باز {fa_name}"):
            chat_data["locks"][key] = False
            data[chat_id] = chat_data
            save_data(data)
            await message.reply(f"🔓 {fa_name} با موفقیت باز شد!")
            return

@bot.on_message_group()
async def group_message_handler(bot: Robot, message: Message):
    # اگر پیام دستور هوش مصنوعی باشد، اجازه دهید پردازش شود
    if message.text:
        known_commands = ["iron", "آیرون", "gpt", "جی‌پی‌تی", "delete", "پاک کردن", "rubino", "روبینو", "zekr", "ذکر", "chart", "چارت", "start", "help", "راهنما", "وضعیت", "تنظیم ادمین", "حذف ادمین"]
        cmd = message.text.split()[0].lower()
        if cmd in known_commands:
            return

    chat_id = message.chat_id
    chat_data = data.get(chat_id)
    if not chat_data:
        return

    admin_id = chat_data.get("admin")
    if message.sender_id == admin_id:
        return

    locks = chat_data.get("locks", default_locks)

    # بررسی قفل‌ها و حذف پیام در صورت نیاز
    checks = {
        "links": "has_link",
        "media": "is_media",
        "files": "file",
        "stickers": "sticker",
        "polls": "poll",
        "contacts": "contact_message",
        "locations": ["location", "live_location"],
        "forwarded": "is_forwarded"
    }

    for key, attr in checks.items():
        if isinstance(attr, list):
            if any(getattr(message, a, None) for a in attr) and locks.get(key):
                await message.delete()
                return
        else:
            if getattr(message, attr, None) and locks.get(key):
                await message.delete()
                return

    media_types = ["photo", "video", "audio", "voice", "document", "archive", "executable", "font"]
    for mtype in media_types:
        if locks.get(mtype) and getattr(message, f"is_{mtype}", False):
            await message.delete()
            return

    # سخنگو هوشمند
    if chat_data.get("talker"):
        text = message.text or ""
        if text:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(f"https://api.rubka.ir/ans/?text={text}") as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            response = result.get("response")
                            if response:
                                await message.reply(response)
                except Exception:
                    pass

# ========== هندلر برای پیام‌های معمولی (هوش مصنوعی) ==========

@bot.on_message()
async def handle_all_messages(bot: Robot, message: Message):
    # اگر پیام دستور باشد، از قبل پردازش شده
    if message.text:
        known_commands = ["start", "help", "iron", "آیرون", "gpt", "جی‌پی‌تی", "delete", "پاک کردن", "rubino", "روبینو", "zekr", "ذکر", "chart", "چارت", "راهنما", "وضعیت", "تنظیم ادمین", "حذف ادمین"]
        cmd = message.text.split()[0].lower()
        if cmd in known_commands:
            return
    
    # اگر پیام در گروه است و مربوط به مدیریت گروه نیست، هوش مصنوعی پاسخ دهد
    if message.is_group:
        chat_id = message.chat_id
        chat_data = data.get(chat_id)
        if chat_data:
            admin_id = chat_data.get("admin")
            # اگر کاربر ادمین نیست و پیام دستور نیست، هوش مصنوعی پاسخ دهد
            if message.sender_id != admin_id and message.text:
                mode = user_modes.get(message.sender_id, "iron")
                asyncio.create_task(fetch_and_reply(message, mode))
        return
    
    # اگر در پیوی است و پیام دستور نیست
    if message.text:
        # پاسخ به سلام‌های معمولی
        text = message.text.lower()
        if text in ["سلام", "hello", "hi", "سلام بوت"]:
            await message.reply("👋 سلام! برای مشاهده راهنما help را ارسال کنید.")
        else:
            # استفاده از هوش مصنوعی برای پاسخ به پیام‌های معمولی
            mode = user_modes.get(message.sender_id, "iron")
            asyncio.create_task(fetch_and_reply(message, mode))

# اجرای ربات
async def main():
    await bot.run(sleep_time=0.1)

if __name__ == "__main__":
    asyncio.run(main())