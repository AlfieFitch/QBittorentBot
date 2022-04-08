import qbittorrentapi, math

qbt_client = qbittorrentapi.Client(
    host='192.168.1.226',
    port=8080,
    username='admin',
    password='adminadmin',
)

def newcheck():
    array = []
    print("checking")
    for torrent in qbt_client.torrents_info():
            array.append([torrent.name, math.trunc(torrent.progress * 100), torrent.eta, torrent.size])
    return(array)






