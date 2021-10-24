cd /home/nicholas/Downloads
sudo rm -rf flipClock

git clone git@github.com:nicknamemok/flipClock.git

cd /home/nicholas/RPi
sudo rm -rf flipClock

sudo mv -u /home/nicholas/Downloads/flipClock .
cd /flipClock

python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt

deactivate