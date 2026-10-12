import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SUBSCRIBERS = set()

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.command()
async def subscribe(ctx):
    SUBSCRIBERS.add(ctx.author.id)
    await ctx.reply("Έκανες εγγραφή για DM ενημερώσεις!")

@bot.command()
async def unsubscribe(ctx):
    SUBSCRIBERS.discard(ctx.author.id)
    await ctx.reply("Ακυρώθηκε η εγγραφή σου.")

@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message):
    sent = 0
    for user_id in list(SUBSCRIBERS):
        user = bot.get_user(user_id)
        if user is None:
            try:
                user = await bot.fetch_user(user_id)
            except discord.HTTPException:
                continue
        try:
            await user.send(message)
            sent += 1
        except discord.HTTPException:
            pass
    await ctx.reply(f"Η ενημέρωση στάλθηκε σε {sent} μέλη.")

bot.run(os.environ["DISCORD_TOKEN"])

