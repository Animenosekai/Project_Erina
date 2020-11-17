import sys
import json
import shlex
import time
import asyncio
import subprocess
import websockets
import threading
import fcntl, os

bufferIndex = 0

async def _asyncMessageSending(websocketConnection, message, code):
    await websocketConnection.send(json.dumps({"message": str(message), "code": code}))

def _sendMessage(websocketConnection, message, code):
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(_asyncMessageSending(websocketConnection, message, code))

def _checkOutput(process, websocketConnection):
    print("ErinaConsole: Start reading...")
    while process.poll() is None:
        try:
            output = process.stdout.read()
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            output = None
        if output:
            messageSendingThread = threading.Thread(target=_sendMessage, args=[websocketConnection, output.decode("utf-8"), 0])
            messageSendingThread.daemon = True
            messageSendingThread.start()
        time.sleep(0.1)
    print("ErinaConsole: Process exited")
    messageSendingThread = threading.Thread(target=_sendMessage, args=[websocketConnection, "ErinaConsole: The process has exited", process.returncode])
    messageSendingThread.daemon = True
    messageSendingThread.start()

async def console_connection(ws, path):
    if path == '/ErinaConsole':
        try:
            print("> New ErinaConsole connection!")
            currentProcess = subprocess.Popen(shlex.split("bash"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            fcntl.fcntl(currentProcess.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            newReadingThread = threading.Thread(target=_checkOutput, args=[currentProcess, ws])
            newReadingThread.daemon = True
            newReadingThread.start()
            await ws.send(json.dumps({"message": "ErinaConsole: Connection successfully established", "code": 0}))
            async for message in ws:
                try:
                    data = json.loads(message)
                    if "input" in data:
                        userInput = str(data["input"])
                        if userInput != "exit":
                            """
                            process = subprocess.run(userInput, text=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=False, shell=True)
                            await ws.send(json.dumps({"message": str(process.stdout)[:-1], "code": process.returncode}))
                            """
                            """
                            sendingMessage = ""
                            for index, message in enumerate(currentProcess.stdout):
                                if index < bufferIndex:
                                    continue
                                else:
                                    sendingMessage += message
                            """
                            currentProcess.stdin.write(str(userInput + "\n").encode("utf-8"))
                        else:
                            currentProcess.terminate()
                except:
                    await ws.send(json.dumps({"message": f"ErinaConsole: An error occured ({str(sys.exc_info()[0])})", "code": -1}))
        except:
            await ws.send(json.dumps({"message": f"ErinaConsole: An error occured ({str(sys.exc_info()[0])})", "code": -1}))
        finally:
            print("< ErinaConsole disconnected")
            #await ws.send(json.dumps({"message": "ErinaConsole: Disconnection...", "code": 0}))

try:
    print("Serving WS Server...")
    ErinaConsole = websockets.serve(console_connection, "127.0.0.1", 5555)
    asyncio.get_event_loop().run_until_complete(ErinaConsole)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print("Disconnection...")
except:
    print("An error occured.")
"""
while True:
    try:
        try:
            userInput = input(f"ErinaConsole >> ")
            if userInput != "exit":
                process = subprocess.run(userInput, text=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=False, shell=True)
                if process.returncode != 0:
                    print(f"ErinaConsole: [WARNING] Process terminated with code {str(process.returncode)}")
                print(process.stdout)
            else:
                break
        except KeyboardInterrupt:
            print("")
            print("ErinaConsole: KeyboardInterrupt")
            continue
    except KeyboardInterrupt:
        print("")
        print("ErinaConsole: KeyboardInterrupt")
        continue
"""