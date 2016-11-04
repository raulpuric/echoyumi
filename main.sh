#!/usr/bin/env bash

cd ~/Workspace/rishi_working/echoyumi/
git pull origin master
source activate alan_rishi

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

function ctrl_c() {
	source deactivate
	exit $?
}

python manage.py runserver &
./ngrok-linux-64 http 8000

source deactivate alan_rishi
