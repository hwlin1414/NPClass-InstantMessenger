import MySQLdb
import MySQLdb.cursors

class database(object):
    def __init__(self, host='localhost', port='3306', user=None, passwd=None, db=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def open(self):
        try :
            db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=int(self.port), cursorclass=MySQLdb.cursors.DictCursor)
        except MySQLdb.Error, e:
            print "DB connection Error %d: %s" % (e.args[0], e.args[1])
            return None
        db.autocommit(True)
        self.c = db.cursor()
        self.c.execute('set names \'utf8\'')
        return self
