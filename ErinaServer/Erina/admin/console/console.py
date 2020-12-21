import sys
import time
import json
import shlex
import threading
import subprocess
import fcntl, os
from Erina.erina_log import log
from ErinaServer.Server import ErinaServer
from flask_sockets import Sockets
from ErinaServer.Erina.auth import authManagement

ErinaSockets = Sockets(ErinaServer)

@ErinaSockets.route("/ErinaConsole")
def ErinaConsole(ws):
    currentProcess = None
    message = ws.receive()
    try:
        data = json.loads(message) # retrieve a message from the client
        if "token" in data:
            tokenVerification = authManagement.verifyToken(data)
            if tokenVerification.success:
                log("ErinaAdmin", "> New ErinaConsole connection!")
                bash = False
                if os.path.isfile("/bin/bash"):
                    bash = True
                    currentProcess = subprocess.Popen(shlex.split("/bin/bash"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Open a bash prompt
                else:
                    currentProcess = subprocess.Popen(shlex.split("/bin/sh"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Open a shell prompt
                fcntl.fcntl(currentProcess.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK) # Non blocking stdout and stderr reading
                threading.Thread(target=_checkOutput, args=[currentProcess, ws], daemon=True).start() # Start checking for new text in stdout and stderr
                if bash:
                    ws.send(json.dumps({"message": f"ErinaConsole: Connection successfully established (bash) with PID: {str(currentProcess.pid)}", "code": 0})) # Send a message to notifiy that the process has started
                else:
                    ws.send(json.dumps({"message": f"ErinaConsole: Connection successfully established (sh) with PID: {str(currentProcess.pid)}", "code": 0})) # Send a message to notifiy that the process has started
            else:
                ws.send(json.dumps({"message": f"ErinaConsole: Authentification Error: {str(tokenVerification)}", "code": 400}))
        else:
            ws.send(json.dumps({"message": f"ErinaConsole: Your connection could not be authentificated", "code": 400}))
    except:
        try:
            ws.send(json.dumps({"message": f"ErinaConsole: An error occured ({str(sys.exc_info()[0])}) while creating a new ErinaConsole instance", "code": -1}))
        except:
            log("ErinaAdmin", "ErinaConsole >>> Failed to send a message")
    while not ws.closed:
        message = ws.receive()
        try:
            data = json.loads(message) # retrieve a message from the client
            tokenVerification = authManagement.verifyToken(data)
            if tokenVerification.success:
                if "input" in data:
                    userInput = str(data["input"])
                    #if userInput != "exit":
                    currentProcess.stdin.write(str(userInput + "\n").encode("utf-8")) # Write user input (ws client) to stdin
                    currentProcess.stdin.flush() # Run the command
                    log("ErinaAdmin", "ErinaConsole >> Admin ran command > " + str(userInput))
                    """
                    else:
                        currentProcess.terminate() # If "exit" sent by client, terminate the process
                    """
            else:
                ws.send(json.dumps({"message": f"ErinaConsole: Authentification Error: {str(tokenVerification)}", "code": 400}))
        except:
            try:
                ws.send(json.dumps({"message": f"ErinaConsole: An error occured ({str(sys.exc_info()[0])})", "code": -1}))
            except:
                log("ErinaAdmin", "ErinaConsole >>> Failed to send a message")
    if currentProcess is not None:
        if currentProcess.poll() is None:
            currentProcess.terminate()
    log("ErinaAdmin", "< ErinaConsole disconnected")

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
            websocketConnection.send(json.dumps({"message": output.decode("utf-8"), "code": 0})) # Send the new output
        time.sleep(0.1) # Wait a lil bit to avoid confusion from the computer
    ### EXITED THE LOOP ### (process exited)
    websocketConnection.send(json.dumps({"message": f"ErinaConsole: The process has exited with code {str(process.returncode)}", "code": process.returncode})) # Send a disconnection message