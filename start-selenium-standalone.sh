#!/usr/bin/env bash
#
# IMPORTANT: Change this file only in directory Standalone!

java ${JAVA_OPTS} -jar /opt/selenium/selenium-server.jar standalone \
  --relax-checks true ${SE_OPTS}
