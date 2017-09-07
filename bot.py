#!/usr/bin/env python
# encoding: utf-8

import discord
import asyncio
import os
import time
import sys
import threading
import urllib

from discord.ext import commands
from conf import *

description = """yet another niche, general(?)-purpose discord bot for qvalador.  hey, how'd you find this description, anyway?"""

bot = commands.Bot(command_prefix=commands.when_mentioned_or('/'), description=description)

VERSION = "1.0.0"

def update_avatar(filename):
    """updates the avatar to the provided file name."""
    if os.path.isfile(filename):
        with open(filename, "rb") as avatar:
            bot.edit_profile(avatar=avatar.read())
            
def load_cogs():
    for subdir in next(os.walk(cog_dir))[1]:
        try:
            bot.load_extension("cogs.{}.cog".format(subdir))
            print("loaded plugin: {}".format(subdir))
        except Exception as error:
            exception = "{0}: {1}".format(type(error).__name__, error)
            print("Failed to load {}: {}".format(subdir, exception))
            
@bot.event
async def on_ready():
    print("connected!")
    print("username: " + bot.user.name)
    print("id: " + bot.user.id)
    update_avatar("avatar.png")
    load_cogs()
    internet_on()
    
@bot.event
async def on_message_edit(old, new):
    await bot.process_commands(new)
    

@bot.command()
async def quit():
    """bye!"""
    await bot.say("goodbye to oz, and everything i love.")
    os._exit(0)
    
@bot.command()
async def reload(cogname):
    cog = "cogs." + cogname + ".cog"
    try:
        bot.unload_extension(cog)
        bot.load_extension(cog)
        print('reloaded {}'.format(cogname))
        await bot.say('reloaded {}.'.format(cogname))
    except Exception as e:
        print('failed to reload cog {}\n{}: {}'.format(cogname, type(e).__name__, e))
    
@bot.command()
async def info():
    """provides basic information about the bot."""
    await bot.say("""**scout, version {}**
hi, i'm a niche, multi-purpose discord bot written in discord.py by Qvalador.  try {} help for information on my commands.""".format(VERSION, u'\U00002699'))
    
    
@bot.command()
async def ping():
    """boink."""
    await bot.say("pong!")
    
@bot.command(pass_context=True)
async def avatar(ctx, member: discord.Member = None):
    """returns the given user's avatar."""
    if not member:
        member = ctx.message.author
    image_embed = discord.Embed(title="{}'s avatar".format(member.name))
    image_embed.set_image(url=member.avatar_url)
    await bot.say(embed=image_embed)
    
@bot.command()
async def echo(channel: discord.Channel, *, arg):
    await bot.send_message(channel, arg)

def internet_on():
    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
    except:
        os._exit(0)
    threading.Timer(10, internet_on).start()
 
try:   
    bot.run(token)
except OSError:
    os._exit(0)