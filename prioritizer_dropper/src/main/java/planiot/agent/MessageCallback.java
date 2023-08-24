package planiot.agent;

import static planiot.common.Log.PRIORITY;

import java.util.Optional;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import planiot.common.Log;
import planiot.commonPriorities.Application;

public class MessageCallback implements MqttCallback {

	@Override
	public void connectionLost(final Throwable cause) {
		if (Log.ON) {
			PRIORITY.warn("{}", () -> "agent's client lost connection to the broker");
		}
	}

	/*
	 * The message will be queued in this function in the adequate priority Queue
	 * based on the app's priority
	 */
	@Override
	public void messageArrived(final String topic, final MqttMessage message) throws Exception {
		String subTopic = topic.split("/")[0] + "/" + topic.split("/")[1];
		String appId = topic.split("/")[1];
		Optional<Application> appli = Agent.payloadJson.getAppById(appId);
		if (appli.isEmpty()) {
			throw new IllegalArgumentException("pb in getting application by id(" + appId + ")");
		}
		int appPriority = appli.get().getPriority();
		Agent.priorityQueue.enqueue(appPriority, new MessageToRepublish(subTopic, new String(message.getPayload())));
	}

	@Override
	public void deliveryComplete(final IMqttDeliveryToken token) {
		if (Log.ON) {
			PRIORITY.warn("{}", () -> "message well delivered to the agent ");
		}
	}

}
