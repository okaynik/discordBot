ls -tl
pwd
cd discordBot &&
git pull &&
pip3 install -r requirements.txt &&
cat bot.pid | xargs kill
nohup python3 bot.py &
echo $! > bot.pid