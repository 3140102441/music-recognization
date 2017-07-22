import pymysql
from pymysql.cursors import DictCursor
import genprint
import database

#获取样板片段的指纹
def getcutprint(cutname):

    name, songhash, printhash = genprint.getsongprint(cutname)
    
    return printhash

#从数据库中获取匹配的歌曲
def match(printhash):
    print(len(printhash))
    database.cur.execute("SELECT * FROM fingerprints;")

    match = []
    result = [["","",0.0],["","",0.0],["","",0.0]]
    for i in database.cur:
        for j in printhash:
            if i[0] == j[0][0:10]:#检验指纹匹配
                offset_diff = i[2] - j[1]
                match.append((offset_diff, i[1]))#将时间差和指纹的元祖插入match列表

    sid = getid(match)

    for i in range(0,3):
        sid[i][1] = sid[i][1]/(len(printhash)) * 100
        database.cur.execute("SELECT song_name FROM songs WHERE song_id = %d;" %(sid[i][0]))
        songname = database.cur.fetchone()
        database.cur.execute("SELECT singer_name FROM songs WHERE song_id = %d;" %(sid[i][0]))
        singer_name = database.cur.fetchone()
        result[i][0] = (str)songname
        result[i][1] = (str)singer_name
        result[i][2] = sid[i][1]
        print(songname + '     %.2f%%'%(sid[i][1]))
        print(result)

    return result


#获取匹配歌曲的id
def getid(match):
    print(match)
    repeat = {}
    for i in match:
        repeat[i] = match.count(i)

    sid = [[-1,0.0],[-1,0.0],[-1,0.0]]

    repeat = sorted(repeat.items(), key = lambda asd:asd[1], reverse = True)
    print(result)
    sid[0][0] = repeat[0][0][1]
    sid[0][1] = repeat[0][1]
    j = 0

    for i in range (0,len(repeat)):
        print(repeat[i][0][1])
        if (repeat[i][0][1] != sid[0][0] and j == 0 ):
            j = j + 1 
            sid[j][0] = repeat[i][0][1]
            sid[j][1] = repeat[i][1]
        elif (repeat[i][0][1] != sid[0][0] and repeat[i][0][1] != sid[1][0] and j == 1):
            j = j + 1
            sid[2][0] = repeat[i][0][1]
            sid[2][1] = repeat[i][1]
        
    return(sid)

printhash = getcutprint('test.mp3')
match(printhash)