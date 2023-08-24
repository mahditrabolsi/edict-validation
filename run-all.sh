#!/bin/sh
emqx foreground &
java -jar ../appPlaniotAPI/planiotapi.jar &
java -jar agent.jar &
wait