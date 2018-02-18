package com.programmerkat.helloworld;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.ConsoleCommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;

public class ChatListener implements Listener{
	Main main;
	static ConsoleCommandSender console = Bukkit.getServer().getConsoleSender();
	
	public ChatListener(Main main) {
		this.main = main;
	}	

	public static void print(String text){
	    console.sendMessage(ChatColor.AQUA+text);
	    //It will print in sserver's console.
	}
	
	@EventHandler(priority = EventPriority.LOW)
	public void onPlayerChat(AsyncPlayerChatEvent event) {
		event.setCancelled(true);		
		Player player = event.getPlayer();
		//player.sendMessage(event.getPlayer().getName() + ": " + event.getMessage());
		//System.out.println(event.getPlayer().getName() +  ": " + event.getMessage());
		main.sentToServer(event.getPlayer().getName() +  ": " + event.getMessage());
		main.broadCast(event.getPlayer().getName() + ": " + event.getMessage());
		//if(player.getName().equalsIgnoreCase("xl_callum_lx"));		
	}	
}
