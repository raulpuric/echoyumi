import sqlite3
import datetime

def log(message):
	conn = sqlite3.connect('db.sqlite3')
	cursor = conn.cursor()

	cursor.execute("INSERT INTO RobotThoughtApp_log (description, reported, creation_time) VALUES (?, 0, ?)", (message, str(datetime.datetime.now())))

	# for row in cursor.execute("SELECT * FROM RobotThoughtApp_log"):
	# 	print row

	conn.commit()
	conn.close()

	return

log("Test logger")
