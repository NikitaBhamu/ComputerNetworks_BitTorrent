from socket import *
import threading
import hashlib
import time

serverName = 'vayu.iitd.ac.in'
serverPort = 80
chunk = 100000
maxsize = 6488666
num_threads = 3
sum = '70a4b9f4707d258f559f91615297a3ec'
Strings = []
for i in range((maxsize//chunk) + 1):
   Strings.append("")
times = []
for i in range((maxsize//chunk) + 1):
   times.append(0)

def checkerfunc(times):
  for t in times:
    if (t != 1):
       return False
  return True

def func(clientSocket, byte_start, byte_end, i):
    num = 0
    start = byte_start
    size = byte_end-byte_start+1
    request = 0

    while(num < byte_end - byte_start+1):
       try:
           if(request < 50):
                   if(start+chunk-1 <= byte_end):
                       sentence = 'GET /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in\r\nConnection: keep-alive\r\nRange: bytes='+ str(start) + '-' + str(chunk+start-1) + '\r\n\r\n'
                       request += 1
                       clientSocket.send(bytes(sentence,'utf-8'))

                       line_obt = ""
                       size = chunk
                       count = 0
                       while(count < size):
                          response = clientSocket.recv(4096)
                          sentence = response.decode()
                          modifiedSentence = ""
                          line = sentence.split('\r\n\r\n')
                          if (len(line)==2):
                             modifiedSentence = line[1]
                          else:
                             modifiedSentence = line[0]
                          #f.write(modifiedSentence)
                          line_obt = line_obt + modifiedSentence
                          count = count + len(modifiedSentence.encode('utf-8'))

                       Strings[i-1] = line_obt
                       times[i-1] += 1
                       #print(i)
                       i = i+1
                       num = num + chunk
                       start = start + chunk

                   else:
                       sentence = 'GET /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in\r\nConnection: keep-alive\r\nRange: bytes='+ str(start) + '-' + str(byte_end) + '\r\n\r\n'
                       request += 1
                       clientSocket.send(bytes(sentence,'utf-8'))

                       line_obt = ""
                       size = byte_end-start+1
                       count = 0
                       while(count < size):
                          response = clientSocket.recv(4096)
                          sentence = response.decode()
                          modifiedSentence = ""
                          line = sentence.split('\r\n\r\n')
                          if (len(line)==2):
                             modifiedSentence = line[1]
                          else:
                             modifiedSentence = line[0]
                          #f.write(modifiedSentence)
                          line_obt = line_obt + modifiedSentence
                          count = count + len(modifiedSentence.encode('utf-8'))

                       Strings[i-1] = line_obt
                       #print(i)
                       times[i-1] += 1
                       i = i+1
                       num = num + chunk
                       start = start + chunk
           else:
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.settimeout(8)
                clientSocket.connect((serverName,serverPort))
                request = 0
       except:
           continue

def thread_making():
   chunk_size = chunk
   chunks = 6488666//chunk;
   chunks_to_1_thread = chunks//num_threads;

   start = 0
   chunk_num = 1
   List = []
   for j in range(num_threads-1):
     clientSocket = socket(AF_INET, SOCK_STREAM)
     clientSocket.connect((serverName,serverPort))
     clientSocket.settimeout(8)
     t = threading.Thread(target=func, args=(clientSocket,start,start + (chunks_to_1_thread*chunk_size) -1,chunk_num,))
     List.append(t)
     chunk_num = chunk_num + chunks_to_1_thread
     start = start + (chunks_to_1_thread*chunk_size)

   clientSocket = socket(AF_INET, SOCK_STREAM)
   clientSocket.connect((serverName,serverPort))
   clientSocket.settimeout(8)
   t_final = threading.Thread(target=func, args=(clientSocket,start,maxsize-1,chunk_num,))
   List.append(t_final)
   return List

start_time = time.time()

list = thread_making()
for th in list:
  th.start()
for th in list:
  th.join()
  

f = open("ankit.txt","w+")
for l in Strings:
   f.write(l)
f.close()

fl = open("ankit.txt","rb")
byt = fl.read()
md5sum = hashlib.md5(byt).hexdigest()
fl.close()

while(md5sum != sum):
   list = thread_making()
   for th in list:
     th.start()
   for th in list:
     th.join()
   
   f = open("ankit.txt","w+")
   for l in Strings:
      f.write(l)
   f.close()
   
   fl = open("ankit.txt","rb")
   byt = fl.read()
   md5sum = hashlib.md5(byt).hexdigest()
   fl.close()
   


end_time = time.time()
print('Done!')


print("All chunks are downloaded once : "+ str(checkerfunc(times)))
print("The MD5sum of the output file is : "+md5sum)
print("The number of threads are : "+str(num_threads))
print("Time taken : ",end_time-start_time)
