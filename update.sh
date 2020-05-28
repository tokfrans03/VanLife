#!/bin/sh

echo "Upgraderar till $1"

wget $1 -O update.zip # hämta första argumentet (zip fil)

unzip -o update.zip -d . # extrahera och skriv äver utan att fråga
chown -R pi:pi .
cp -r www/* /var/www/html/

systemctl restart Backendurl.service # starta om saker
# sudo systemctl restart vanlife

# rm update.zip
