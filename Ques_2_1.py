from socket import *
import threading

serverName = 'vayu.iitd.ac.in'
serverPort = 80
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
filename = "nikita.txt"
f= open(filename,"w+")

maxsize = 6488666
chunk = 100000

num = 0
i = 1
start = 0
helper = 0
request = 0;

while (num < maxsize):
  if (request < 100):
        if (num+chunk <= maxsize):
            sentence = 'GET /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in\r\nConnection: keep-alive\r\nRange: bytes='+ str(start) + '-' + str(chunk+start-1) + '\r\n\r\n'
            request += 1
            clientSocket.send(bytes(sentence,'utf-8'))

            size = chunk;
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
                f.write(modifiedSentence)
                count = count + len(modifiedSentence.encode('utf-8'))

            print(i)
            i = i+1
            num = num + chunk
            start = start + chunk
        else:
            sentence = 'GET /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in\r\nConnection: keep-alive\r\nRange: bytes='+ str(start) + '-' + str(maxsize-1) + '\r\n\r\n'
            request += 1
            clientSocket.send(bytes(sentence,'utf-8'))

            size = maxsize - start;
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
                f.write(modifiedSentence)
                count = count + len(modifiedSentence.encode('utf-8'))

            print(i)
            i = i+1
            num = num + chunk
            start = start + chunk
  else:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        request = 0
    
f.close()
clientSocket.close()
