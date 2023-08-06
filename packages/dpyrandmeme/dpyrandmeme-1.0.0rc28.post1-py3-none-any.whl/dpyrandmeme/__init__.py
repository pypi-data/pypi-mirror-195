#   -------------------------------------------------------------
#   Copyright (c) aviance. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""
dpyrandmeme: discord.py-random-meme

Random memes to be used in discord.py

Copyright (c) aviance. All rights reserved.
Licensed under the MIT License. See LICENSE in project root for information.
"""

from __future__ import annotations
import aiohttp
import discord
import random

__version__ = "1.0.0-rc28-post1"



async def pyrandmeme(hex_color):
    """
        Get Random Meme from a random subreddit and return it inside of an discord embed.
        Usage: pyrandmeme(hex_color)
        Remember to strip the # at the start, or it won't work.
    """
    color = '0x' + hex_color
    lists_for_memes = ['https://www.reddit.com/r/GoCommitDie/rising.json?sort=rising',
                       'https://www.reddit.com/r/okbuddyretard/top.json?sort=top', 
                       'https://www.reddit.com/r/memes/rising.json?sort=rising', 
                       'https://www.reddit.com/r/meme/rising.json?sort=rising', 
                       'https://www.reddit.com/r/dank_meme/rising.json?sort=rising', 
                       'https://www.reddit.com/r/AdviceAnimals/rising.json?sort=rising',
                       'https://www.reddit.com/r/deepfriedmemes/rising.json?sort=rising',
                       'https://www.reddit.com/r/dankchristianmemes/rising.json?sort=rising',
                       'https://www.reddit.com/r/terriblefacebookmemes/rising.json?sort=rising',
                       'https://www.reddit.com/r/prequelmemes/rising.json?sort=rising',
                       'https://www.reddit.com//r/garlicbreadmemes/rising.json?sort=rising',
                       'https://www.reddit.com/r/offensivememes/rising.json?sort=rising',
                       'https://www.reddit.com/r/arabfunny/rising.json?sort=rising',
                       'https://www.reddit.com/r/darkmemes/rising.json?sort=rising',
                       'https://www.reddit.com/r/antimeme/rising.json?sort=rising',
                       'https://www.reddit.com/r/madlads/rising.json?sort=rising',
                       'https://www.reddit.com/r/funny/rising.json?sort=rising',]
    

    async with aiohttp.ClientSession() as cs:
        async with cs.get(lists_for_memes[random.randint(0, 16)]) as r:
            res = await r.json()
            var=res['data']['children'][random.randint(0, 16)]['data']
            pymeme = discord.Embed(url="https://www.reddit.com" + var['permalink'], title="**" + var['title'] + "**", color=color)
            pymeme.set_image(url=var['url'])
            pymeme.set_footer(text='Post made by u/' + var['author'] + ' and posted in subreddit r/' + var['subreddit'] + '.')
            return pymeme
        await pyrandmeme('e91e63')