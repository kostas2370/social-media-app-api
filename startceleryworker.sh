#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'

celery -A SocialMediaApi worker -l INFO --pool=solo
