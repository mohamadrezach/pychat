from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread,Lock
from optparse import OptionParser
from os import _exit
import sys

print_lock=Lock()
class handler(Thread):
	def __init__(self,s):
		super().__init__()
		self.s=s
	def run(self):
		try:
			while True:
				m=self.s.recv(1024)
				if m==b'@@@server_is_stoped@@@':
					print('server is outed')
					break
				print(m.decode('utf-8'))
		except Exception:
			print(Exception)
		finally:
			_exit(1)		

class client:
	def __init__(self,server,port,user):
		self.server=server
		self.port=port
		self.user=user

	def perform(self):
		s=socket(AF_INET,SOCK_STREAM)
		s.connect((self.server,self.port))
		print("Connected.......... [type EXIT to exit] ")
		obj=handler(s)
		obj.daemon=False
		obj.start()
		msg=self.user+ ' joined'
		try:
			while(msg.find('EXIT')==-1):
				s.send(bytes(msg,'utf-8'))
				msg = sys.stdin.readline()
				msg=self.user+" : "+msg
					
		finally:
			s.send(b'EXIT')		
			_exit(1)	

def main(server,port,user):
	obj_c=client(server,port,user)
	obj_c.perform()


if __name__=="__main__":
	p=OptionParser(usage='%prog -s|--server [server-adress] -p|--port [port_number]')
	p.add_option('-s','--server',action='store',dest='server',type='string',help='address of server')
	p.add_option('-p','--port',action='store',dest='port',type='int',help='port number')
	p.add_option('-u','--user',action='store',dest='user',type='string',help='your nickname')
	options,args=p.parse_args()
	if(options.server==None or options.port==None or options.user==None):
		p.error('ERR : see -p or --help')
	main(options.server,options.port,options.user)	