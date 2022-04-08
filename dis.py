import discord, datetime, math
from main import newcheck

client = discord.Client()

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$downloading'):
        array = newcheck()
        embed=discord.Embed(title="""Currently Downloading""", description="ㅤ", color=0xe61eb1)
        for i in array:
            embed.add_field(name=str(i[0]), value="""
            ㅤ
            ETA:  """ +  str(datetime.timedelta(seconds=i[2])) + """
            
            Percentage:   """ + str(i[1])+"%" + """
            
            Size:   """ + str(convert_size(i[3])) + """
            
            """, inline=False)
            embed.add_field(name="ㅤ", value="ㅤ", inline=False)
        await message.channel.send(embed=embed)

client.run('OTYxOTYwNDk4MjAxNDkzNTI0.YlAlhw.6GaRszQqAMzSm2em8xFa20nvg7g')
