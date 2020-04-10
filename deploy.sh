#!/bin/bash

set -e

echo "=============================="
echo
echo "Version number?"
echo
echo "=============================="
echo -n  "> "
read version
echo "=============================="
echo
echo "Body of release?"
echo
echo "=============================="
echo -n "> "
read body
echo "installing..."
cd vanlifevue
npm i

echo "building..."

npm run build

echo "Zipping..."
cd -
mv vanlifevue/dist www

mkdir www/Settings www/Notif www/Lampor 

echo '<meta http-equiv="Refresh" content="0; url=https://192.168.0.97/" />' > www/Settings/index.html
echo '<meta http-equiv="Refresh" content="0; url=https://192.168.0.97/" />' > www/Notif/index.html
echo '<meta http-equiv="Refresh" content="0; url=https://192.168.0.97/" />' > www/Lampor/index.html

zip van.zip -r www/ BackendApi.py Mqtt_relay.py send.py update.sh
rm -r www

echo "Uploading..."


token=$(cat config.json | jq ".creds | .github_repo_token" | tr -d '"')
echo $token

json='{
  "tag_name": "'"$version"'", 
  "target_commitish": "master",
  "name": "'"Release $version"'",
  "body": "'"$body"'",
  "draft": false,
  "prerelease": false
  }'

# echo $json

# skapar
res=$(curl -X POST "https://api.github.com/repos/tokfrans03/VanLife/releases" -u "tokfrans03:$token" -d "$json")

# laddar upp
id=$(echo $res | jq ".id")

curl -X POST "https://uploads.github.com/repos/tokfrans03/VanLife/releases/$id/assets?name=van.zip" \
    -H "Content-Type: application/zip" \
    --data-binary "@van.zip" \
    -u "tokfrans03:$token" -q | jq

rm van.zip