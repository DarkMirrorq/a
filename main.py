from aiogram import Bot, Dispatcher, executor, types
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    'SpaceStudents\main\spacestudents-1aa1f-firebase-adminsdk-1yh7g-4c353b5ae7.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://spacestudents-1aa1f-default-rtdb.firebaseio.com"
})
ref = db.reference('/hesap')


download_link = "https://firebasestorage.googleapis.com/v0/b/bybugteknov1.appspot.com/o/SpaceStudent-1-0-0.apk?alt=media&token=a0efac59-4f30-453e-b2d7-c0a272061da0"
QR_Download = "https://bybug.net/wp-content/uploads/2022/10/qr.png"


API_TOKEN = "5768978172:AAFTBp2Yziv41uP-6bKI6uifNwHg-WwfwtQ"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Merhaba, ben Space Student's için görev yapan bir Telegram botuyum. Size en iyi hizmeti sağlayabilmek için buradayım. Neler yapabildiğimi görmek ister misiniz?\n\n/docs")


@dp.message_handler(commands=["docs"])
async def docs(message: types.Message):
    await message.reply("Dökümanlarım;\nhttps://bybug.net/space-students/telegram/docs")


@dp.message_handler(commands=["download"])
async def download(message: types.Message):
    await message.reply("Uygulama indiriliyor...\nBu işlem birkaç dakika sürebilir. Eğer bildirimlerimi açarsanız dosya gönderildiğinde Telegram size bildirim gönderecektir.")
    await bot.send_document(message.chat.id, types.InputFile.from_url(download_link))


@dp.message_handler(commands=["link", "downloadlink"])
async def links(message: types.Message):
    await message.reply(f"Drive: https://drive.google.com/file/d/1wco3i0mzyQHxDy_IswCx1FL4TdNRmoZP/view?usp=share_link\n\nYandex: https://disk.yandex.com.tr/d/xovLIpLaF3lrag\n\nDosyaCO: https://dosya.co/87un8quyk1zw/SpaceStudent-1-0-0.apk.html\n\nQR ile indir: {QR_Download}")


@dp.message_handler()
async def premium(message: types.Message):
    if "premium: " in message.text:
        token = message.text.split("premium: ")[1]
        veritabani = ref.get()
        if veritabani[token][8] == "Premium":
            await message.answer('Bu hesap Space Premium üyesidir.')
        else:
            await message.answer('Bu hesap Space Premium üyesi değildir.')
    elif "new: " in message.text:
        token = message.text.split("new: ")[1]
        veritabani = ref.get()
        if not token in veritabani:
            await message.answer('Böyle bir hesap bulunamadı.')
        else:
            await message.answer('Kayıt başarılı!')
    elif "info: " in message.text:
        veritabani = ref.get()
        token = message.text.split("info: ")[1]
        if token in veritabani:
            veri = veritabani[token]
            print(veri)
            parcala = veri.replace("[", "").replace(
                "]", "").replace('"', "").split(",")
            await message.answer(f"Kullanıcı Adı: {parcala[0]}\nE-Posta: {parcala[1]}\nBiyografi: {parcala[2]}\nYaş: {parcala[3]}\n\nKişisel bilgileriniz güvenlik kuralları nedeniyle gizlenmiştir.")
        else:
            await message.answer('Böyle bir hesap bulunamadı.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
