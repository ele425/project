#

def hash_fingerprints(peaks, dstnc): #peaks[freq,time]
    import hashlib

    MAXDELTA = 200
    MINDELTA = 0
    fp = []

    for i in range(len(peaks)):
        for j in range(dstnc):
            if(i + j) < len(peaks):
                f1 = peaks[i][0]
                f2 = peaks[i + j][0] # frequencies at i and up to dstnc away

                delta_t = peaks[i+j][1] - peaks[i][1] # time difference between i and up to distance dstnc away

                if delta_t >= MINDELTA and delta_t <= MAXDELTA:
                    hashpeak = hashlib.md5("{0},{1},{2}".format(str(f1), str(f2), str(delta_t)).encode('utf-8')).hexdigest().upper()
                    fp.append(hashpeak) #32 character hashes
    return fp

def write_fingerprint (filename, fprints):
    filename = filename.replace(" ", "_")
    if filename[-4:] != ".txt":
        filename += ".txt"
    file = open(filename, 'w')
    for i in range(len(fprints)):
        file.write(fprints[i] + ",")


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
        if hsh == '': # if end of file, break
            break
        elif hsh == hashedpeaks[i]:
            count += 1
        l.append(hsh) #
        i += 1        # skipped if eof

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
    hashid = db.fetchone()[0]

    db.execute("insert into songs(hash_id, song_name, song_artist) values ('{0}','{1}','{2}')".format(hashid, songname[:-4], artist))
    d.commit()
