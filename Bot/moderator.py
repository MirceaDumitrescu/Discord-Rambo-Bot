from cog import client, db, write, warning_added
import discord
from discord.utils import get

warnings = {}
# warnings[message.author.id] = points


@client.event
async def on_message(message):
    msg = message.content

    # if message.author.guild_permissions.administrator:
    #     await client.process_commands(message)
    #     return
    # else:
    if any(word.lower() in msg.lower() for word in db["bad_words"]):
        key = str(message.author.id)
        points_database = db["warning_points"]
        if key in points_database:
            if db["warning_points"][key] <= 5:
                points = points_database[key]
                warning_added(key)
                myEmbed = discord.Embed(
                    title="Message Deleted",
                    description=f"Watch your language {message.author}",
                    color=0xFF0000,
                )
                myEmbed.add_field(
                    name="Warning Points", value=f"{points}", inline=False
                )
                await message.delete()
                await message.channel.send(embed=myEmbed)
            else:
                member = message.author
                role = get(member.guild.roles, name="Muted")
                await member.add_roles(role, atomic=True)
                embed = discord.Embed(
                    title="User Muted!",
                    description="**{0}** was muted by the server!".format(member),
                    color=0xFF00F6,
                )
                await message.channel.send(embed=embed)
        else:
            points_database = db["warning_points"]
            points_database[message.author.id] = 1
            write("db/db.json", db)
    await client.process_commands(message)
