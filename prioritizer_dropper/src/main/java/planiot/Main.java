package planiot;

import java.io.IOException;

import org.eclipse.paho.client.mqttv3.MqttException;

import planiot.agent.Agent;
import planiot.commonPriorities.APIServices;

public class Main {
	public static void main(final String[] args) throws MqttException, IOException, InterruptedException {
		Thread.sleep(5000);
		APIServices apiServices = new APIServices();
		apiServices.addAgentUser();
		Agent agent = new Agent();
		agent.start();
		System.out.println("agent activated");
		//TODO: save JVM performance data
		/*
		ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();
		executor.scheduleAtFixedRate(new Thread (new Instrument()), 0, 30, TimeUnit.SECONDS);
		*/
		Thread.sleep(10000000);
		System.out.println("agent de-activated");
		System.exit(0);
	}
}
