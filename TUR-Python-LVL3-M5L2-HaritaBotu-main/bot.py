from config import *
from logic import *
import discord
from discord.ext import commands
from config import TOKEN

# Veri tabanı yöneticisini başlatma
manager = DB_Map("database.db")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot başlatıldı!")

@bot.command()
async def start(ctx: commands.Context):
    await ctx.send(f"Merhaba, {ctx.author.name}. Mevcut komutların listesini keşfetmek için !help_me yazın.")

@bot.command()
async def help_me(ctx: commands.Context):
    await ctx.send("""
Mevcut komutlar:
- `!start` - Botu başlatır ve hoş geldiniz mesajı verir.
- `!help_me` - Bu komut listesini gösterir.
- `!show_city <şehir_adı>` - Belirtilen şehri haritada gösterir.
- `!remember_city <şehir_adı>` - Belirtilen şehri kaydeder.
- `!show_my_cities` - Kaydedilmiş şehirlerinizi listeler ve haritada gösterir.
""")

@bot.command()
async def show_city(ctx: commands.Context, *, city_name=""):
    coordinates = manager.get_coordinates(city_name)
    if not coordinates:
        await ctx.send("Şehir bulunamadı. Lütfen doğru bir şehir adı girin.")
        return

    path = f"{city_name}_map.png"
    manager.create_graph(path, [city_name])
    with open(path, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command()
async def show_my_cities(ctx: commands.Context):
    cities = manager.select_cities(ctx.author.id)
    if not cities:
        await ctx.send("Henüz şehir kaydetmediniz.")
        return

    path = f"{ctx.author.id}_my_cities.png"
    manager.create_graph(path, cities)
    with open(path, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command()
async def remember_city(ctx: commands.Context, *, city_name=""):
    if manager.add_city(ctx.author.id, city_name):  
        await ctx.send(f'{city_name} şehri başarıyla kaydedildi!')
    else:
        await ctx.send("Hatalı format. Lütfen şehir adını İngilizce olarak ve komuttan sonra bir boşluk bırakarak girin.")

if __name__ == "__main__":
    bot.run(TOKEN)
