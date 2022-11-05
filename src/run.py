import subprocess
import time

time.sleep(120)

process1 = subprocess.Popen(["python", "client_1.py"]) 
# process2 = subprocess.Popen(["python", "client_2.py"])
# process3 = subprocess.Popen(["python", "client_3.py"])
# process4 = subprocess.Popen(["python", "client_4.py"])
# process5 = subprocess.Popen(["python", "client_5.py"])

process1.wait() 
# process2.wait()
# process3.wait()
# process4.wait()
# process5.wait()