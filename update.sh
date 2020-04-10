#!/bin/sh

echo "Upgraderar till $1"

wget $1 -O update.zip # hämta första argumentet (zip fil)

unzip -o update.zip -d vanlife/ # extrahera och skriv äver utan att fråga

# sudo systemctl restart Backendapi # starta om saker
# sudo systemctl restart vanlife

rm update.zip
