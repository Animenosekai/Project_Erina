import sys
import json
import asyncio
import subprocess
import websockets

async def console_connection(ws, path):
    if path == '/ErinaConsole':
        try:
            print("> New ErinaConsole connection!")
            await ws.send(json.dumps({"message": "ErinaConsole: Connection successfully established", "code": 0}))
            async for message in ws:
                try:
                    data = json.loads(message)
                    if "input" in data:
                        userInput = str(data["input"])
                        if userInput != "exit":
                            process = subprocess.run(userInput, text=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=False, shell=True)
                            await ws.send(json.dumps({"message": str(process.stdout)[:-1], "code": process.returncode}))
                except:
                    await ws.send(json.dumps({"message": f"ErinaConsole: An error occured ({str(sys.exc_info()[0])})", "code": -1}))
        except:
            await ws.send(json.dumps({"message": f"ErinaConsole: An error occured ({str(sys.exc_info()[0])})", "code": -1}))
        finally:
            print("< ErinaConsole disconnected")
            #await ws.send(json.dumps({"message": "ErinaConsole: Disconnection...", "code": 0}))

ErinaConsole = websockets.serve(console_connection, "127.0.0.1", 5555)
asyncio.get_event_loop().run_until_complete(ErinaConsole)
asyncio.get_event_loop().run_forever()

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