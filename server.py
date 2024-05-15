import socket
import threading
from fileHandling import *
from KeyClient import *

HOST = "127.0.0.1"  
PORT = 3333  
SECRET = ['key1', 'key2', 'key3']
REPO_KEY = "AnaisND"

class Request:
  def __init__(self, command, params):
    self.type = command
    self.params = params

class Response:
  def __init__(self, status, payload):
    self.status = status
    self.payload = payload

def serialize(response):
  return bytes(str(response.status) + ' ' + response.payload, encoding='utf-8')

def deserialize(request):
  items = request.decode('utf-8').strip().split(' ')
  if (len(items) > 1):
    return Request(items[0], items[1:])
  return Request(items[0], None)

class StateMachine:
  def __init__(self, client, global_state):
    self.transitions = {}
    self.start_state = None
    self.end_states = []
    self.current_state = None
    self.global_state = global_state
    self.client = client
  
  def add_transition(self, state_name, command, transition, end_state = 0):
    self.transitions.setdefault(state_name, {})
    self.transitions[state_name][command] = transition
    if end_state:
      self.end_states.append(state_name)

  def set_start(self, name):
      self.start_state = name
      self.current_state = name

  def process_command(self, unpacked_request):
    print('from %s' % self.current_state)
    if self.current_state in self.transitions and unpacked_request.type in self.transitions[self.current_state]:
      handler = self.transitions[self.current_state][unpacked_request.type]
      if not handler:
        return Response("Code -4 ", 'cannot transition')
      else:
        (new_state, response) = handler(unpacked_request, self.global_state, self.client)
        self.current_state = new_state
        print('to %s' % self.current_state)
        return response
    else:
      return Response("Code -4 ", 'Client needs to login first.')

def request_connect(request, global_state, client):
    if len(request.params) > 0:
        key = request.params[0]
        if key in SECRET:
            clientName = connectKeyToClient(key)
            client_address = client.getpeername()
            username = f"user{client_address[1]}"
            global_state.username_to_key[username] = key 
            createDirectory(clientName)
            downloadClientCommits(REPO_KEY, clientName, clientName)
            my_list = listClientCommits(REPO_KEY, clientName)
            my_list_stringified = listFiles(my_list)
            message = f"{clientName} is online as {username}.\n{clientName} has uploaded {my_list_stringified}.\n\n"
            global_state.broadcast_except(message, client)
            my_message = f"You are logged in as {username}."
            return ('auth', Response("Code 0 ", my_message))
        else:
            return ('start', Response("Code -2 ", 'Wrong password.'))
    else:
        return ('start', Response("Code -1 ", 'Not enough params.'))

def request_disconnect(request, global_state, client):
    client_address = client.getpeername()
    username = f"user{client_address[1]}"
    key = global_state.username_to_key.pop(username)
    clientName = connectKeyToClient(key) 
    deleteDirectory(clientName)
    my_list = listClientCommits(REPO_KEY, clientName)
    deleteServerFilesClientOFF(my_list)
    my_list_stringified = listFiles(my_list)
    message = f"{clientName} is now offline. Please delete {my_list_stringified} from your directory.\n\n"
    global_state.broadcast_except(message, client)
    return ('start', Response("Code 0 ", 'You are logged out.'))

def request_rights(request, global_state, client):
    if len(request.params) > 0:
        client_address = client.getpeername()
        target_username = request.params[0]
        target_file = request.params[1]

        username = f"user{client_address[1]}"
        key = global_state.username_to_key.get(username)
        clientName = connectKeyToClient(key)

        request_message = f"\n✉ from {clientName}: Hello {target_username}! May I have access to {target_file}?"
        global_state.broadcast_except(request_message, client)

        return ('auth', Response("Code 0 ", "sent"))
    else:
        return ('start', Response("Code -1 ", 'Not enough params.'))
    
def request_answerYes(request, global_state, client):
    if len(request.params) > 0:
        client_address = client.getpeername()
        target_username = request.params[0]

        username = f"user{client_address[1]}"
        key = global_state.username_to_key.get(username)
        clientName = connectKeyToClient(key)

        request_message = f"\n✉ from {clientName}: Hello {target_username}! Yes, you may."
        global_state.broadcast_except(request_message, client)

        return ('auth', Response("Code 0 ", "sent"))
    else:
        return ('start', Response("Code -1 ", 'Not enough params.'))
    
def request_answerNo(request, global_state, client):
    if len(request.params) > 0:
        client_address = client.getpeername()
        target_username = request.params[0]

        username = f"user{client_address[1]}"
        key = global_state.username_to_key.get(username)
        clientName = connectKeyToClient(key)

        request_message = f"\n✉ from {clientName}: Hello {target_username}! No, you may not."
        global_state.broadcast_except(request_message, client)

        return ('auth', Response("Code 0 ", "sent"))
    else:
        return ('start', Response("Code -1 ", 'Not enough params.'))
    
def request_download(request, global_state, client):
    if len(request.params) > 0:
      client_address = client.getpeername()
      target_username = request.params[0]
      target_file = request.params[1]
      username = f"user{client_address[1]}"
      key = global_state.username_to_key.get(username)
      clientName = connectKeyToClient(key)
      downloadClientFile(clientName, target_file)
      request_message = f"\n✉ from {clientName}: I have downloaded {target_file} from {target_username}."
      global_state.broadcast_except(request_message, client)
      my_message = f"{target_file} downloaded."
      return ('auth', Response("Code 0 ", my_message))
    else:
        return ('start', Response("Code -1 ", 'Not enough params.'))

def request_read(request, global_state, client):
    if len(request.params) > 0:
      client_address = client.getpeername()
      target_username = request.params[0]
      target_file = request.params[1]
      username = f"user{client_address[1]}"
      key = global_state.username_to_key.get(username)
      clientName = connectKeyToClient(key)
      content = readTextFile(target_username, target_file)
      request_message = f"\n✉ from {clientName}: I have read {target_file} from {target_username}."
      global_state.broadcast_except(request_message, client)
      my_message = f"File content | {content} |"
      return ('auth', Response("Code 0 ", my_message))
    else:
        return ('start', Response("Code -1 ", 'Not enough params.'))

def request_delete(request, global_state, client):
    if len(request.params) > 0:
      client_address = client.getpeername()
      target_file = request.params[0]
      username = f"user{client_address[1]}"
      key = global_state.username_to_key.get(username)
      clientName = connectKeyToClient(key)
      deleteClientFile(clientName, target_file)
      request_message = f"\n✉ from {clientName}: I have deleted {target_file}."
      global_state.broadcast_except(request_message, client)
      my_message = f"{target_file} deleted."
      return ('auth', Response("Code 0 ", my_message))
    else:
        return ('start', Response("Code -1 ", 'Not enough params.'))
    

def request_listAllFiles(request, global_state, client):
    file_list = listServerFiles()
    file_list_stringified = listFiles(file_list)
    my_message = f"\nPublic files: {file_list_stringified}."
    return ('auth', Response("Code 0 ", my_message))
    

def request_listFiles(request, global_state, client):
    target_username = request.params[0]
    file_list = listMyFiles(target_username)
    file_list_stringified = listFiles(file_list)
    my_message = f"\n{target_username}'s files: {file_list_stringified}."
    return ('auth', Response("Code 0 ", my_message))

class TopicProtocol(StateMachine):
  def __init__(self, client, global_state):
    super().__init__(client, global_state)
    self.set_start('start')
    self.add_transition('start', 'login', request_connect)
    self.add_transition('auth', 'logout', request_disconnect)
    self.add_transition('auth', 'rights', request_rights)
    self.add_transition('auth', 'yes', request_answerYes)
    self.add_transition('auth', 'no', request_answerNo)
    self.add_transition('auth', 'download', request_download)
    self.add_transition('auth', 'read', request_read)
    self.add_transition('auth', 'delete', request_delete)
    self.add_transition('auth', 'listall', request_listAllFiles)
    self.add_transition('auth', 'list', request_listFiles)

class TopicList:
  def __init__(self):
    self.clients = []
    self.topics = {}
    self.messages = {}
    self.username_to_key = {} 
    self.lock = threading.Lock()
  def add_client(self, client):
    with self.lock:
      self.clients.append(client)
  def remove_client(self, client):
    with self.lock:
      self.clients.remove(client)
      for topic, clients in self.topics.items():  
        clients.remove(client)
  def broadcast(self, message):
        with self.lock:
            for client in self.clients:
                try:
                    client.sendall(bytes(message, encoding='utf-8'))
                except Exception as e:
                    print(f"Error broadcasting to client {client}: {e}")
  def broadcast_except(self, message, excluded_client):
        with self.lock:
            for client in self.clients:
                if client != excluded_client:
                    try:
                        client.sendall(bytes(message, encoding='utf-8'))
                    except Exception as e:
                        print(f"Error broadcasting to client {client}: {e}")


is_running = True
global_state = TopicList()

def handle_client_write(client, response):
  client.sendall(serialize(response))

def handle_client_read(client):
  try:
    protocol = TopicProtocol(client, global_state)
    while True:
      if client == None:
        break
      data = client.recv(1024)
      if not data:
        break
      unpacked_request = deserialize(data)    
      response = protocol.process_command(unpacked_request)
      handle_client_write(client, response)

  except OSError as e:
    global_state.remove_client(client)

def accept(server):
  while is_running:
    client, addr = server.accept()
    global_state.add_client(client)
    print(f"{addr} has connected.")
    client_read_thread = threading.Thread(target=handle_client_read, args=(client,  ))
    client_read_thread.start()


def main():
  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    accept_thread = threading.Thread(target=accept, args=(server,))
    accept_thread.start()
    accept_thread.join()
  except BaseException as err:
    print(err)
  finally:
    if server:
      server.close()

if __name__ == '__main__':
  main()