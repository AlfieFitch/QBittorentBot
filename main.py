import discord, qbittorrentapi, datetime, math, time
from StringProgressBar import progressBar

qbt_client = qbittorrentapi.Client(
    host='<hostname>', 
    port = <port>,
    username='<username', 
    password='<password'
    )

films = []

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

class MyClient(discord.Client):
    async def on_ready(self):
        while True:
            await check_torrents()
            time.sleep(5)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'check':
            await check_torrents()

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

async def check_torrents():
    print("checking new torrents")
    print(films)
    channel = client.get_channel(<channel_id>)
    for torrent in qbt_client.torrents_info():

        present = False;

        for x in films:
            if(torrent.name == x["name"] and torrent.size == x["size"]):
                present = True;
                break;
        
        if(present is True):
            if(torrent.size == torrent.completed):
                print("torrent completed")
                bardata = progressBar.filledBar(torrent.size, torrent.completed, 20, ":black_medium_square:", ":white_medium_square:")
                embed = discord.Embed(title="Download Complete", description="", color=0x00ff00)
                embed.add_field(name="Title", value=torrent.name, inline=False)
                embed.add_field(name="Progress", value=bardata[0] + " " + str(math.floor(bardata[1])) + "%", inline=False)
                embed.add_field(name="Size", value = convert_size(torrent.size), inline=False)
                message = x["message_id"]
                await channel.get_partial_message(message).edit(embed=embed)
            else:
                print("already in list")
                bardata = progressBar.filledBar(torrent.size, torrent.completed, 20, ":black_medium_square:", ":white_medium_square:")
                embed = discord.Embed(title="New Download", description="", color=0xe61eb1)
                embed.add_field(name="Title", value=torrent.name, inline=False)
                embed.add_field(name="Progress", value=bardata[0] + " " + str(math.floor(bardata[1])) + "%", inline=False)
                embed.add_field(name="Size", value = convert_size(torrent.size), inline=False)
                message = x["message_id"]
                await channel.get_partial_message(message).edit(embed=embed)

        else:
            print("not in list")
            bardata = progressBar.filledBar(torrent.size, torrent.completed, 20, ":black_medium_square:", ":white_medium_square:")
            embed = discord.Embed(title="New Download", description="", color=0xe61eb1)
            embed.add_field(name="Title", value=torrent.name, inline=False)
            embed.add_field(name="Progress", value=bardata[0] + " " + str(math.floor(bardata[1])) + "%", inline=False)
            embed.add_field(name="Size", value = convert_size(torrent.size), inline=False)
            message = await channel.send(embed=embed)
            x = {"name": torrent.name, "message_id": message.id, "size": torrent.size}
            films.append(x)

        if not films:
            print("not in list")
            bardata = progressBar.filledBar(torrent.size, torrent.completed, 20, ":black_medium_square:", ":white_medium_square:")
            embed = discord.Embed(title="New Download", description="", color=0xe61eb1)
            embed.add_field(name="Title", value=torrent.name, inline=False)
            embed.add_field(name="Progress", value=bardata[0] + " " + str(math.floor(bardata[1])) + "%", inline=False)
            embed.add_field(name="Size", value = convert_size(torrent.size), inline=False)
            message = await channel.send(embed=embed)
            x = {"name": torrent.name, "message_id": message.id}
            films.append(x)

intents = discord.Intents.default()

client = MyClient(intents=intents)
client.run("<bot_token>")

