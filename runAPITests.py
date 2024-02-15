import threading
import subprocess
import time
import os
import signal

def runServer(pyScript):
    subprocess.run(["python", pyScript])

def runTests(pyScript):
    subprocess.run(["pytest", pyScript])
    

if __name__ == "__main__":
    serverThread = threading.Thread(target=runServer, args=("FileUpload.py",))
    testThread = threading.Thread(target=runTests, args=("TestApp.py",))
    
    serverThread.start()
    time.sleep(1)
    testThread.start()

    testThread.join()
    #serverThread.join()
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)