
# System Imports
import sys
import vxi11

# Local Imports
import laserTools          as Tools
import laserServer_message as Message

# ===============================================================================
# Generator functions ===========================================================
# ===============================================================================

def start():
    return vxi11.Instrument("192.168.42.11")

def queue_handler(device, queue, trigger, end, db):
    trigger.wait()
    while not end.is_set():
        while (len(queue)>0):
            command = queue[0]["tosend"]
            response = run_command(device, command)
            Tools.verbose("Device response:\n" + response, level=1)
            parse_result = Message.parse("GEN " + command, response, db)
            queue[0]["toreturn"].set()
            queue.pop(0)
        trigger.clear()
        trigger.wait()

def run_command(device, command):
    response = device.ask(command)
    return response
