import subprocess

process1 = subprocess.Popen(["python", "firewall_PF.py"]) 
process2 = subprocess.Popen(["python", "dpi.py"])
process3 = subprocess.Popen(["python", "plain_PF.py"])

process1.wait() 
process2.wait()
process3.wait()