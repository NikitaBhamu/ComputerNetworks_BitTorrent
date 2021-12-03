filename = "MyFile.txt"
file = open(filename, "w")
request = 'GET /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in\r\nConnection: keep-alive\r\nRange: bytes=0-999\r\n\r\n'
file.write(request)
print("\nUse the filename : << "+filename + " >> in the cat command\n")
file.close()
