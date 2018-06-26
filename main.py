import discord
import asyncio
import  requests


client = discord.Client()

headers = {
    'User-Agent': 'hq-viewer/1.2.4 (iPhone; iOS 11.1.1; Scale/3.00)',
    'x-hq-client': 'iOS/1.2.4 b59'
}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    url="https://api-quiz.hype.space/"
    requests.post("https://api-quiz.hype.space/verifications", data={

    }).json()["verificationId"]
    print(response.json())


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'test!!!')
    elif message.content.startswith('!say'):
        await client.send_message(message.channel, 'leave message')
        msg = await client.wait_for_message(timeout=15.0, author=message.author)

        if msg is None:
            await client.send_message(message.channel, 'input while 15s. try again: !say')
            return
        else:
            await client.send_message(message.channel, msg.content)


client.run('NDU5NzE3ODAwMTY5MDQ2MDI2.Dg6qQw.skpz25CW4irzV5DzVJ3zdQpBSWs')
