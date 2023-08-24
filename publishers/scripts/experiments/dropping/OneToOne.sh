#!/bin/bash

mvn exec:java -Dexec.mainClass="planiot.experiments.dropping.OneToOne" > trace/one_to_one.log
mvn exec:java -Dexec.mainClass="planiot.experiments.Stats" -Dexec.args="trace/one_to_one.log" >> trace/one_to_one.log