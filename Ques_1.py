from socket import *
import os
import hashlib
import time

start_time = time.time()
"""
def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
"""

#serverName = 'vayu.iitd.ac.in'
serverName = 'norvig.com'
serverPort = 80
size = 6488666
sum = '70a4b9f4707d258f559f91615297a3ec'
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
   
filename = "output.txt"
f= open(filename,"w+")

sentence = 'GET /big.txt HTTP/1.1\r\nHost: '+serverName+'\r\n\r\n'
clientSocket.send(bytes(sentence,'utf-8'))

count = 0;
modifiedSentence = ""
i = 1
while (count < size):
   response = clientSocket.recv(4096).decode()
   #print(i)
   #i = i+1
   line = response.split('\r\n\r\n')
   if len(line) == 2:
       modifiedSentence = line[1]
       print(line[0])
       f.write(modifiedSentence)
   else:
        modifiedSentence = line[0]
        f.write(modifiedSentence)
   count = count+ len(modifiedSentence.encode('utf-8'))
   
f.close()

"""
response = os.popen('md5 '+ '/Users/nikitabhamu/Desktop/' + filename)
md5sum = response.readlines()
str = 'MD5 (/Users/nikitabhamu/Desktop/' + filename + ') = 70a4b9f4707d258f559f91615297a3ec\n'
"""
fl = open(filename,"rb")
byt = fl.read()
md5sum = hashlib.md5(byt).hexdigest()
fl.close()

while (md5sum != sum):
    clientSocket.send(bytes(sentence,'utf-8'))
    f= open(filename,"w+")
    count = 0;
    modifiedSentence = ""
    i = 1
    while (count < size):
           response = clientSocket.recv(4096).decode()
           #print(i)
           #i = i+1
           line = response.split('\r\n\r\n')
           if len(line) == 2:
               modifiedSentence = line[1]
               print(line[0])
               f.write(modifiedSentence)
           else:
                modifiedSentence = line[0]
                f.write(modifiedSentence)
           count = count+ len(modifiedSentence.encode('utf-8'))
    f.close()
     
    fl = open(filename,"rb")
    byt = fl.read()
    md5sum = hashlib.md5(byt).hexdigest()
    fl.close()
    
#print("\nContent-length downloaded : "+str(count))
print("MD5 sum of the file is : "+md5sum)
print("Time required : ",time.time() - start_time, "seconds\n")
clientSocket.close()
