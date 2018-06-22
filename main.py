import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'test!!!')
    elif message.content.startswith('!say'):
        await client.send_message(message.channel, 'leave message')
        msg = await client.wait_for_message(timeout=3.0, author=message.author)

        if msg is None:
            await client.send_message(message.channel, 'input while 15s. try again: !say')
            return
        else:
            await client.send_message(message.channel, msg.content)
client.run('NDU5NzE3ODAwMTY5MDQ2MDI2.Dg6qQw.skpz25CW4irzV5DzVJ3zdQpBSWs')
