import MySQLdb
import settings

settings.init()

db = MySQLdb.connect(host=settings.DB_ENDPOINT, port=settings.DB_PORT, user=settings.DB_USER, passwd=settings.DB_PASSWORD, db=settings.DB_NAME)
handle = db.cursor()
handle.execute("DROP TABLE nicolet_event_log; COMMIT;")
db.close()
db = MySQLdb.connect(host=settings.DB_ENDPOINT, port=settings.DB_PORT, user=settings.DB_USER, passwd=settings.DB_PASSWORD, db=settings.DB_NAME)
handle = db.cursor()
handle.execute("CREATE TABLE nicolet_event_log (ID VARCHAR(255) NOT NULL, filename VARCHAR(255), datenum INT, channel INT, event_start VARCHAR(40), event_stop VARCHAR(40), event_start_tmstmp FLOAT, event_stop_tmstmp FLOAT, PRIMARY KEY (ID)); COMMIT;")
db.close()