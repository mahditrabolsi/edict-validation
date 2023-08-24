package planiot;

import static planiot.common.Log.GEN;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;

import com.opencsv.CSVWriter;

import planiot.clients.Application;
import planiot.common.Configuration;
import planiot.common.JSONDataParser;
import planiot.common.Log;
import planiot.common.MessageResult;

public class Main {

	static final int EXPERIMENTATION_DURATION = 720000; // 12 minutes

	public static void main(String[] args) throws IOException, InterruptedException {
		String jsonData = new String(Files.readAllBytes(Paths.get(Configuration.SCENARIO)));
		ConcurrentHashMap<String, Application> applications = JSONDataParser.getApplications(jsonData);
		if (Log.ON) {
			GEN.info("{}", () -> "Subscribing applications");
		}
		applications.entrySet().forEach(app -> {
			app.getValue().connect(Configuration.BORKER_URL);
			app.getValue().subscribe();
		});
		System.out.println("**************************** subscribers START OF EXPERIMENT********************************");
		Thread.sleep(EXPERIMENTATION_DURATION);
		
		//Writing summary of results to result.csv
		String[] header = { "app, topic, category, priority, msgreceived, responsetime" };
		CSVWriter writer = new CSVWriter(new FileWriter("results/result.csv"));
		writer.writeNext(header);
		applications.entrySet().forEach(app -> {
			String appId = app.getValue().getClientId();
			String category = app.getValue().getCategory().name();
			String priority = String.valueOf(app.getValue().getPriority());
			String nbReceivedMsgs = String.valueOf(app.getValue().getNbMessagesReceived());
			try {
				HashMap<String, Double> latencyPerTopic = app.getValue().getLatencyPerTopic();
				for (String t : latencyPerTopic.keySet()) {
					if (Log.ON) {
						GEN.info("{}", () -> "Response time for: " + app.getValue().getClientId() + t + " = "
								+ latencyPerTopic.get(t));
					}
					String[] data = { appId, t, category, priority, nbReceivedMsgs,
							String.valueOf(latencyPerTopic.get(t)) };
					writer.writeNext(data);
				}
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		});
		writer.close();
		
		//Writing response time per message to csv file responsetimes.csv
//		CSVWriter responseTimesWriter = new CSVWriter(new FileWriter("results/responsetimes.csv"));
//		String[] csvHeader = { "timestamp, topic, latency" };
//		responseTimesWriter.writeNext(csvHeader);
//		applications.entrySet().forEach(app -> {
//			ArrayList<MessageResult> messageResultList = app.getValue().getResponseTimePerMessage();
//			for (MessageResult messageResult : messageResultList) {
//				String[] data = { Long.toString(messageResult.timestamp), messageResult.topic, 
//						Long.toString(messageResult.latency)};
//				responseTimesWriter.writeNext(data);
//			}
//		});
//		responseTimesWriter.close();
		
		System.out.println("*************************** subscribers END OF EXPERIMENT********************************");
//        applications.entrySet().forEach(app -> app.getValue().unsubscribe());
//        applications.entrySet().forEach(app -> app.getValue().disconnect());

		Thread.sleep(1000);
		System.exit(0);

	}

}
