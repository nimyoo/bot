import discord
import asyncio
import os
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread

# Configurações básicas
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Servidor web simples para manter online
app = Flask('')

@app.route('/')
def home():
    return "🤖 Bot Discord Online 24/7"

def run_web():
    app.run(host='0.0.0.0', port=8080)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user.name}')
    print(f'🔗 ID do Bot: {bot.user.id}')
    print('🤖 Bot está online e funcionando 24/7!')
    
    # Atualiza status do bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Online 24/7 🚀"
        )
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!ping'):
        await message.channel.send('🏓 Pong!')
    
    if message.content.startswith('!info'):
        await message.channel.send('🤖 Bot online 24/7 com Python!')
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f'👋 Olá {ctx.author.mention}!')

@bot.command()
async def status(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'📊 Status: Online\n⏱️ Latência: {latency}ms')

# Comando para verificar uptime
@bot.command()
async def uptime(ctx):
    await ctx.send('🕒 Bot online 24 horas por dia!')

# Loop para manter atividades
@tasks.loop(minutes=30)
async def change_status():
    activities = [
        discord.Activity(type=discord.ActivityType.playing, name="Online 24/7 🚀"),
        discord.Activity(type=discord.ActivityType.watching, name="seus comandos"),
        discord.Activity(type=discord.ActivityType.listening, name="!help")
    ]
    
    for activity in activities:
        await bot.change_presence(activity=activity)
        await asyncio.sleep(300)  # Muda a cada 5 minutos

def main():
    # Inicia o servidor web em uma thread separada
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    
    # Inicia o bot
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ ERRO: DISCORD_TOKEN não encontrado!")
        return
    
    bot.run(token)

if __name__ == "__main__":
    main()
