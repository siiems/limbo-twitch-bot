import time
import math
import random
import psutil
from twitchio.ext.commands.core import Context
from general import *
from twitchio.ext import commands

access_token : str = refresh_token()

start_time = time.time()


    
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=f'oauth:{access_token}',
            prefix=f'{prefix}',
            initial_channels=[f'{initial_channel[0]}']
            )
    
    async def event_ready(self):
        print(f'Script by siiems (twitch.tv/siiems)')
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
    
    async def event_message(self, message):
        if message.echo: return
        if message.author.name.lower() in username_blacklist: return
        if message.author.id in userid_blacklist: return

        if (debug):
            print(f'{message.channel.name.lower()}| {message.author.display_name}: {message.content}')
        
        await self.handle_commands(message)


    
    async def event_command_error(self, ctx: Context, error: Exception) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'/me @{ctx.author.name.lower()} command on cooldown')


    
    async def event_token_expired(self):
        try:
            print(f'Access token expired!')
            await commands.Bot.__init__(token=await refresh_token())
            await Bot.connect()
            print('Succesfully refreshed access token and reconnected to twitch IRC server!')
        except: 
            print(f'Failed to reconnect to twitch IRC server - please restart the bot!')
            exit()


    @commands.command(aliases=[''])
    async def ping(self, ctx: commands.Context): 
        uptime = time.time() - start_time
        
        minutes = uptime / 60
        hours = minutes / 60
        seconds = uptime

        uptimeMessage = 'Uptime:'
        if (hours > 1):
            uptimeMessage += f' {round(hours,0)}h'
            minutes = round(minutes,0) % 60

        if (minutes > 1):
            seconds = round(uptime % minutes,0)
            if (seconds % minutes == 0): uptimeMessage += ' and'
            uptimeMessage += f' {round(minutes,0)}mins'

        if (seconds > 0):
            if (hours > 1 or minutes > 1): uptimeMessage += ' and'
            uptimeMessage += f' {round(seconds,2)}s'

        ramUsage = round(psutil.virtual_memory()[3]/1000000000,2)

        await ctx.send(f'/me 🏓 RAM Usage: {ramUsage}MB | {uptimeMessage}')


    @commands.cooldown(rate=1, per=cooldown_limbo, bucket=commands.Bucket.member)
    @commands.command()
    async def limbo(self, ctx: commands.Context): # limbo bet_amount : int | multiplier_prediction : str 
        message : str = ctx.message.content.lower()
        args : [str] = message.split(' ')

        args.pop(0)
        print(message, args)
        if (len(args) < 2):
            await ctx.send(f'/me @{ctx.author.name} bad args')
            return

        userdata = getJsonData('./data.json')

        user_index = get_user_index(userdata, ctx.author.id)

        if (user_index == -1):
            add_user(ctx.author.id)
            user_index = get_user_index(getJsonData('./data.json'),ctx.author.id)


        # PARSE bet_amount 

        bet_amount = 0

        if (not args[0].isnumeric()):
            if (args[0] == 'all'):
                bet_amount = userdata[user_index]['money']

            elif (args[0][-1] == '%'):
                bet_amount = round(userdata[user_index]['money'] * float(args[0][:-1]),2)

            else:
                await ctx.send(f'/me @{ctx.author.name} bad args')
                return
        else:
            bet_amount = round(float(args[0]),2)


        if (bet_amount < 0):
            await ctx.send('/me bet amount is lower than 0!')
            return
        elif (bet_amount > userdata[user_index]['money']):
            await ctx.send('/me not enough money to do dat!')
            return
    

        # PARSE multiplier_prediction

        multiplier_prediction = 0
        try:
            float(args[1])
            multiplier_prediction = round(float(args[1]),3)
        except:
            if (args[1][-1] == 'x'):
                multiplier_prediction = round(float(args[1][:-1]),3)
            else:
                await ctx.send(f'/me @{ctx.author.name} bad args')
                return

        if ((multiplier_prediction < 1.1)):
            await ctx.send('/me multiplier is too low!')
            return

        ran = random.random()
        target = math.pow(multiplier_prediction,-0.99)

        moneyChange = bet_amount * -1
        if (ran < target):
            moneyChange = (bet_amount * multiplier_prediction) - bet_amount

        roll = round((math.exp(math.log(ran)/-1)),2)

        if (random.random() < pre_1x_crash):
            moneyChange = bet_amount * -1
            roll = 0


        userdata[user_index]['money'] += moneyChange
        writeJsonData('./data.json',userdata)

        


        

        if (moneyChange > 0):
            await ctx.send(f'/me @{ctx.author.name} you won {currency}{moneyChange:0,.2f}! => {currency}{userdata[user_index]["money"]} | Rolled ~{roll}x :D ({round(target*100,2)}%)')
        else:
            await ctx.send(f'/me @{ctx.author.name} you lost {currency}{moneyChange*-1:0,.2f}! => {currency}{userdata[user_index]["money"]} | Rolled ~{roll}x :( ({round(target*100,2)}%)')

        if (debug):
            print(f'Chance of winning {round(target*100,2)}%')

    @commands.cooldown(rate=1, per=cooldown_free, bucket=commands.Bucket.member)
    @commands.command()
    async def free(self, ctx: commands.Context): 
        data = getJsonData('./data.json')

        index = get_user_index(data, ctx.author.id)

        if (index == -1):
            add_user(ctx.author.id)
            index = get_user_index(data, ctx.author.id)
        print(index)
        print(data[index])
        data[index]['money'] += free_money
        print(data[index])
        writeJsonData('./data.json',data)

        await ctx.send(f'/me @{ctx.author.name} added {currency}{free_money:0,.2f} to your account :D')

    @commands.command()
    async def balance(self, ctx: commands.Context): # balance
        data = getJsonData('./data.json')
        index = get_user_index(data,ctx.author.id)

        if (index == -1): return
        money = data[index]['money']
        await ctx.send(f'/me @{ctx.author.name} you have {currency}{money:0,.2f} ewpert')



    @commands.command()
    async def chance(self, ctx: commands.Context):
        message = ctx.message.content
        args = message.split(' '); args.pop(0)

        print(args)
        if len(args) < 1: 
            await ctx.send(f'/me @{ctx.author.name} state a roll (e.g {round(random.random()*100,2)}x)')
            return
        
        try:
            args[0] = float(args[0])
        except:
            if (args[0][-1] == 'x'):
                args[0] = float(args[0][:-1])
            else:
                await ctx.send(f'/me @{ctx.author.name} roll must be a number')
                return


        args[0] = round(args[0],2)
        chance = round(math.pow(args[0],-0.99)*100,2)
        if chance > 100: chance = 100

        await ctx.send(f'/me @{ctx.author.name} the chance of winning a {args[0]}x roll is {chance}% :Z')

    
    @commands.command()
    async def flekyu(self, ctx: commands.Context):
        await ctx.send('www.twitch.tv/flekyu/clip/SaltyAbstemiousWoodcockKreygasm-RvbwZxPKyIhDLwXQ')

    @commands.command() 
    async def give(self, ctx: commands.Context):
        message = ctx.message.content
        args = message.split(' '); args.pop(0)

        if (len(args) < 2):
            await ctx.send(f'/me @{ctx.author.name} bad args')
            return
        
        data = getJsonData('./data.json')

        sender_index = get_user_index(data, ctx.author.id)

        if (sender_index == -1):
            add_user(ctx.author.id)

        try:
            int(args[0])
        except:
            await ctx.send(f'/me @{ctx.author.name} invalid userid :/ ')
            return 
        

        recipient_index = get_user_index(data, args[0])

        if (recipient_index == -1):
            await ctx.send(f'/me @{ctx.author.name} that user has no bank account :/')
            return
        
        
        try:
            args[1] = round(float(args[1]),2)
            if (0 >= args[1]): 
                raise ValueError
        except:
            await ctx.send(f'/me @{ctx.author.name} invalid amount :/')
            return
        
        if (data[sender_index]['money'] < args[1]):
            await ctx.send(f'/me @{ctx.author.name} you do not have enough money :/')
            return
        

        data[sender_index]['money'] -= args[1]

        data[recipient_index]['money'] += args[1]

        writeJsonData('./data.json', data)

        await ctx.send(f'/me @{ctx.author.name} gave UserID {args[0]} {currency}{args[1]:0,.2f} :D')

        

    @commands.command(aliases=['pos','position','lb']) 
    async def leaderboard(self, ctx: commands.Context):
        data = getJsonData('./data.json')

        userindex = get_user_index(data, ctx.author.id)

        if (userindex == -1):
            add_user(ctx.author.id)

        leaderboard = sorted(data, key=lambda x: x['money'], reverse=True)

        leaderPos = -1
        for i in range(len(leaderboard)):
            if (leaderboard[i]['user_id'] == ctx.author.id):
                leaderPos = i+1
                break
        
        if (leaderPos == -1):
            print(f'Error while executing leaderboard command with user {ctx.author.id}')
            return
        
        await ctx.send(f'/me @{ctx.author.display_name} you are #{leaderPos} / {len(leaderboard):0,.0f} :D')
        



    

bot = Bot()
bot.run()