#!/bin/bash
_401=$(echo ${1} | jq ".detail" |  tr -d '"')
_404=$(echo ${1} | jq ".message" |  tr -d '"')
STATUS=$(echo ${1} | jq ".tag_status" |  tr -d '"')

if [[ "$_404" == *"404"* ]]; then
  echo "Version is valid"
  exit 0
elif [[ "$STATUS" == "active" ]]; then
  echo "ABORTING: Version already exists"
  echo "ABORTING: Change the version.yaml file"
  exit 1
elif [[ "$_401" == "unauthorized" ]]; then
  echo "ABORTING: Unauthorized response"
  echo "ABORTING: Must set a valid docker hub token in gh actions secrets"
  exit 1
else
  echo "ABORTING: Unexpected response"
  exit 1
fi
