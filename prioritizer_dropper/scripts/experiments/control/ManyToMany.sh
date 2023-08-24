#!/bin/bash

mvn exec:java -Dexec.mainClass="planiot.experiments.control.ManyToMany" > trace/prio/many_to_many_control$1.log
mvn exec:java -Dexec.mainClass="planiot.experiments.Stats" -Dexec.args="trace/many_to_many_control.log" >> trace/prio/many_to_many_control$1.log