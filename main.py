import asyncio

import discord
from discord.ext import commands
from instaloader import Instaloader, Profile

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

def download_profile_picture(username):
    try:
        loader = Instaloader()
        profile = Profile.from_username(loader.context, username)
        loader.download_profilepic(profile)
        return "Zdjęcie profilowe pobrane pomyślnie."
    except Exception as e:
        return f"Wystąpił błąd podczas pobierania zdjęcia profilowego: {str(e)}"

def download_stories(username):
    try:
        loader = Instaloader()
        loader.download_stories(userids=[username])
        return "Instagram Stories pobrane pomyślnie."
    except Exception as e:
        return f"Wystąpił błąd podczas pobierania Instagram Stories: {str(e)}"

def download_recent_photos(username, count=5):
    try:
        loader = Instaloader()
        profile = Profile.from_username(loader.context, username)
        posts = profile.get_posts()
        for post in list(posts)[:count]:
            loader.download_post(post, target=profile.username)
        return f"{count} ostatnich zdjęć pobrane pomyślnie."
    except Exception as e:
        return f"Wystąpił błąd podczas pobierania ostatnich zdjęć: {str(e)}"

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user.name}')

@bot.command()
async def instagram(ctx):
    await ctx.send("Wybierz co chcesz pobrać:\n1. Zdjęcie profilowe\n2. Instagram Stories\n3. Ostatnie dodane zdjęcia")
    try:
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=60)
        choice = int(msg.content)
        await ctx.send("Podaj nazwę użytkownika na Instagramie:")
        username_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=60)
        username = username_msg.content

        result = ""
        if choice == 1:
            result = download_profile_picture(username)
        elif choice == 2:
            result = download_stories(username)
        elif choice == 3:
            await ctx.send("Podaj liczbę ostatnich zdjęć do pobrania:")
            count_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=60)
            count = int(count_msg.content)
            result = download_recent_photos(username, count)
        else:
            result = "Nieprawidłowa opcja. Wybierz 1, 2 lub 3."

        await ctx.send(result)

    except ValueError:
        await ctx.send("Nieprawidłowa odpowiedź. Spróbuj ponownie.")
    except asyncio.TimeoutError:
        await ctx.send("Czas na odpowiedź minął.")

bot.run("YOUR_TOKEN")
