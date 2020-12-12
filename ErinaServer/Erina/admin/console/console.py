import sys
import time
import json
import shlex
import asyncio
import threading
import subprocess
import websockets
import fcntl, os

async def _asyncMessageSending(websocketConnection, message, code):
    try:
        await websocketConnection.send(json.dumps({"message": str(message), "code": code})) # Sends messages asynchronously (WebSocket Object is async)
    except:
        print("Attempted message sending failed")

def _sendMessage(websocketConnection, message, code):
    """
    Synchronous function which sends starts the _asyncMessageSending function
    """
    asyncio.set_event_loop(asyncio.new_event_loop()) # Creates another async event loop because multi-threaded programs usually have problems with them
    asyncio.get_event_loop().run_until_complete(_asyncMessageSending(websocketConnection, message, code)) # Starts the _asyncMessageSending function

def _checkOutput(process, websocketConnection):
    """
    Checks the output of stdout and stderr to send it to the WebSocket client
    """
    while process.poll() is None: # while the process isn't exited
        try:
            output = process.stdout.read() # Read the stdout PIPE (which contains stdout and stderr)
        except:
            output = None
        if output:
            messageSendingThread = threading.Thread(target=_sendMessage, args=[websocketConnection, output.decode("utf-8"), 0]) # Creates another thread to send the message (continue reading stdout even when sending a message)
            messageSendingThread.daemon = True # Kill the thread if main thread is killed
            messageSendingThread.start() # Start the thread
        time.sleep(0.1) # Wait a lil bit to avoid confusion from the computer
    ### EXITED THE LOOP ### (process exited)
    messageSendingThread = threading.Thread(target=_sendMessage, args=[websocketConnection, f"ErinaConsole: The process has exited with code {str(process.returncode)}", process.returncode]) # Send a disconnection message
    messageSendingThread.daemon = True
    messageSendingThread.start()

async def console_connection(ws, path):
    """
    WebSocket Handling Script
    """
    if path == '/ErinaConsole': # If connecting to ErinaConsole
        try:
            print("> New ErinaConsole connection!")
            bash = False
            if os.path.isfile("/bin/bash"):
                bash = True
                currentProcess = subprocess.Popen(shlex.split("/bin/bash"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Open a bash prompt
            else:
                currentProcess = subprocess.Popen(shlex.split("/bin/sh"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Open a shell prompt
            fcntl.fcntl(currentProcess.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK) # Non blocking stdout and stderr reading
            newReadingThread = threading.Thread(target=_checkOutput, args=[currentProcess, ws]) # Start checking for new text in stdout and stderr
            newReadingThread.daemon = True
            newReadingThread.start()
            if bash:
                await ws.send(json.dumps({"message": f"ErinaConsole: Connection successfully established (bash) with PID: {str(currentProcess.pid)}", "code": 0})) # Send a message to notifiy that the process has started
            else:
                await ws.send(json.dumps({"message": f"ErinaConsole: Connection successfully established (sh) with PID: {str(currentProcess.pid)}", "code": 0})) # Send a message to notifiy that the process has started
            async for message in ws:
                try:
                    data = json.loads(message) # retrieve a message from the client
                    if "input" in data:
                        userInput = str(data["input"])
                        if userInput != "exit":
                            currentProcess.stdin.write(str(userInput + "\n").encode("utf-8")) # Write user input (ws client) to stdin
                            currentProcess.stdin.flush() # Run the command
                            print("ErinaConsole: Admin ran command > " + str(userInput))
                        else:
                            currentProcess.terminate() # If "exit" sent by client, terminate the process
                except:
                    await ws.send(json.dumps({"message": f"ErinaConsole: An error occured ({str(sys.exc_info()[0])})", "code": -1}))
        except:
            await ws.send(json.dumps({"message": f"ErinaConsole: An error occured ({str(sys.exc_info()[0])})", "code": -1}))
        finally:
            if currentProcess.poll() is None:
                currentProcess.terminate()
            print("< ErinaConsole disconnected")





def serveWebSocketServer():
    try:
        print("ErinaConsole: Serving WS Server...")
        ErinaConsole = websockets.serve(console_connection, "127.0.0.1", 5555) # Server the WS Server (on port 5555 for now)
        asyncio.get_event_loop().run_until_complete(ErinaConsole) # Run the async function
        asyncio.get_event_loop().run_forever() # Run the WS Server forever
    except KeyboardInterrupt:
        print("ErinaConsole: Disconnection...")
    except:
        print("ErinaConsole: An error occured.")
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])