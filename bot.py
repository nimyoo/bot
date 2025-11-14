import discord
import os
import asyncio
from discord.ext import commands
from flask import Flask
from threading import Thread

# Configuração do servidor web
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot Discord Online 24/7"

@app.route('/health')
def health():
    return "OK"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# Configuração do bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user.name}')
    print(f'🔗 ID: {bot.user.id}')
    print('🚀 Bot online 24/7!')
    
    # Status personalizado
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Online 24/7 🚀"
        )
    )

@bot.command()
async def ping(ctx):
    """Verifica a latência do bot"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! {latency}ms')

@bot.command()
async def info(ctx):
    """Informações do bot"""
    await ctx.send('🤖 Bot desenvolvido em Python\n⚡ Online 24/7 no Railway')

@bot.command()
async def hello(ctx):
    """Saudação"""
    await ctx.send(f'👋 Olá {ctx.author.mention}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Resposta automática para mensagens específicas
    if 'bot' in message.content.lower() and 'funciona' in message.content.lower():
        await message.channel.send('🤖 Estou funcionando perfeitamente!')
    
    await bot.process_commands(message)

def start_bot():
    """Inicia o bot Discord"""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ ERRO: DISCORD_TOKEN não encontrado!")
        print("💡 Configure a variável de ambiente DISCORD_TOKEN")
        return
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"❌ Erro ao iniciar bot: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando servidor web...")
    # Inicia servidor web em thread separada
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    print("🤖 Iniciando bot Discord...")
    start_bot()
