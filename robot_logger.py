import sqlite3
import datetime

"""
Log a message to the Echo server's database.
"""
def log(message):
	conn = sqlite3.connect('/home/autolab/Workspace/rishi_working/echoyumi/db.sqlite3')
	cursor = conn.cursor()

	cursor.execute("INSERT INTO RobotThoughtApp_log (description, reported, creation_time) VALUES (?, 0, ?)", (message, str(datetime.datetime.now())))

	conn.commit()
	conn.close()

	return

"""
Get all the part names that were spoken to the Echo.
"""
def getGraspCommands():
	f = open("/home/autolab/Workspace/rishi_working/echoyumi/grasp_command.txt", 'r')
	line = f.read()
	f.close()
	if line is None or line == "":
		return None
	part_names = line.split(",")
	# clearing file
	open("/home/autolab/Workspace/rishi_working/echoyumi/grasp_command.txt", 'w').close()
	return part_names

"""
Get (without replacement) the first part name that was spoken to the Echo.
Call this function iteratively to get the part names one at a time.
"""
def getSingleGraspCommand():
	f = open("/home/autolab/Workspace/rishi_working/echoyumi/grasp_command.txt", 'r')
	line = f.read()
	f.close()
	if line is None or line == "":
		return None
	part_names = line.split(",")
	f = open("/home/autolab/Workspace/rishi_working/echoyumi/grasp_command.txt", 'w')
	f.write( ','.join(part_names[1:]) )
	f.close()
	return part_names[0]

