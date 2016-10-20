import sqlite3
import datetime

def log(message):
	conn = sqlite3.connect('/home/autolab/Workspace/rishi_working/echoyumi/db.sqlite3')
	cursor = conn.cursor()

	cursor.execute("INSERT INTO RobotThoughtApp_log (description, reported, creation_time) VALUES (?, 0, ?)", (message, str(datetime.datetime.now())))

	conn.commit()
	conn.close()

	return
