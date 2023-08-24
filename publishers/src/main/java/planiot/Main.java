package planiot;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.eclipse.paho.client.mqttv3.MqttException;

import com.opencsv.CSVWriter;

import planiot.clients.Device;
import planiot.common.Configuration;
import planiot.common.JSONDataParser;
import planiot.common.PublishMessage;
import planiot.commonPriorities.Statistics;

public class Main {
	static final int EXPERIMENT_DURATION = 300000; // 5 minutes

	public static void main(String[] args) throws IOException, InterruptedException, MqttException {
		String jsonData = new String(Files.readAllBytes(Paths.get(Configuration.SCENARIO)));
		HashMap<String, Device> devices = JSONDataParser.getDevices(jsonData);
		CSVWriter writer = new CSVWriter(new FileWriter("results/result.csv"));
		String[] header = { "device", "topic", "nbMessages" };
		writer.writeNext(header);
		writer.close();
		List<Thread> threads = new ArrayList<>();
		devices.entrySet().forEach(dev -> {
			try {
				dev.getValue().connect(Configuration.BROKER_URL);
			} catch (IOException e) {
				e.printStackTrace();
			}
		});
		// 1 publisher
//        Device device = devices.get("topic1_source");
//        Thread thread = new Thread(new PublishMessage(device, experimentDuration));
//    	threads.add(thread);
//        thread.start();
//        
//        threads.forEach(t -> { try {
//        	t.join();
//        } catch (Exception e) {
//        	e.printStackTrace();
//        }
//        });
		System.out.println("**************************** publishers START OF EXPERIMENT********************************");
		for (Map.Entry<String, Device> d : devices.entrySet()) {
			Thread thread = new Thread(new PublishMessage(d.getValue(), EXPERIMENT_DURATION));
			threads.add(thread);
			thread.start();
		}
		threads.forEach(thread -> {
			try {
				thread.join();
			} catch (Exception e) {
				e.printStackTrace();
			}
		});
		devices.entrySet().forEach(dev -> dev.getValue().disconnect());
		Statistics.addSeperation();
		Thread.sleep(1000); 
		System.out.println(Main.class.getCanonicalName()
				+ " ***************************publishers END OF EXPERIMENT********************************");
		System.exit(0);
	}
}
