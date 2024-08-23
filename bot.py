import discord
from discord.ext import commands
import json
import os
import aiohttp

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

@bot.command()
async def add_item(ctx, *, item_name):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    if 'inventory' not in data[user_id]:
        data[user_id]['inventory'] = []
    if item_name in data[user_id]['inventory']:
        await ctx.send('Item already in inventory.')
        return
    data[user_id]['inventory'].append(item_name)
    save_data(data)
    await ctx.send(f'Item {item_name} added to your inventory.')

@bot.command()
async def view_inventory(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    inventory = ', '.join(data[user_id].get('inventory', []))
    await ctx.send(f'Inventory: {inventory}')
@bot.command()
async def earn_achievement(ctx, *, achievement_name):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    if 'achievements' not in data[user_id]:
        data[user_id]['achievements'] = []
    if achievement_name in data[user_id]['achievements']:
        await ctx.send('Achievement already earned.')
        return
    data[user_id]['achievements'].append(achievement_name)
    save_data(data)
    await ctx.send(f'Achievement {achievement_name} earned!')

@bot.command()
async def view_achievements(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    achievements = ', '.join(data[user_id].get('achievements', []))
    await ctx.send(f'Achievements: {achievements}')


@bot.command()
async def leaderboard(ctx):
    sorted_users = sorted(data.items(), key=lambda x: len(x[1].get('badges', [])), reverse=True)
    leaderboard_msg = 'Leaderboard:\n'
    for idx, (user_id, user_data) in enumerate(sorted_users[:10]):
        user = await bot.fetch_user(int(user_id))
        badges_count = len(user_data.get('badges', []))
        leaderboard_msg += f'{idx + 1}. {user.name} - {badges_count} badges\n'
    await ctx.send(leaderboard_msg)

@bot.command()
async def delete_character(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found.')
        return
    del data[user_id]
    save_data(data)
    await ctx.send('Character deleted.')


@bot.command()
async def help(ctx):
    help_text = (
        "!create_character <name> - Create a new character\n"
        "!customize_character <attribute> - Customize your character\n"
        "!add_badge <badge_name> - Add a badge to your character\n"
        "!remove_badge <badge_name> - Remove a badge from your character\n"
        "!view_character - View your character's details\n"
        "!add_item <item_name> - Add an item to your inventory\n"
        "!view_inventory - View your inventory\n"
        "!earn_achievement <achievement_name> - Earn an achievement\n"
        "!view_achievements - View your achievements\n"
        "!leaderboard - View top users by badges\n"
        "!delete_character - Delete your character\n"
    )
    await ctx.send(help_text)

@bot.command()
async def set_profile_picture(ctx, url):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data[user_id]['profile_picture'] = url
                save_data(data)
                await ctx.send('Profile picture updated.')
            else:
                await ctx.send('Failed to fetch image. Please check the URL.')

@bot.command()
async def view_profile_picture(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    profile_picture = data[user_id].get('profile_picture')
    if profile_picture:
        await ctx.send(profile_picture)
    else:
        await ctx.send('No profile picture set.')

@bot.command()
async def set_background(ctx, *, background_text):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    data[user_id]['background'] = background_text
    save_data(data)
    await ctx.send('Character background updated.')

@bot.command()
async def view_background(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    background = data[user_id].get('background', 'No background set.')
    await ctx.send(f'Background: {background}')


@bot.command()
async def add_currency(ctx, amount: int):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    if 'currency' not in data[user_id]:
        data[user_id]['currency'] = 0
    data[user_id]['currency'] += amount
    save_data(data)
    await ctx.send(f'Added {amount} currency to your account.')

@bot.command()
async def view_currency(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    currency = data[user_id].get('currency', 0)
    await ctx.send(f'Your current balance is {currency} currency.')

@bot.command()
async def level_up(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    if 'level' not in data[user_id]:
        data[user_id]['level'] = 1
    data[user_id]['level'] += 1
    save_data(data)
    await ctx.send(f'Your character is now level {data[user_id]["level"]}.')

@bot.command()
async def view_level(ctx):
    user_id = str(ctx.author.id)
    if user_id not in data:
        await ctx.send('No character found. Use !create_character first.')
        return
    level = data[user_id].get('level', 1)
    await ctx.send(f'Your character is level {level}.')


















bot.run('YOUR_BOT_TOKEN')
