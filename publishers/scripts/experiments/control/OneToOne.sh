#!/bin/bash

mvn exec:java -Dexec.mainClass="planiot.experiments.control.OneToOne" > trace/one_to_one_control.log
mvn exec:java -Dexec.mainClass="planiot.experiments.Stats" -Dexec.args="trace/one_to_one_control.log" >> trace/one_to_one_control.log