#!/bin/bash

rm -rf ./lambda_code_uri
mkdir lambda_code_uri
cd lambda_code_uri && mkdir chatytt/ && cd ..
cp -r ../chatytt/. ./lambda_code_uri/chatytt
cp -r ../server/. ./lambda_code_uri/server

poetry export --without-hashes -f requirements.txt --output requirements.txt
mv requirements.txt ./lambda_code_uri/
