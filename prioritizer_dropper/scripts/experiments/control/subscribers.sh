#!/bin/bash

mvn exec:java -Dexec.mainClass="planiot.experiments.control.Subscribers" > trace/prio/subscribers$1.log