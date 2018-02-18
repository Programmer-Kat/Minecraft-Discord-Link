package com.programmerkat.helloworld;

import org.bukkit.plugin.PluginManager;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ConnectException;
import java.net.Socket;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.command.ConsoleCommandSender;
import org.bukkit.event.Listener;
import com.programmerkat.helloworld.ChatListener;

public class Main extends JavaPlugin implements Listener {
	ConsoleCommandSender console = Bukkit.getServer().getConsoleSender();
	static Main main;
	ServerThread serverThread;

	public void print(String text) {
		console.sendMessage(ChatColor.AQUA + text);
		// It will print in sserver's console.
	}

	@Override
	public void onEnable() {
		getServer().getPluginManager().registerEvents(this, this);
		PluginManager pm = this.getServer().getPluginManager();
		pm.registerEvents(new ChatListener(this), this);
		print("The plugin has loaded.");
		setupServer();
	}

	@Override
	public void onDisable() {
		//
	}

	@Override
	public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
		if (command.getName().equalsIgnoreCase("mycommand")) {
			sender.sendMessage("You ran /mycommand nya~!");
			return true;
		}
		return false;
	}

	public void broadCast(String s) {
		Bukkit.broadcastMessage(s);
	}

	public void sentToServer(String s) {
		serverThread.print(s);

	}

	public void setupServer() {
		new ServerThread(this).start();
	}
}

class ServerThread extends Thread {
	Main main;
	// ----------Program Settings----------------------------------------------
	static String serverAddress = "localhost";
	static int serverPort = 12345;
	public static String serverName = "Tekkit";
	// ----------End of Program
	// Settings----------------------------------------------
	PrintWriter out;
	BufferedReader input;
	Socket socket;
	long timeoutDuration = 5000;// Reconnection CoolDowns
	int reconnectAttempts = 0;
	boolean serverTimeOut = true;

	public ServerThread(Main main) {
		// super(str);
		this.main = main;
		main.serverThread = this;
	}

	public void print(String s) {
		try {
			out.println(s);
		} catch (Exception e) {
			serverTimeOut = true;
			ChatListener.print(e.toString());
			// e.toString();s

		}
	}

	public void run() {
		main.print("Server Thread Created");
		String response = "";
		while (true) {
			if (!serverTimeOut) {
				try {
					//Thread.sleep(5000);
					//print("<HEARTBEAT>");
					System.out.println("Waiting for Server Reply");
					response = input.readLine();
					System.out.println("Server has sent a reply");
					//System.out.println(response);
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					serverTimeOut = true;
				}
				if (response.compareTo("<HEARTBEAT>") == 0) {

				} else {
					if (response.compareTo("") != 0 || response != null) {
						//System.out.println(response);
						main.broadCast(response);
						response = "";//
					}

				}

			} else {
				try {
					connectToServer();
					serverTimeOut = false;
				} catch (Exception e) {
					main.print("Failed to Connect to Discord Bot");
					// e.printStackTrace();s
				}
				switch (reconnectAttempts) {
				case 0:
					timeoutDuration = 5000;
					break;
				case 12:
					timeoutDuration = 60000;// unable to reconnect in a minute, now trying to reconnect every minute.
				}//
				main.print("Lost Connection to Discord Bot retrying in " + timeoutDuration / 1000
						+ " seconds. Connection attempt " + reconnectAttempts);
				reconnectAttempts += 1;
				try {
					Thread.sleep(timeoutDuration);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
	}

	public void connectToServer() throws IOException, InterruptedException, ConnectException {
		// Get the server address from a dialog box.
		String serverAddress = "localhost";
		// Make connection and initialize streams
		socket = new Socket(serverAddress, 12345);
		reconnectAttempts = 0;
		input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		out = new PrintWriter(socket.getOutputStream(), true);
	}

	public void stopServer() {
		try {
			socket.close();
		} catch (Exception e) {
			// e.printStackTrace();
		}
	}

}