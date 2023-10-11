import usocket as socket
import uselect as select
import time

def createSocket(server, port):
  try:
    web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     web_socket.setblocking(False)
    web_socket.bind((server,port))
    web_socket.listen(1)
    print('listening on', server, port)
    return web_socket
  except OSError as e:
    print("Socket not established")
    return "Not found"

def respondWebServer(client, response):
  data = response
  total_sent = 0
  data_size = len(response)
  while len(data):
    try:
      sent = client.send(data)
      total_sent += sent
      data = data[sent:]
      print('Sending data')
    except OSError as e:
#       client.close()
      break
#   assert total_sent == data_size  # True
  
def receiveWebServer(client):
  print("ghuss gaya receive func mein ")
  time_now = time.time()
  while True:
    request = client.recv(1024)
    if request != b'' or time.time()- time_now > 60:
      return request
    else:
      continue
  