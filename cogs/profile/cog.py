# encoding: utf-8

import discord
import praw
import pickle
import datetime
import time
import threading

from conf import *
from discord.ext import commands

class Profile:
    """gets information about TGRP characters."""
    
    def __init__(self, bot):
        self.bot = bot
        self.profile_dir = cog_dir + "profile/profiles.pickle"
        self.check_dir = cog_dir + "profile/last_check.pickle"
        self.users = {}
        self.users = pickle.load(open(self.profile_dir, "rb"))
        self.r = praw.Reddit(client_id = 'WlFvF27esc9alg',
                                  client_secret = 'gzDwG6TiZXluCTlW9MzLs0xDkow',
                                  user_agent = 'scout, a discord bot by /u/Qvalador')
        self.last_check = pickle.load(open(self.check_dir, "rb"))
        self.check_reddit()

    def save_profiles(self):
        """saves all the profiles to the profile pickle."""
        pickle.dump(self.users, open(self.profile_dir, "wb"))
        
    def get_profile(self, profile, member):
        """generates a profile embed."""
        if profile["reddit"]:
            author = profile["name"]
            if profile["cult number"]:
                author += " (No. {})".format(profile["cult number"])
            title = "/u/{}".format(profile["reddit"])
            title_url = "http://reddit.com" + title
        else:
            author = "Profile"
            title = profile["name"]
            if profile["cult number"]:
                title += " (No. {})".format(profile["cult number"])
            title_url = None
            
        if profile["balance"] > 0:
            colour = discord.Colour.green()
        if profile["balance"] == 0:
            colour = discord.Colour.default()
        if profile["balance"] < 0:
            colour = discord.Colour.red()
        
        bio = profile["bio"]
        market_blurb = "{} (${})".format(profile["level"], profile["balance"])
        
        profile_embed = discord.Embed(title=title, url=title_url, colour=colour)
        profile_embed.set_author(name=author, icon_url=member.avatar_url)
        profile_embed.add_field(name="Bio", value=bio)
        profile_embed.add_field(name="Market", value=market_blurb, inline=False)
        
        return profile_embed
        
    @commands.group(pass_context=True, invoke_without_command=True)
    async def profile(self, ctx, member: discord.Member=None):
        """displays a user's profile."""
        if member and member.id in self.users:
            profile_embed = self.get_profile(self.users[member.id], member)
            await self.bot.say(embed=profile_embed)
        elif member and member.id not in self.users:
            await self.bot.say("that user is not registered.")
        else:
            profile_embed = self.get_profile(self.users[ctx.message.author.id], ctx.message.author)
            await self.bot.say(embed=profile_embed)
        
    @profile.command(pass_context=True)
    async def register(self, ctx):
        """creates a profile for the user."""
        id = ctx.message.author.id
        name = ctx.message.author.name
        
        self.users[ctx.message.author.id] = {"name": name, "id": id, "balance": 0, "reddit": '', "level": '0', "bio": '(None)', "cult number": None}
        print("created profile for {}.".format(self.users[id]["name"]))
        await self.bot.say("created profile for {}.".format(self.users[id]["name"]))
        self.save_profiles()
        
    @profile.command(pass_context=True)
    async def name(self, ctx, member: discord.Member=None):
        """returns the name of the user."""
        if member and member.id in self.users:
            name = self.users[member.id]["name"]
            await self.bot.say(name)
        elif member and not member.id in self.users:
            username = member.name
            await self.bot.say("No profile found for {}.".format(username))
        elif not member:
            name = self.users[ctx.message.author.id]["name"]
            await self.bot.say(name)
            
    @profile.command(pass_context=True)
    async def set(self, ctx, profile, *, arg):
        """sets various profile attributes for the user."""
        outlets = {"reddit": self.set_reddit, "bio": self.set_bio, "number": self.set_number}
        if profile in outlets:
            outlet = outlets[profile]
        else:
            await self.bot.say("that profile attribute wasn't found.")
            return
        await outlet(ctx, arg)
        self.save_profiles()
        
        
    async def set_reddit(self, ctx, username):
        """helper function to set a user's reddit account."""
        for item in ["/u/", "u/", "/user/", "user/"]:
            if item in username:
                username = username.replace(item, '')
        redditor = self.r.redditor(username)
        if self.users[ctx.message.author.id]:
            if redditor:
                self.users[ctx.message.author.id]["reddit"] = username
                success = "updated {}'s reddit account: /u/{}".format(ctx.message.author.name, username)
                print(success)
                await self.bot.say(success)
            else:
                await self.bot.say("that reddit account doesn't exist.")
        else:
            await self.bot.say("you are not registered.")
            
    async def set_bio(self, ctx, arg):
        """helper function to set a user's bio."""
        if self.users[ctx.message.author.id]:
            self.users[ctx.message.author.id]["bio"] = arg
            await self.bot.say("{}'s bio has been updated to: `{}`".format(self.users[ctx.message.author.id]["name"], arg))
        else:
            await self.bot.say("you are not registered.")
            
    async def set_number(self, ctx, no):
        if ctx.message.server.id not in ['258764365820461057', '285786907323924482']:
            pass
        else:
            if self.users[ctx.message.author.id]:
                self.users[ctx.message.author.id]["cult number"] = no
                await self.bot.say("{}'s number has been updated to: `{}`".format(self.users[ctx.message.author.id]["name"], no))
            else:
                await self.bot.say("you are not registered.")
                
    @commands.command(pass_context=True)
    async def award(self, ctx, member: discord.Member, quantity):
        """awards the user with the indicated amount of money.  admin use only."""
        if ctx.message.author.id != '117662741413625859':
            await self.bot.say("you're not cool enough for that.")
            return
        else:
            self.users[member.id]["balance"] += int(quantity)
            await self.bot.say("{}'s balance has successfully been increased by ${}.".format(self.users[member.id]["name"], quantity))
            self.save_profiles()
            return
                
    def check_reddit(self):

        for user in self.users:
            if self.users[user]["reddit"]:

                comments = (comment for comment in self.r.redditor(self.users[user]["reddit"]).comments.new(limit=10) if comment.subreddit == self.r.subreddit('tgrp') and datetime.datetime.fromtimestamp(comment.created_utc) > self.last_check)

                submissions = (submission for submission in self.r.redditor(self.users[user]["reddit"]).submissions.new(limit=10) if submission.subreddit == self.r.subreddit('tgrp') and datetime.datetime.fromtimestamp(submission.created_utc) > self.last_check)

                for comment in comments:
                    self.users[user]["balance"] += 20
                for submission in submissions:
                    self.users[user]["balance"] += 30

        self.last_check = datetime.datetime.utcnow()
        pickle.dump(self.last_check, open(self.check_dir, "wb"))

        print("checked reddit.")
        self.save_profiles()
        threading.Timer(600, self.check_reddit).start()
        
def setup(bot):
    bot.add_cog(Profile(bot))