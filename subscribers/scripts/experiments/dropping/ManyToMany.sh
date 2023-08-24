#!/bin/bash

mvn exec:java -Dexec.mainClass="planiot.experiments.dropping.ManyToMany" > trace/many_to_many.log
mvn exec:java -Dexec.mainClass="planiot.experiments.Stats" -Dexec.args="trace/many_to_many.log" >> trace/many_to_many.log