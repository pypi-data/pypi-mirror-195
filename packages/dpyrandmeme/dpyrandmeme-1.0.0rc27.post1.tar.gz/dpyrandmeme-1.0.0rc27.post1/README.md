# dpyrandmeme: random memes for discord.py


**What does the library do?**
This library simply uses aiohttp to collect json data from a reddit page and turns it into a link inorder to be used while also storing the memes and returning the meme as a discord embed before sending back to the discord bot to send to the member who sent that command. It is the same meme library that is currently being used inside Paradigm.
<br>
**PyPi library link:**
https://pypi.org/project/dpyrandmeme/
<br><br>
**USAGE OF CODE IN A DISCORD SLASH COMMAND COG:**

```python
"""
  This snippet is the actual meme slash command code from the Paradigm Source Code.
"""

from discord.ext import commands
from dpyrandmeme import pyrandmeme


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def meme(self, ctx):
        """
        Get some random memes from reddit.
        """

        await ctx.send(embed=await pyrandmeme())

async def setup(client):
    await client.add_cog(Meme(client))
```
<br>
<br>
**Credits:**

d33pak123: https://github.com/d33pak123/Pyrandmeme-python-library, <br>
Microsoft for the template.
<br>
<br>
<br>
<br>
©2023 aviance. Project is open-source through the MIT License.
