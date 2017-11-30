#

def hash_fingerprints(peaks, dstnc): #peaks[time, freq]
    import hashlib

    MAXDELTA = 200
    MINDELTA = 0
    fp = []

    for i in range(len(peaks)):
        for j in range(dstnc):
            if(i + j) < len(peaks):
                f1 = peaks[i][1]
                f2 = peaks[i + j][1] # frequencies at i and up to dstnc away

                delta_t = peaks[i+j][0] - peaks[i][0] # time difference between i and up to distance dstnc away

                if delta_t >= MINDELTA and delta_t <= MAXDELTA:
                    hashpeak = hashlib.md5("{0},{1},{2}".format(str(int(f1)), str(int(f2)), str(int(delta_t))).encode('utf-8')).hexdigest().upper()
                    fp.append(hashpeak) #32 character hashes
    return fp

def write_fingerprint (filename, fprints):
    filename = filename.replace(" ", "_")

    if filename[-4:] != ".txt":
        filename += ".txt"

    file = open(filename, 'w')
    for i in range(len(fprints)):
        file.write(fprints[i] + ",")
    file.close()

"""fingerprints(hash_id, hash_path)
   songs(song_id, hash_id, song_name, song_artist)"""

def find_collisions(filename, hashedpeaks):
    count = 0
    filename = filename.replace(" ","_")
    if filename[-4:] != ".txt":
        filename += ".txt"
    f = open(filename, 'r')
    l = []
    i = 0

    while True:
        hsh = f.read(32) # read 32 character hash
        f.read(1) # skip comma
        try:
            if hsh == '': # if end of file, break
                break
            elif hsh == hashedpeaks[i]:
                count += 1
            l.append(hsh) #
            i += 1        # skipped if eof
        except IndexError:
            break # skip index errors,

    return count

"""fingerprints(hash_id, hash_path)
   songs(song_id, hash_id, song_name, song_artist)"""

def db_connect():
    import MySQLdb as sql
    hst = 'localhost'
    usr = 'root'
    pwd = ''
    dbase = 'audiofingerprinting'

    d = sql.connect(hst, usr, pwd, dbase)
    return d # return connection

def insert_song(songname, artist):
    path = "C:/Fingerprints/"
    songname = songname.replace(" ", "_")
    if songname[-4:] != ".txt":
        songname += ".txt"
    path += songname # add songname to path
    d = db_connect()
    db = d.cursor()
    db.execute("insert into fingerprints(hash_path) values ('{0}')".format(path))
    db.execute("select hash_id from fingerprints where hash_path = '{0}'".format(path))
    hashid = db.fetchone()[0] # hash_id will equal song_id

    db.execute("insert into songs(song_id, song_name, song_artist) values ('{0}','{1}','{2}')".format(hashid, songname[:-4], artist))
    d.commit()
    db.close() # close connection

def match_song(hashedpeaks):
        import re
        regex = r"[^/]+\.txt$"

        d = db_connect()
        db = d.cursor() # get cursor

        db.execute("select hash_path from fingerprints")
        files = db.fetchall()

        l = {}
        for i in range(len(files)):
            l[files[i][0]] = find_collisions(files[i][0], hashedpeaks)

        return get_artist(re.search(regex, max(l, key = l.get)).group()[:-4])

def get_artist(songname):
    songname = songname.replace(" ", "_")
    d = db_connect()
    db = d.cursor()

    db.execute("select song_artist from songs where song_name = '{0}'".format(songname))
    return songname.replace("_", " "), db.fetchone()[0]
