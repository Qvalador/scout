# -*- coding: utf-8 -*-

from discord.ext import commands
import random as rng

class RNG:
    """Utilities that provide pseudo-RNG."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def random(self, ctx):
        """displays a random thing you request."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('incorrect random subcommand passed.')

    @random.command()
    async def lenny(self):
        """Displays a random lenny face."""
        lenny = rng.choice([
            "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)",
            "( ͡o ͜ʖ ͡o)", "͡(° ͜ʖ ͡ -)", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "(ง ͠° ͟ل͜ ͡°)ง",
            "ヽ༼ຈل͜ຈ༽ﾉ"
        ])
        await self.bot.say(lenny)

    @commands.command()
    async def choose(self, *choices):
        """chooses between multiple choices.
        to denote multiple choices, you should use double quotes.
        """
        if len(choices) < 2:
            await self.bot.say('not enough choices to pick from.')
        else:
            await self.bot.say(rng.choice(choices))
    # redundancy for `?random choose`       
    @random.command()
    async def choose(self, *choices):
        """chooses between multiple choices.
        to denote multiple choices, you should use double quotes.
        """
        if len(choices) < 2:
            await self.bot.say('not enough choices to pick from.')
        else:
            await self.bot.say(rng.choice(choices))
            
    @commands.command()
    async def roll(self, dice : str):
        """rolls a dice in NdN format."""
        try:
            rolls, limit = dice.split('d')
            if rolls == '':
                rolls = '1'
            rolls = int(rolls)
            limit = int(limit)
        except Exception:
            await self.bot.say('format has to be in NdN!')
            return

        randlist = [str(rng.randint(1, limit)) for r in range(rolls)]
        result = ', '.join(randlist)
        if rolls > 1:
            result_sum = " > {}".format(sum([int(i) for i in randlist]))
        else:
            result_sum = ''
        await self.bot.say(result + result_sum)

def setup(bot):
    bot.add_cog(RNG(bot))