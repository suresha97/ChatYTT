#!/bin/bash

rm -rf ./code_uri
mkdir code_uri
cd code_uri && mkdir chatytt/ && cd ..

cp -r ../chatytt/. ./code_uri/chatytt
cp -r ../server/. ./code_uri/server

poetry export --without-hashes -f requirements.txt --output requirements.txt
mv requirements.txt ./code_uri/
