import hashlib
from functools import total_ordering

basehashconsts=[0xec9a67f4b868fd5c43b75a061e806ed9dc964a996459c09723f3cfa0fed7a6e6,
		0xb329552536d44b0e5062ad8c53be55bda3f4f8d716a6110dd6ae689ee7a9c7a8,
		0x7e5ad33e6094ae05cfa5c89f58ba17dd381a7d07396f91571ebb80a14964baf3,
		0xaa32c9e3146b002b4ba971a1d7f5f9a71637ce879ee3ef4ece6ebebeb36f1726,
		0xab7456c9ffe000c8ac81f5714eefa493478f24d3d6e023890a46734a075ab0ff,
		0x41559eca0bd401984018c56c27f5fe7aeb1cbdd5a858c677416a339cacd2a6b6,
		0x4faab2ce81ee4da1ad213be3208cddadf449e8e5e633fb1606125c8086ff460a,
		0x4a6d1da3e5303c14dd4b84073c46eb575d8b26f04c4498287d68690c81a6c98e,
		0x80c16ea0591577c9bfde1d85db08f4f06cc3a00abd94cffa4d53d813a89c80a2,
		0xabc6fae7b2b67e78e9a20188d5bea649fb8bfd033773c49c29cde4105b399f3d,
		0x4c6d4342bdc300e4421ea341818d7216dba2463de89a9b27e337820ffeaa99de,
		0xb7db95fab8205c0d996424b07a73605adf7f983dbb00cb7cc248a934cde8d89a,
		0xa232b9e5e7c376828ca0e14b383aa51151d1ee216b331b4d64042c350ec1ded6,
		0x0f408ae5fcf94f3bf739142b38d51ca80f5ab93cabf0f934d192082d5abbb470,
		0x424bbb0e29f76851b1f533e7631c0df4b98c094e4fe2f6c0c304be9e7811a7f6,
		0x829bf6d35fff48ac475e9214884f4c5df9ef050d3cb09df4274f0bbe5d3d77b5]
		
hashconsts=[x if xi==yi else x ^ y for xi,x in enumerate(basehashconsts) for yi,y in enumerate(basehashconsts)]

def lrotate(x,k,l=256):
	return ((x << k) | (x >> (l-k))) & ((1 << l)  - 1)
		
class cyclebuf(object):
	def __init__(self,sz):
		self.buf=bytearray(sz)
		self.tailptr=0
		self.full=False
	def tail(self):
		return self.buf[self.tailptr]
	def push(self,x):
		t=self.tail()
		self.buf[self.tailptr]=x
		self.tailptr=(self.tailptr+1) % len(self.buf)
		if(self.tailptr==0):
			self.full=True
		if(not self.full):
			return None
		return t
	def __repr__(self):
		return ''.join([chr(c) for c in self.buf])
			
def rkslice(content,l_average_size,l_window_size):
	ch=0
	k=1 << l_window_size
	windowchars=cyclebuf(k)
	chunk=bytearray()
	
	for nextb in content:
		#print((ch,windowchars))
		front=ord(nextb)
		back=windowchars.push(front)
		fhash=hashconsts[front]
		if(back):
			bhash=lrotate(hashconsts[back],k)
		else:
			bhash=0
			
		ch=lrotate(ch,1) ^ bhash ^ fhash
	
		chunk.append(front)
		if(ch < (1 << (256-l_average_size))):
			yield chunk,int(hashlib.sha256(chunk).hexdigest(),16)
			chunk=bytearray()
	yield chunk,int(hashlib.sha256(chunk).hexdigest(),16)
def alphatest():
	for y in ['abcdefghijklmnopqrstuvwxyz','qrstuvwxyz']:
		for c in rkslice(y,1,3):
			#print(''.join([chr(x) for x in c]))
			pass
		
def bufferedread(fileobj,bufsize=1<<10):
	buf=fileobj.read(bufsize)
	while(buf != ''):
		for b in buf:
			yield b
		buf=fileobj.read(bufsize)
		
		
#Ghost node:  provides a gethash and getchildren and gettimestamp

class node(object):
	def __init__(self,path,index):
		self.path=path
		self.dirty=index.get('dirty',True)
	def gethash(self):
		hio=index.get('hash',0)
		if(self.getdirty() or hio==0):
			h=hashlib.sha256()
			for c in self.getchildren():
				ch=c.gethash()
				h.update(bytes.fromhex(hex(ch)[2:-1]))
			hio=int(h.hexdigest(),16)
			index['timestamp']=hio
		return hio
	def getchildren(self):
		pass
	def getdirty(self):
		d=self.dirty
		for c in self.getchildren():
			if(d):
				self.dirty=True
				return True
			d=d or c.getdirty()
		return d
	
class directorynode(object):
	def __init__(self,path):
		dirname=os.path.split(path)[1]
		index=load_index(dirname) #last
		super(directorynode,self).__init__(path,index)
		self.children={}
	def getchildren(self):
		for l in listdir(path):
			if(l not in self.children):
				self.dirty=True
				
@total_ordering
class PathHashTimestamp(object):
	def __init__(self,path,hash=0,timestamp=0):
		self.path=path
		self.hash=hash
		self.timestamp=timestamp
	def __lt__(self,other):
		return (self.path,self.hash,self.timestamp) < (other.path,other.hash,other.timestamp)
	def __eq__(self,other):
		return (self.path,self.hash,self.timestamp) == (other.path,other.hash,other.timestamp)

		
def index_sync(local,remote,path):
	remote.getpht(path)
	lc=local.phat_table.get(path,default=PathHashTimestamp(path)
	if(lc
		
def on_recieve_phat(local,remote,phatmsg):
	lc=local.phat_table.get(phatmsg.path,default=PathHashTimestamp(phatmsg.path))
	if(lc == phatmsg):
		remote.send_phat_agree(lc)
	else:
		children=local.getchildpaths(lc.path)
		for c in children:
			remote.send_phat(local.phat_table[c])  #async here.
		
		if(lc.timestamp < phatmsg.timestamp):
			local.phat_table[phatmsg.path]=phatmsg
			local.phat_dirty_table[phatmsg.path]=True
		
			
		

if(__name__=='__main__'):
	import sys
	for c,ch in rkslice(bufferedread(sys.stdin),16,8):
		print(''.join([chr(x) for x in c]))
		print('-'*64)


	
