import discord
from discord.ext import commands

from datetime import datetime
import lavalink
import requests
import os

import time
from random import choice, randint
import random
from discord.ext.commands import errors, converter
from random import choice as rnd
import re

import aiohttp
import asyncio
import json
import datetime
from .utils import checks


class Developer:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        
    @commands.command()
    async def email(self, ctx, to, subject, *, content):
        r = requests.post(
        "https://api.mailgun.net/v3/sandboxd50559c8904b4e4c880a191a5a3658a5.mailgun.org/messages",
        auth=("api", "a66a57368fcd56103f64af8bc9307e55-b0aac6d0-51737e92"),
        data={"from": "Siri <postmaster@sandboxd50559c8904b4e4c880a191a5a3658a5.mailgun.org>",
              "to": f"Luke Jeffries <itslukejeffries@gmail.com>",
              "subject": subject,
              "text": content})
        embed = discord.Embed()
        embed.add_field(name="To", value="Luke J")
        embed.add_field(name="From", value="Siri")
        embed.add_field(name="Subject", value=subject)
        embed.add_field(name="Content", value=content)
        await ctx.send(embed=embed, content=":mailbox: Sent to **Luke J**!")
        
    @commands.group(pass_context=True)
    @commands.is_owner()
    async def set(self, ctx):
        pass
        
    @set.command(pass_context=True)
    async def status(self, ctx, status):
        if status == 'online' or status == 'Online':
            st = discord.Status.online
        elif status == 'dnd' or status == 'DND' or status == 'donotdisturb':
            st = discord.Status.dnd
        elif status == 'idle' or status == 'Idle':
            st = discord.Status.idle
        elif status == 'invisible' or status == 'Invisible':
            st = discord.Status.invisible
        else:
            pass

        try:
            await self.bot.change_presence(status=st)
            embed = discord.Embed(colour=0x00ff00, title="👌 Done!", description=f"I have set my status to `{status}`!")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
        except:
            await ctx.send("That's not a valid status! Statuses: `online`, `dnd`, `idle`, and `invisible`")
            
    @set.command(pass_context=True)
    async def house(self, ctx, house):
        if house == 'brilliance' or house == 'Brilliance':
            st = discord.HypeSquadHouse.brilliance
        elif house == 'balance' or house == 'Balance':
            st = discord.HypeSquadHouse.balance
        elif house == 'bravery' or house == 'Bravery':
            st = discord.HypeSquadHouse.bravery
        else:
            pass
        try:
            await self.bot.user.edit(house=st)
            embed = discord.Embed(colour=0x00ff00, title="👌 Done!", description=f"I have set my house to `{house}`!")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
        except:
            await ctx.send("That's not a valid house! Houses: `brilliance`(best), `bravery`, and `balance`")

    @set.command(pass_context=True)
    async def username(self, ctx, *, newName):
        try:
            await self.bot.user.edit(username=newName)
            embed = discord.Embed(title="👌 Done!", description=f"I have changed my username!")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error!\n```py\n{e}```")

    @set.command(pass_context=True)
    async def av(self, ctx, url:str):
        try:
            r = requests.get(url)
            await self.bot.user.edit(avatar=r.content)
            embed = discord.Embed(title="👌 Done!", description=f"I have changed my avatar!")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"JPEG & PNG Only!\n```py\n{e}```")
                
    @commands.command(aliases=["resp"])
    @commands.is_owner()
    async def respond(self, ctx, ticket, id, *, message):
        try:
            target = self.bot.get_user(int(id))
            embed = discord.Embed(colour=0x00a6ff, description=f"\"{message}\" - **{ctx.message.author}**")
            embed.set_author(name=f"In response to ticket #{ticket}..", icon_url=self.bot.user.avatar_url)
            await target.send(embed=embed)
            await ctx.send(f":incoming_envelope: I have sent the response to the owner of Ticket **#**{ticket}.")
        except Exception as e:
            await ctx.send(f"U: **Error sending support response!**\n```{e}```")
                
                
    @commands.command(aliases=["respc"])
    @commands.is_owner()
    async def respondc(self, ctx, channel, id, *, message):
        try:
            ticket = channel
            guild = self.bot.get_guild(int(id))
            target = discord.utils.get(guild.channels, name=ticket)
            embed = discord.Embed(colour=0x00a6ff, description=f"\"{message}\" - **{ctx.message.author}**")
            embed.set_author(name=f"Please turn on DMs for better support!", icon_url=self.bot.user.avatar_url)
            await target.send(embed=embed, content=":incoming_envelope: A member of this server attempted to contact support, but had their DMs disabled! **Here is the response from our Support Team:**")
            await ctx.send(f":incoming_envelope: I have sent the response to the guild of the owner of that ticket (`{e}`)") 
        except Exception as e:
            await ctx.send(f"**Error sending support response!**\n```{e}```")
            
    @commands.command(aliases=['debug', 'ev'])
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        """thanksss skuwww"""
        try:
            env = {
                'bot': ctx.bot,
                'ctx': ctx,
                'channel': ctx.message.channel,
                'author': ctx.message.author,
                'guild': ctx.message.guild,
                'message': ctx.message,
                'discord': discord,
                'random': random,
                'commands': commands,
                'requests': requests,
                're': re,
                'os': os,
                'time_rx': re.compile('[0-9]+'),
                'player': self.bot.lavalink.players.get(ctx.guild.id),
                '_': self._last_result
            }

            try:
                result = eval(code, env)
            except SyntaxError as e:
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, e))
                embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                return
            except Exception as e:
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, e))
                embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                return

            if asyncio.iscoroutine(result):
                result = await result

            self._last_result = result
            if code == "bot.http.token":
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\nyou thought wrong.. slut```".format(code))
                embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            else:
                if len(str(result)) > 1500:
                    r = requests.post(f"https://hastebin.com/documents",
                    data=result.encode('utf-8')).json()
                    await ctx.send(":weary::ok_hand: The output is too long to send to chat. Here is a hastebin file for ya.. :point_right: https://hastebin.com/" + r['key'])
                    return
                else:
                    try:
                        embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, result))
                        embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                        embed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed=embed)
                        return
                    except Exception as e:
                        embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, e))
                        embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                        embed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed=embed)
                        return

        except Exception as e:
            embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, e))
            embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            return
        
        
        
    @commands.command(hidden=True, aliases=['cl'])
    @commands.is_owner()
    async def changelog(self, ctx, option, link, *, message):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        letters = ['a', 'A', 'b', 'B', 'C', 'd', 'n', 'x', 'Y', 'y', 's', 'S', 'i', 'k', 'K', 'g', 'G', 'm', 'c']
        letters2 = ['q', 'Q', 'p', 'P', 'o', 'v', 'V', 'z', 'e', 'E', 'I', 'L', 't', 'T', 'r', 'R', 'j', 'J', 'O']
        randc = f'{a}{rnd(letters)}{b}{rnd(letters2)}{c}'
        try:
            c = self.bot.get_channel('478833607126024192')
            if option == 'other' or option == 'o':
                #try:
                embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n* {message}```")
                embed.set_image(url=link)
                #except:
                    #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n* {message}```")
                await c.send(embed=embed)
                await ctx.send(":ok_hand: Done.")
            elif option == 'add' or option == 'a':
                #try:
                embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n+ {message}```")
                embed.set_image(url=link)
                #except:
                    #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n+ {message}```")
                await c.send(embed=embed)
                await ctx.send(":ok_hand: Done.")
            elif option == 'remove' or option == 'r':
                #try:
                embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n- {message}```")
                embed.set_image(url=link)
                #except:
                    #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n- {message}```")
                await c.send(embed=embed)
                await ctx.send(":ok_hand: Done.")
            else:
                await ctx.send("That isn't an option.")
        except Exception as e:
            trl = discord.Embed(title="Error!", colour=0xff775b, description=f"```py\n{e}```")
            await ctx.send(embed=trl)
        
        
    @commands.command(pass_context=True, aliases=['fp', 'forcepost'])
    @commands.is_owner()
    async def post(self, ctx, e = None):
        if e is not None:
            try:
                headers = {'Authorization': fight_me}
                data = {'server_count': len(self.bot.guilds)}
                api_url = 'https://discordbots.org/api/bots/' + str(self.bot.user.id) + '/stats'
                p = requests.post(api_url, data=data, headers=headers).json()
                chan = self.bot.get_channel("478821892309123091")
                msg = await ctx.send("<a:loading:473279565670907914> **Posting** server count..")
                await asyncio.sleep(5)
                await msg.edit(f"<:CheckMark:473276943341453312> Server count **posted**! (`{p}`)")
                embed = discord.Embed(colour=0x008AE2, title="<a:dblheartbeat:393548388664082444> Update!", description="Server Count successfully posted to DBL! (**{}** Servers)".format(len(self.bot.servers)))
                embed.set_footer(text="Force-Posted")
                await chan.send(embed=embed)

            except Exception as e:
                fmt = '```py\n{}: {}\n```'
                embed = discord.Embed(title="<:WrongMark:473277055107334144> **An error occurred while processing your request**", color=0xff0000, description=fmt.format(type(e).__name__, e))
                await ctx.send(embed=embed)
        else:
            await ctx.send("no bitch ")
            

            
def setup(bot):
  bot.add_cog(Developer(bot))
