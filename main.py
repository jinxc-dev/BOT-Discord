import discord
import asyncio
import hq


client = discord.Client()
hq_inst = hq.HQ()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')

@client.event
async def on_message(message):
    
    msg = message.content.strip()
    args_val = msg.split(' ')
    author = message.author

    if message.content.startswith('!hq new'):
        embed = discord.Embed(title="HQ New Helper", desciption="HQ New helper running")
        result_state = ''
       
        # phone authenticate
        result_state = hq_inst.authenticate(args_val[2])
        if result_state == "error_phone":
            embed.add_field(name="Wrong Phone", value=f'{author.name} check phone number [{args_val[2]}]')
            embed.add_field(name="Wrong Phone", value=f'{author.name} check {args_val[2]}')
        else:
            embed.add_field(name="SMS Sent", value=f'{author.name} Check {args_val[2]} for your code')
            embed.add_field(name="Next Stage", value=f'!hq life <sms_code> <referral username> in chat for you HQ life!')
        await client.send_message(message.channel, embed=embed)

    elif message.content.startswith('!hq life'):
        embed = discord.Embed(title="HQ Life Helper", desciption="HQ Life helper running")
        result_state = ''
        # phone verifiy
        if len(args_val) < 4:
            embed.add_field(name="Error Command", value=f'!hq life <sms_code> <referral username>')
        else:
            result_state = hq_inst.verification(args_val[2])
            if result_state == "error_sms":
                embed.add_field(name="Wrong SMS Code", 
                  value=f'{author.name}: Phone verifiy code wrong **[{args_val[2]}]**')
            else:
                result_state = hq_inst.create_referral(args_val[3])

                if result_state == "error_exist_user":
                    embed.add_field(name="Wrong create user", 
                      value=f'{author.name}:This phonenumber is exist owner')

                elif result_state == "error_referral":
                    embed.add_field(name="SMS Sent", 
                        value=f'{author.name}: Wrong referral username **{args_val[3]}**')

                else:
                    embed.add_field(name="Success!", 
                      value=f'Created account **{result_state["username"]}** and referred **{args_val[3]}**!')
                    embed.add_field(name="desc", value=f'**{result_state["username"]}** will join text game...')

        await client.send_message(message.channel, embed=embed)
    elif message.content.startswith('!hq stats'):
        embed = discord.Embed(title="HQ stats", desciption=f"Get HQ user **{args_val[2]}** stats helper")
        if len(args_val) < 3:
            embed.add_field(name="Error Command", value=f'!hq stats <username>')
        else:
            result_state = hq_inst.get_user(args_val[2])
            if result_state == "error_auth":
                embed.add_field(name="Error Auth", value=f"Bot have no HQ Auth")
            elif result_state == "error_no_user":
                embed.add_field(name="Wrong User", value=f"**{args_val[2]}** doesn't exist in HQ Life")
            else:
                embed.add_field(name="Games", value=f"**Played**: {result_state['gamesPlayed']}")
                embed.add_field(name="Wins", 
                    value=f"**Total Wins**: {result_state['leaderboard']['wins']}\n**Total Earnings**:{result_state['leaderboard']['alltime']['total']}\n**Weekly Earnings**:{result_state['leaderboard']['weekly']['total']}\n")
                embed.add_field(name="Ranking", 
                    value=f"**Weekly**: {result_state['leaderboard']['weekly']['rank']}\n**All Time**:{result_state['leaderboard']['alltime']['rank']}")
        await client.send_message(message.channel, embed=embed)
    elif message.content.startswith('!hq nextgame'):
        embed = discord.Embed(title="HQ Upcoming Game", desciption=f"HQ Upcoming Game")
        info = hq_inst.get_show_info()
        embed.add_field(name="GameInfo", value=f"**DateTime**: {info['nextShowTime']}\n**Prize**: {info['nextShowPrize']}")
        await client.send_message(message.channel, embed=embed)

    elif message.content.startswith('!help'):
        embed = discord.Embed(title="HQ Life Bot", desciption="Help")
        embed.add_field(name="Command", 
            value = "**1.new**: !hq new +<country prefix><number>\n**2.life**:!hq life <code> <referral username>\n**3.life**:!hq stats <username>\n**4.life**:!hq nextgame")
        await client.send_message(message.channel, embed=embed)

client.run('NDYxMjk5MjMwMjk2NzY4NTI1.DhSHRA.xe0v4vLMuSALNDr6P5a4AxdXu5w')
