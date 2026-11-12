from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "9289886987:AAEplF-SHoFlU16ITHH2tcdpXhcrLRaGZdM
"
ADMIN = "@Bntyemn"
bot = Bot(token=TOKEN)
dp = Dispatcher()

PAYMENTS = {
    "الكريمي جوالي": "الكريمي - الاسم: ... - الرقم: 7XXXXXXXX",
    "ون كاش": "ون كاش - الرقم: 7XXXXXXXX",
    "أم فلوس": "أم فلوس - الرقم: 7XXXXXXXX",
}

PRODUCTS = {
    "whatsapp_ready": [
        {"name": "رقم واتساب جاهز 733", "price": "5000 ريال", "code": "W1"},
        {"name": "رقم واتساب جاهز 772", "price": "5000 ريال", "code": "W2"},
    ],
    "telegram_ready": [
        {"name": "حساب تلجرام جاهز", "price": "4000 ريال", "code": "T1"},
    ],
    "vip": [
        {"name": "رقم مميز 777777", "price": "50,000 ريال", "code": "V1"},
    ],
    "closed": [
        {"name": "رقم مغلق اتصال 733", "price": "7000 ريال", "code": "C1"},
    ],
}

CATEGORIES = {
    "whatsapp_ready": "📱 ارقام واتساب جاهزة",
    "telegram_ready": "✈️ حسابات تلجرام جاهزة",
    "vip": "💎 ارقام واتساب مميزة",
    "closed": "🔒 ارقام واتساب مغلقة اتصال",
}

def main_menu():
    kb = InlineKeyboardBuilder()
    for key, title in CATEGORIES.items():
        kb.button(text=title, callback_data=f"cat_{key}")
    kb.button(text="👨‍💻 مطور البوت", url="https://t.me/Bntyemn")
    kb.button(text="📞 الدعم", url="https://t.me/Bntyemn")
    kb.adjust(1)
    return kb.as_markup()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"أهلا فيك في متجر أرقام اليمن 🔥\n\nاختر القسم اللي تبغاه:\nمطور البوت: {ADMIN}", reply_markup=main_menu())

@dp.callback_query(F.data.startswith("cat_"))
async def show_category(call: types.CallbackQuery):
    cat = call.data.replace("cat_", "")
    kb = InlineKeyboardBuilder()
    text = f"{CATEGORIES[cat]}\n\nاختر المنتج:\n"
    for p in PRODUCTS[cat]:
        kb.button(text=f"{p[ name ]} - {p[ price ]}", callback_data=f"buy_{p[ code ]}")
    kb.button(text="🔙 رجوع", callback_data="back")
    kb.adjust(1)
    await call.message.edit_text(text, reply_markup=kb.as_markup())

@dp.callback_query(F.data == "back")
async def back(call: types.CallbackQuery):
    await call.message.edit_text("اختر القسم اللي تبغاه:", reply_markup=main_menu())

@dp.callback_query(F.data.startswith("buy_"))
async def buy(call: types.CallbackQuery):
    code = call.data.replace("buy_", "")
    product = None
    for lst in PRODUCTS.values():
        for p in lst:
            if p[ code ] == code:
                product = p
    kb = InlineKeyboardBuilder()
    for pay_name in PAYMENTS.keys():
        kb.button(text=f"💳 {pay_name}", callback_data=f"pay_{code}_{pay_name}")
    kb.button(text="🔙 رجوع", callback_data="back")
    kb.adjust(1)
    await call.message.edit_text(f"اخترت: {product[ name ]}\nالسعر: {product[ price ]}\n\nاختر طريقة الدفع:", reply_markup=kb.as_markup())

@dp.callback_query(F.data.startswith("pay_"))
async def pay(call: types.CallbackQuery):
    _, code, pay_name = call.data.split("_", 2)
    info = PAYMENTS[pay_name]
    await call.message.edit_text(f"✅ طلبك تم استلامه\n\nكود المنتج: {code}\nطريقة الدفع: {pay_name}\nحول على:\n{info}\n\nبعد التحويل، ارسل صورة الاشعار للمطور {ADMIN}\nوسيتم تسليمك المنتج فوراً.", reply_markup=main_menu())

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
  
