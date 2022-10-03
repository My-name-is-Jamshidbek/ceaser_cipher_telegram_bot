from aiogram import types
from loader import dp
from Caesar_cipher import main
from aiogram.dispatcher.filters import CommandStart
from states import *
from aiogram.dispatcher import FSMContext
from btn import *
@dp.message_handler(CommandStart())
async def resend(m:types.Message):
    await m.answer('Assalomu aleykum '+str(m.from_user.full_name)+' bu caeser cipher telgram boti bu bot yordamida siz cieser cipher algoritmidan foydalanib matnlarni decodlash va encodlashingiz mumkin!\kerakli menyuni tanlang:',reply_markup=btn_menu)
    await Yagona.tur.set()
@dp.message_handler(state=Yagona.tur, content_types=types.ContentType.TEXT)
async def tur(msg:types.Message,state:FSMContext):
    if msg.text == 'Encod':
        await msg.answer('Siz encode menyuini tanladingiz shifrni ochish uchun matnni kiriting:',reply_markup=btn_bekor)
        await state.update_data(tur = 'encode')
        await Yagona.soz.set()
    elif msg.text == 'Decod':
        await msg.answer('Siz decode menyuini tanladingiz shifrlash uchun matnni kiriting:',reply_markup=btn_bekor)
        await state.update_data(tur = 'decode')
        await Yagona.soz.set()
    else:
        await msg.answer('Bunday menyu mavjud emas!',reply_markup=btn_menu)
        await Yagona.tur.set()
@dp.message_handler(state=Yagona.soz,content_types=types.ContentType.TEXT)
async def soz(msg:types.Message,state:FSMContext):
    if msg.text == 'Bekor qilish':
        await msg.answer('Bekor qilindi!', reply_markup=btn_menu)
        await Yagona.tur.set()
    else:
        await state.update_data(soz=str(msg.text))
        await msg.answer(str('Surishlar'),reply_markup=btn_bekor)
        await Yagona.surish.set()
@dp.message_handler(state=Yagona.surish,content_types=types.ContentType.TEXT)
async def surish(msg:types.Message,state:FSMContext):
    try:
        if msg.text.isdigit():
            if 0<int(msg.text)<27:
                baza = await state.get_data()
                soz = baza.get('soz')
                tur = baza.get('tur')
                surish = int(msg.text)
                cl = main.Ceaser_cipher(surish)
                if tur == 'encode':
                    txt = cl.encod(soz)
                    await msg.answer('encode: '+ soz + '\ncode: '+txt,reply_markup=btn_menu)
                    await Yagona.tur.set()
                elif tur == 'decode':
                    txt = cl.decod(soz)
                    await msg.answer('decode: '+ soz + '\ncode: '+txt,reply_markup=btn_menu)
                    await Yagona.tur.set()
                else:
                    await msg.answer('Nomalum xatolik!',reply_markup=btn_menu)
                    await Yagona.tur.set()
            else:
                await msg.answer('Siz kiritgan raqam 1 dan katta 26 dan kichik shartini qo`llab quvvatlamaydi!',reply_markup=btn_bekor)
                await Yagona.surish.set()
        elif msg.text == 'Bekor qilish':
            await msg.answer('Bekor qilindi!',reply_markup=btn_menu)
            await Yagona.tur.set()
        else:
            await msg.answer('Siz son kiritmadingiz iltimos surishlar sonini kiriting.',reply_markup=btn_bekor)
            await Yagona.surish.set()
    except:
        await msg.answer('Nomalum xatolik!', reply_markup=btn_menu)
        await Yagona.tur.set()
