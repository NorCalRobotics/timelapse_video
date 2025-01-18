#!/usr/bin/env bash

HEUR_HN=$(sed -ne 's/^[ \t]*["'"'"']vidcap_camera_index["'"'"'][ \t]*:[ \t]*["'"'"']http:\/\/\([^\/]*\).*["'"'"'].*$/\1/p' config.json)
HOSTNAME="${HEUR_HN:-10.10.87.118}"

until ping -c 1 $HOSTNAME ; do
    sleep 1
done
