import subprocess
import time


time.sleep(120)

process1 = subprocess.Popen(["python", "firewall_PF.py"]) 
process2 = subprocess.Popen(["python", "dpi.py"])
process3 = subprocess.Popen(["python", "load_balancer.py"])
process4 = subprocess.Popen(["python", "plain_PF.py"])

process1.wait() 
process2.wait()
process3.wait()
process4.wait()