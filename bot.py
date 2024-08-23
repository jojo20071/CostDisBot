import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load_data():
    if os.path.isfile('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

data = load_data()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def create_character(ctx, *, name):
    user_id = str(ctx.author.id)
    if user_id in data:
        await ctx.send('Character already exists.')
        return
    data[user_id] = {'name': name, 'badges': []}
    save_data(data)
    await ctx.send(f'Character {name} created!')

@bot.command()
async def customize_character(ctx, *, attribute):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    data[user_id]['attribute'] = attribute
    save_data(data)
    await ctx.send(f'Character customized with {attribute}.')

@bot.command()
async def add_badge(ctx, badge_name):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    if badge_name in data[user_id]['badges']:
        await ctx.send('Badge already owned.')
        return
    data[user_id]['badges'].append(badge_name)
    save_data(data)
    await ctx.send(f'Badge {badge_name} added to your character.')

@bot.command()
async def remove_badge(ctx, badge_name):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    if badge_name not in data[user_id]['badges']:
        await ctx.send('Badge not found.')
        return
    data[user_id]['badges'].remove(badge_name)
    save_data(data)
    await ctx.send(f'Badge {badge_name} removed from your character.')
@bot.command()
async def view_character(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    character = data[user_id]
    name = character.get('name', 'Unknown')
    attribute = character.get('attribute', 'None')
    badges = ', '.join(character.get('badges', []))
    response = f'Name: {name}\nAttribute: {attribute}\nBadges: {badges}'
    await ctx.send(response)










bot.run('YOUR_BOT_TOKEN')
