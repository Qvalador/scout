#!/usr/bin/env python
# encoding: utf-8
# v1.0

import discord
import gspread
from conf import *
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands
from fuzzywuzzy import process

class TGRP:
    """gets information about TGRP characters."""
    
    def __init__(self, bot):
        self.bot = bot
        self.characters = {}
        self.names = []
        self._update()
        
    @commands.group(invoke_without_command=True)
    async def tgrp(self, *, arg):
        """provides tgrp-related information.  when executed without a subcommand, provides a character profile."""
        
        query = process.extractOne(arg, self.names)[0]
        character = self.characters[query]
        
        name = query
        url = "http://tokyo-ghoul-roleplay.wikia.com/wiki/{}".format(name.replace(" ", "_"))
        species = character['species']
        alias = character['alias']
        faction = character['faction']
        squad = character['squad']
        position = character['position']
        rc = character['rc type']
        rank = character['rank']
        image_url = character['image']
        
        description = 'Alias: {}\nRank: {}\nFaction: {} {} {}\nSpecies: {} {}'.format(alias, rank, faction, "({})".format(squad) if squad else "", "({})".format(position) if position and faction != "Za Deado" else "",  species, "({})".format(rc) if rc else "")
    
        character_embed = discord.Embed(title=name, url=url, description=description)
        character_embed.set_thumbnail(url=image_url)
        
        await self.bot.say(embed=character_embed)
        
    def _update(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(cog_dir + 'tgrp/Scout-37660010eb1b.json', ['https://spreadsheets.google.com/feeds'])
        gs = gspread.authorize(credentials)
        sheet = gs.open('Character Records').worksheet('characters')
        sheet_data = sheet.get_all_values()
        
        self.characters = {i[1]: {"user": i[0], "alias": i[2] if i[2] else "None", "faction": i[3], "squad": i[4], "position": i[5], "species": i[6], "rc type": i[7], "rank": i[8], "ward": i[9], "image": i[22]} for i in sheet_data}
        self.names = list(self.characters.keys())    
    
    @tgrp.command()
    async def update(self):
        """updates the mod records to the most recent version."""
        
        self._update()

        await self.bot.say("done. {} tgrp records are now up-to-date.".format(u'\U00002714'))
        
    @tgrp.command(aliases=['rc'])
    async def species(self, *, arg):
        """returns the character's species."""
        
        query = process.extractOne(arg, self.names)[0]
        character = self.characters[query]
        
        name = query
        url = "http://tokyo-ghoul-roleplay.wikia.com/wiki/{}".format(name.replace(" ", "_"))
        species = character['species']
        rc = character['rc type']
        
        description = "Species: {} {}".format(species, "({})".format(rc) if rc else "")
        
        species_embed = discord.Embed(title=name, url=url, description=description)
        await self.bot.say(embed=species_embed)
        
    @tgrp.command()
    async def alias(self, *, arg):
        """returns the character's alias."""
        
        query = process.extractOne(arg, self.names)[0]
        character = self.characters[query]
        
        name = query
        url = "http://tokyo-ghoul-roleplay.wikia.com/wiki/{}".format(name.replace(" ", "_"))
        alias = character['alias']
        
        alias_embed = discord.Embed(title=name, url=url, description=alias)
        await self.bot.say(embed=alias_embed)        
        
    @tgrp.command()
    async def faction(self, *, arg):
        """returns the character's faction."""
        
        query = process.extractOne(arg, self.names)[0]
        character = self.characters[query]
        
        name = query
        url = "http://tokyo-ghoul-roleplay.wikia.com/wiki/{}".format(name.replace(" ", "_"))
        squad = character['squad']
        position = character['position']
        faction = character['faction']
        
        description = "Faction: {} {} {}".format(faction, "({})".format(squad) if squad else "", "({})".format(position) if position and faction != "Za Deado" else "")
        
        faction_embed = discord.Embed(title=name, url=url, description=description)
        await self.bot.say(embed=faction_embed)
        
    @tgrp.command(aliases=['rate', 'rating', 'ranking'])
    async def rank(self, *, arg):
        """returns the character's rank."""
        
        query = process.extractOne(arg, self.names)[0]
        character = self.characters[query]
        
        name = query
        url = "http://tokyo-ghoul-roleplay.wikia.com/wiki/{}".format(name.replace(" ", "_"))
        rank = character['rank']
        
        rank_embed = discord.Embed(title=name, url=url, description=rank)
        await self.bot.say(embed=rank_embed)   
        
def setup(bot):
    bot.add_cog(TGRP(bot))