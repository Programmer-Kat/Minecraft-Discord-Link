#Author Kat
#Version 0.1

#Bot Settings
botToken = 'NDA5Mjk5OTk3ODc2NjgyNzkz.DVcmbA.YE1DZ2fSxVYH68xx4irbjJAPWKw'
botStatus = 'MineBot'
DiscordServerIp = "127.0.0.1"
DiscordServerPort = 12345
#End of Bot Settings



#Global Variables please don't touch these :>
lastMessage = 'I Wonder whats for Dinner?'
linkRunning = False
#End of Global Variables

print('Starting Server')

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):	
    import sys
    global lastMessage
    running = True
    while(running):
	    try:
	    	input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)
	    	#siz = sys.getsizeof(input_from_client_bytes)
	    	#if  siz >= MAX_BUFFER_SIZE:
		    #    print("The length of input is probably too long: {}".format(siz))
	    	input_from_client = input_from_client_bytes.decode("utf8").rstrip()
	    	#if input_from_client == "<HEARTBEAT>":
	    	#	print("Got a HeartBeat from " + ip)
	    	#else:
	    	lastMessage = input_from_client
	    	#res = do_some_stuffs_with_input(input_from_client)
	    	#print("Result of processing {} is: {}".format(input_from_client, res))
	    	#if lastMessage != "" and lastMessage != "<HEARTBEAT>":
	    		#print(lastMessage)
	    		#vysl = input_from_client.encode("utf8")  # encode the result string
	    		#conn.sendall(vysl)  # send it to client
	    except:
	    	print("Connection Terminated from client ")
	    	running = False

    conn.close()
    print('Connection ' + ip + ':' + port + " ended")

def sendMessageToMineCraft(outGoingMessage):
	outGoingMessage += "\n"
	outGoingMessage = outGoingMessage.encode("utf8")  # encode the result string
	conn.sendall(outGoingMessage)  # send it to client


def start_server():
    global conn
    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind((DiscordServerIp, DiscordServerPort))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terrible error!")
            import traceback
            traceback.print_exc()
    soc.close()

def launchServer():	
	from threading import Thread
	try:
		Thread(target=start_server).start()
	except:
		print("Terible error!")
		import traceback
		traceback.print_exc()
launchServer()  
print('Server Setup Complete ')




print('Starting bot')
# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio

from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Basic Bot by Kat", command_prefix="-", pm_help = False)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Created by Kat')
	return await client.change_presence(game=discord.Game(name=botStatus)) #This is buggy, let us know if it doesn't work.

@client.command()
async def startLink(*args):
	global linkRunning
	linkRunning = True
	await client.say("Server Link Running")
	print('Link has started!')
	#insert Link Code here
	running = True
	staleMessage = ""
	while(linkRunning):
		await asyncio.sleep(0.1)
		if(staleMessage != lastMessage):
			await client.say(lastMessage)
			staleMessage = lastMessage
	print('Link has stopped Running')

@client.command()
async def stopLink(*args):
	global linkRunning
	if(linkRunning):
		linkRunning = False
		await client.say("Server Link has been DESTROYED!")
	else:
		await client.say("Server Link was not running. :/")

@client.listen()
async def on_message(message):
	newMessage = "[Discord] "
	newMessage += str(message.author).split("#")[0] + ": "
	newMessage += str(message.content)
	if(message.author.bot is not True):
		sendMessageToMineCraft(newMessage)

	print(newMessage)
	if "Kat 2.0" in message.content:
		channel = message.channel
		print('Mew?')
		await client.send_message(message.channel, "Mew!")
	client.process_commands(message)


client.run(botToken)








#TODO
#Add Discord Chat events and relay that to the connected Servers.
#Create Java plugin client
#Connect Java Plugin Client to Discord Bot
#Enable Java plugin to handle ingame Chat events.
#Enable Java Plugin to receive and say data from Discord Bot.
