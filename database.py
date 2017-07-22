# coding=utf-8
import pymysql

from pymysql.cursors import DictCursor
import genprint

#连接mysql
conn = pymysql.connect(host = 'localhost', port = 3306, user='root', password = '5438', db = 'fingerprint', charset = "utf8")
cur = conn.cursor()

FIELD_FILE_SHA1 = 'file_sha1'
FIELD_SONG_ID = 'song_id'
FIELD_SONGNAME = 'song_name'
FIELD_OFFSET = 'offset'
FIELD_HASH = 'hash'
FIELD_SONG_SINGERNAME = 'singer_name'

#表
FINGERPRINTS_TABLENAME = "fingerprints"
SONGS_TABLENAME = "songs"

#创建表
CREATE_FINGERPRINTS_TABLE = """
    CREATE TABLE IF NOT EXISTS `%s` (
         `%s` char(10) not null,
         `%s` mediumint unsigned not null,
         `%s` int unsigned not null,
     INDEX (%s),
     UNIQUE KEY `unique_constraint` (%s, %s, %s),
     FOREIGN KEY (%s) REFERENCES %s(%s) ON DELETE CASCADE
) ENGINE=INNODB;""" % (
    FINGERPRINTS_TABLENAME, FIELD_HASH,
    FIELD_SONG_ID, FIELD_OFFSET, FIELD_HASH,
    FIELD_SONG_ID, FIELD_OFFSET, FIELD_HASH,
    FIELD_SONG_ID, SONGS_TABLENAME, FIELD_SONG_ID
)

CREATE_SONGS_TABLE = """
    CREATE TABLE IF NOT EXISTS `%s` (
        `%s` mediumint unsigned not null auto_increment,
        `%s` varchar(250) not null,
        `%s` binary(20) not null,
        `%s` varchar(250) not null,
    PRIMARY KEY (`%s`),
    UNIQUE KEY `%s` (`%s`)
) ENGINE=INNODB;""" % (
    SONGS_TABLENAME, FIELD_SONG_ID, FIELD_SONGNAME,
    FIELD_FILE_SHA1, FIELD_SONG_SINGERNAME,
    FIELD_SONG_ID, FIELD_SONG_ID, FIELD_SONG_ID,
)
#插入指纹
INSERT_FINGERPRINT = """
    INSERT IGNORE INTO %s (%s, %s) values
        (UNHEX(%%s), %%s);
""" % (FINGERPRINTS_TABLENAME, FIELD_HASH, FIELD_SONG_ID)

#插入歌曲
INSERT_SONG = "INSERT INTO %s (%s, %s, %s) values (%%s, %%s, UNHEX(%%s));" % (
    SONGS_TABLENAME, FIELD_SONGNAME, FIELD_SONG_SINGERNAME, FIELD_FILE_SHA1)


def create():
    
    cur.execute(CREATE_SONGS_TABLE)
    cur.execute(CREATE_FINGERPRINTS_TABLE)

# 输入歌曲名，将歌曲信息插入mysql
def insert(songname):

    name, songhash, printhash = genprint.getsongprint(songname)
    name = name.encode(encoding='utf=8')

    spitresult = name.split(' - ./')
    
    cur.execute(INSERT_SONG, (spitresult[1], spitresult[0], songhash))
    conn.commit()
    sid = cur.lastrowid
    #print(printhash)
    print(len(printhash))
    for h in range(len(printhash)):
        print(printhash[h])
        print(str(printhash[h])[2:12])
        print(sid)
        print(int(printhash[h][1]))
        cur.execute("INSERT INTO fingerprints(hash, song_id, offset) VALUES ('%s', %d, %d);" % (str(printhash[h])[2:12], sid, int(printhash[h][1])))
    conn.commit()
    return sid
