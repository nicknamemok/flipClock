VERSION=$(curl --silent https://api.github.com/repos/nicknamemok/flipClock/tags \
| grep -m 1 tarball_url \
| cut -d '"' -f 4 \
| awk -F'/' '{print $8}')
TARGET=/home/nicholas/Downloads
APP_NAME=flipClock

# Ensure we're downloading to the Downloads folder
cd /home/nicholas/Documents/

wget https://github.com/nicknamemok/flipClock/archive/refs/tags/v1.tar.gz

tar -xzf v1.tar.gz -C /home/nicholas/Documents
# # Delete the tar zip file to declutter Downloads folder
rm -rf v1.tar.gz

# # Renames the app, stripping away the version name and overwriting the existing app.
# # Thereby ensuring only the most updated app remains in the TARGET folder
# rm -rf /home/nicholas/Downloads/flipClock

# mv -u /home/nicholas/Documents/flipClock${VERSION} /home/nicholas/Downloads/flipClock
# cd /home/nicholas/Downloads/flipClock

# # Creates and activates virtual environment
# python3 -m venv venv
# source venv/bin/activate
# # Installs necessary packages so the application is good to go
# pip3 install -r requirements.txt

# deactivate

# # Generate / Update shortcuts
# . 7-generate_shortcuts.sh

# zenity --info --title 'Update complete!' --text "Update complete! Application version: ${VERSION}"  --width=500 --height=200 --timeout=3