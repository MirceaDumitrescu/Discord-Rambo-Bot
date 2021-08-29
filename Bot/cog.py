import discord
from discord.ext import commands
from discord.utils import get
from main import client, version_no, db, write
from datetime import date
import praw
import random

today = date.today()
version = int(db["version"])
vs = round(version_no(version), 2)


def warning_added(v):
    db["warning_points"][v] += 1
    write("db/db.json", db)
    return db["warning_points"][v]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    test_channel = client.get_channel(881571810125176866)
    myEmbed = discord.Embed(
        title="Bot is online",
        description="RamboBot is now online. Use $help command for info.",
        color=0x00FF00,
    )

    myEmbed.add_field(name="Version", value=f"{vs}", inline=False)
    myEmbed.add_field(name="Last Update", value=f"{today}", inline=False)
    myEmbed.set_footer(text="www.rambobot.com")
    myEmbed.set_author(name="Author: Elder")
    myEmbed.set_thumbnail(
        url="https://www.tvmania.ro/wp-content/uploads/2020/06/Rambo-2-Stallone-Cover-.jpg"
    )

    await test_channel.send(embed=myEmbed)


@client.event
async def on_disconnect():
    print("We have logged off {0.user}".format(client))
    test_channel = client.get_channel(881571810125176866)

    myEmbed = discord.Embed(
        title="Bot is offline",
        description="RamboBot is now offline. Please notify one of its administrators.",
        color=0xFF0000,
    )

    await test_channel.send(embed=myEmbed)


@client.command()
async def close(ctx):
    await client.close()


@client.command()
async def help(ctx):
    myEmbed = discord.Embed(
        title="Help Commands",
        description="""
        Use the following commands with the prefix '$'
        
        This bot is the embodiment of our favorite all times
        character RAMBO. His has the following functionalities:
        - Chat Moderation for swear words
        - Commands listed below
        """,
        color=0x00FF00,
    )

    myEmbed.add_field(
        name="$warnings",
        value="Displays how many warnings you have",
        inline=False,
    )
    myEmbed.add_field(
        name="$dm", value="Gives you an invite link for your friends", inline=False
    )
    myEmbed.add_field(
        name="$meme", value="Returns a random meme in chat for you", inline=False
    )
    myEmbed.add_field(
        name="$add / $remove",
        value="Add / Remove a new swear word to ban from chat (Requires Moderator Role)",
        inline=False,
    )
    myEmbed.add_field(
        name="$role",
        value="Adds you to a very prestigious role named 'Rambo Lover'",
        inline=False,
    )
    myEmbed.set_footer(text="www.rambobot.com")

    await ctx.message.channel.send(embed=myEmbed)


@client.command(name="dm", pass_context=True)
async def dm(ctx, *argument):
    # creating invite link
    invitelink = await ctx.channel.create_invite(temporary=False, unique=True)
    # dming it to the person
    await ctx.author.send(
        f"""**Hello {ctx.author}**
        
Here is your invite link:
    
{invitelink}
                          """
    )


@client.command()
async def add(ctx, *, args):
    member = ctx.message.author
    role = get(ctx.guild.roles, name="Admin")
    if role in member.roles:
        if args.isalpha():
            if args not in db["bad_words"]:
                db.setdefault("bad_words", []).append(args)
                write("db/db.json", db)
                myEmbed = discord.Embed(
                    title="Word Added",
                    description="The word is now added to the Moderator",
                    color=0x00FF00,
                )
                await ctx.message.channel.send(embed=myEmbed)
            else:
                myEmbed = discord.Embed(
                    title="Error!",
                    description="The word might be already in the database.",
                    color=0xFF0000,
                )
                await ctx.message.channel.send(embed=myEmbed)
        else:
            myEmbed = discord.Embed(
                title="Error!",
                description="Only letters allowed",
                color=0xFF0000,
            )
            await ctx.message.channel.send(embed=myEmbed)
    else:
        myEmbed = discord.Embed(
            title="No permission",
            description="You need a higher role for that",
            color=0xFF0000,
        )
        await ctx.message.channel.send(embed=myEmbed)


@client.command()
async def remove(ctx, *, args):
    bad_words = db["bad_words"]
    member = ctx.message.author
    role = get(ctx.guild.roles, name="Admin")
    if role in member.roles:
        if args in db["bad_words"]:
            bad_words.remove(args)
            db["bad_words"] = bad_words
            write("db/db.json", db)
            myEmbed = discord.Embed(
                title="Word Removed",
                description="The word is now removed from the Moderator",
                color=0xFFFF00,
            )
            await ctx.message.channel.send(embed=myEmbed)
        else:
            myEmbed = discord.Embed(
                title="Error!",
                description="The word is already in the list!",
                color=0xFF0000,
            )
            await ctx.message.channel.send(embed=myEmbed)
    else:
        myEmbed = discord.Embed(
            title="No permission",
            description=f"You need a higher role for that",
            color=0xFF0000,
        )
        await ctx.message.channel.send(embed=myEmbed)


@client.command(
    pass_context=True
)  # Need to do a check if the role exists and if the bot has permission
async def role(ctx):
    member = ctx.message.author
    role = get(ctx.guild.roles, name="Rambo")
    if role not in member.roles:
        await member.add_roles(role, atomic=True)
        myEmbed = discord.Embed(
            title="Rambo Role Added",
            description=f"Enjoy your new EPIC ROLE {ctx.message.author}",
            color=0x00FF00,
        )
        await ctx.message.channel.send(embed=myEmbed)
    else:
        myEmbed = discord.Embed(
            title="You already have that role",
            description=f"Isn't it enough?",
            color=0xFF0000,
        )
        await ctx.message.channel.send(embed=myEmbed)


@client.command(pass_context=True)
async def unmute(ctx, user: discord.Member):
    role = get(ctx.guild.roles, name="Muted")
    if role in user.roles:
        await user.remove_roles(role, atomic=True)
        myEmbed = discord.Embed(
            title=f"{user} has been unmuted",
            description=f"Enjoy your time here",
            color=0x00FF00,
        )
        await ctx.message.channel.send(embed=myEmbed)
    else:
        myEmbed = discord.Embed(
            title="The user is not Muted",
            description="Make sure you spelled the name correctly",
            color=0xFFFF00,
        )
        await ctx.message.channel.send(embed=myEmbed)


reddit = praw.Reddit(
    client_id="cgmcBmw0OvoOB4jc8cjV9g",
    client_secret="cb6PIXkEueWP-6IGiWXbkWoAdfwZgA",
    user_agent="Emergency_Pirate2141",
)


@client.command()
async def meme(ctx):
    memes_submissions = reddit.subreddit("memes").hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await ctx.send(submission.url)
