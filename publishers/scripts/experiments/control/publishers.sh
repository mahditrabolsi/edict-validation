#!/bin/bash

mvn exec:java -Dexec.mainClass="planiot.experiments.control.Publishers" > trace/prio/publishers$1.log
