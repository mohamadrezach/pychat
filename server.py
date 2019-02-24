from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread
from optparse import OptionParser
from os import _exit

connection_list_con=list()

class sender(Thread):
	def __init__(self,con,addr,server,port):
		super().__init__()
		self.con=con
		self.addr=addr
		self.server=server
		self.port=port

	def run(self):
		self.perform()

	def perform(self):
		key=b''
		try:
			while key !=b'EXIT':
				key=self.con.recv(1024)
				for i in range(len(connection_list_con)):
					if self.addr[1]!=connection_list_con[i].getpeername()[1] :#and self.addr[0]!=i[0]:
						try:
							connection_list_con[i].sendall(key)
						except Exception as e:	
							print(e,' >  ',i,' host exited')
							connection_list_con.pop(i)

			else:
				connection_list_con.remove(self.con)
		except KeyboardInterrupt:
			for i in connection_list_con:
				i.sendall(b'@@@server_is_stoped@@@')
			_exit(1)			
		except Exception:					
			connection_list_con.remove(con)
		self.con.close()		

class serverClass:
	__instance=None
	def __init__(self,server,port):
		self.server=server
		self.port=port

	@classmethod	
	def getInstance(cls,s,p):
		if(not cls.__instance):
			cls.__instance=serverClass(s,p)
		return cls.__instance	

	def runServer(self):
		s=socket(AF_INET,SOCK_STREAM)
	#	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.bind((self.server,self.port))
		s.listen(2)
		try:
			while True:
				con , addr= s.accept()
				connection_list_con.append(con)
				self.obl=sender(con,addr,self.server,self.port)
				self.obl.daemon=False
				self.obl.start()	
				print(addr,' connected ')
		except KeyboardInterrupt:
			for i in connection_list_con:
				i.sendall(b'@@@server_is_stoped@@@')
			_exit(1)				
		except Exception:
			_exit(1)	

		finally:		
			s.close()

def main(server,port):
	obj=serverClass.getInstance(server,port)
	obj.runServer()

if __name__=="__main__":
	p=OptionParser(usage="%prog -s|--server [ip_address] -p|--port [port]")
	p.add_option('-s','--server',action='store',dest='server',type='string',help='ip address of server')
	p.add_option('-p','--port',action='store',dest='port',type='int',help='port number to listen')
	options,args=p.parse_args()
	if(options.server == None or options.port==None):
		p.error("ERR :  see -h or ---help ")
	main(options.server,options.port)	
