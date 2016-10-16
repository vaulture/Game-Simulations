#settlers of catan

#ore,wood,brick,sheep,wheat
#2,3,4,5,5,6,6,7,8,8,9,9,10,11,12
#2,3,4,5,6,7,8,9,10,11,12
#rings={}


		
import pdb
import random as random
import itertools as it
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np


class Player():
	def __init__(self,name,number):
		self.name = name
		self.number = number
		self.cards = []
		self.settlements = []
		self.roads = []
		self.cities = []
		self.rpo = ['wood','brick','wheat','ore','sheep']
		self.primaryneed,self.secondaryneed,self.tertiaryneed = (None,None,None)

		
		
		
# hex cluster
# TOP = (0,4), TL = (-3,2) , topr = (3,2) , MID = (0,0) , BL = (-3,-2) , BR = (3,-2) , BOT = (0,-4)
		#TOP#
	#TL#	#topr#
		#MID#
	#BL#	#BR#	
		#BOT#

class Hexcluster():
	def __init__(self,gridobj,midtile,ring):
		
		self.tiles = []
		
		if midtile == None:
			basetile = Tile(0,0,0,self,gridobj)
			self.originx = 0
			self.originy = 0
			self.mid = basetile
		else:
			self.originx = midtile.x
			self.originy = midtile.y
			self.mid = midtile
		
		self.tiles.extend([self.mid])
		
		topx,topy = (self.originx,4+self.originy)
		tile = self.occupiedspace(gridobj,topx,topy)
		if tile is None:
			self.top = Tile(topx,topy,ring+1,self,gridobj)
			self.mid.connecttile(gridobj,self.top,'top',0)		
		else:
			self.mid.connecttile(gridobj,tile,'top',1)	
			
		tlx,tly = (-3+self.originx,2+self.originy)
		tile = self.occupiedspace(gridobj,tlx,tly)
		if tile is None:
			self.tl = Tile(tlx,tly,ring+1,self,gridobj)
			self.mid.connecttile(gridobj,self.tl,'topleft',0)
		else:
			self.mid.connecttile(gridobj,tile,'topleft',1)			
			
		trx,topry = (3+self.originx,2+self.originy)
		tile = self.occupiedspace(gridobj,trx,topry)
		if tile is None:
			self.tr = Tile(trx,topry,ring+1,self,gridobj)
			self.mid.connecttile(gridobj,self.tr,'topright',0)			
		else:
			self.mid.connecttile(gridobj,tile,'topright',1)

		blx,bly = (-3+self.originx,-2+self.originy)
		tile = self.occupiedspace(gridobj,blx,bly)
		if tile is None:
			self.bl = Tile(blx,bly,ring+1,self,gridobj)
			self.mid.connecttile(gridobj,self.bl,'bottomleft',0)			
		else:
			self.mid.connecttile(gridobj,tile,'bottomleft',1)			
			
		brx,bry = (3+self.originx,-2+self.originy)	
		tile = self.occupiedspace(gridobj,brx,bry)
		if tile is None:
			self.br = Tile(brx,bry,ring+1,self,gridobj)
			self.mid.connecttile(gridobj,self.br,'bottomright',0)			
		else:
			self.mid.connecttile(gridobj,tile,'bottomright',1)			
			
		botx,boty = (self.originx,-4+self.originy)
		tile = self.occupiedspace(gridobj,botx,boty)
		if tile is None:
			self.bot = Tile(botx,boty,ring+1,self,gridobj)
			self.mid.connecttile(gridobj,self.bot,'bottom',0)			
		else:
			self.mid.connecttile(gridobj,tile,'bottom',1)			
			
		gridobj.hexclusters.extend([self])
		
		
	def occupiedspace(self,gridobj,x,y):
		for tile in gridobj.tiles:
			if (tile.x == x) and (tile.y == y):
				return tile
			else:
				pass
		# no existing tiles had the same coordinates		
		return None
		
	
		
		
class Tile():
	def __init__(self,x,y,ring,hexcluster,gridobj):
		self.availableedges = 6
		self.x = x
		self.y = y
		self.ring = ring
		self.resource = None
		self.number = None
		self.tiletop = None
		self.tiletopright = None
		self.tiletopleft = None
		self.tilebottom = None
		self.tilebottomright = None
		self.tilebottomleft = None
		self.etr = None
		self.etl = None
		self.el = None
		self.er = None
		self.ebl = None
		self.ebr = None
		hexcluster.tiles.extend([self])
		gridobj.tiles.extend([self])
		
	def connecttile(self,gridobj,tile,dir,defineedges):
		#pdb.set_trace()
		if dir == 'top':
			self.tiletop = tile
			tile.tilebottom = self
			if defineedges == 1:
				pass
			else:
				tile.etl = Edge(gridobj,tile.x,tile.y,'tl')
				tile.etr = Edge(gridobj,tile.x,tile.y,'tr')
				if (tile.tilebottomright == None):
					tile.er = Edge(gridobj,tile.x,tile.y,'r')
				if (tile.tilebottomleft == None):
					tile.el = Edge(gridobj,tile.x,tile.y,'l')
		elif dir == 'topright':
			self.tiletopright = tile
			tile.tilebottomleft = self
			if defineedges == 1:
				pass
			else:			
				tile.etr = Edge(gridobj,tile.x,tile.y,'tr')
				tile.er = Edge(gridobj,tile.x,tile.y,'r')
				if (tile.tilebottom == None):
					tile.ebr = Edge(gridobj,tile.x,tile.y,'br')
				if (tile.tiletopleft == None):
					tile.etl = Edge(gridobj,tile.x,tile.y,'tl')
		elif dir == 'topleft':
			self.tiletopleft = tile
			tile.tilebottomright = self
			if defineedges == 1:
				pass
			else:			
				tile.etl = Edge(gridobj,tile.x,tile.y,'tl')
				tile.el = Edge(gridobj,tile.x,tile.y,'l')
				if tile.tilebottom == None:
					tile.ebl = Edge(gridobj,tile.x,tile.y,'bl')
				if tile.tiletopright == None:
					tile.etr = Edge(gridobj,tile.x,tile.y,'tr')
		elif dir == 'bottom':
			self.tilebottom = tile
			tile.tiletop = self	
			if defineedges == 1:
				pass
			else:			
				tile.ebl = Edge(gridobj,tile.x,tile.y,'bl')
				tile.ebr = Edge(gridobj,tile.x,tile.y,'br')
				if tile.tiletopleft == None:
					tile.el = Edge(gridobj,tile.x,tile.y,'l')
				if tile.tiletopright == None:
					tile.er = Edge(gridobj,tile.x,tile.y,'r')
		elif dir == 'bottomleft':
			self.tilebottomleft = tile
			tile.tiletopright = self
			if defineedges == 1:
				pass
			else:			
				tile.el = Edge(gridobj,tile.x,tile.y,'l')
				tile.ebl = Edge(gridobj,tile.x,tile.y,'bl')
				if tile.tiletop == None:
					tile.etl = Edge(gridobj,tile.x,tile.y,'tl')
				if tile.tilebottomright == None:
					tile.ebr = Edge(gridobj,tile.x,tile.y,'br')
		elif dir == 'bottomright':
			self.tilebottomright = tile
			tile.tiletopleft = self	
			if defineedges == 1:
				pass
			else:			
				tile.er = Edge(gridobj,tile.x,tile.y,'r')
				tile.ebr = Edge(gridobj,tile.x,tile.y,'br')
				if tile.tiletop == None:
					tile.etr = Edge(gridobj,tile.x,tile.y,'tr')
				if tile.tilebottomleft == None:
					tile.ebl = Edge(gridobj,tile.x,tile.y,'bl')
		else:
			print('invalid dir:  ',dir)
			return
			

			
class GameSetup():	
	def __init__(self):
		grid = Grid(1)
		self.allocate_resources(grid)
		self.addnumbers(grid)
		self.plist = ['chris','becky','tom','michelle']
		count = it.count(0)
		self.players = [Player(item,next(count)) for item in self.plist]
		
	def allocate_resources(self,grid):
		#pdb.set_trace()
		total = len(grid.tiles)
		minnumeach = total // 5
		resourcetypes = ['ore','wood','brick','sheep','wheat']
		minnums = {x:minnumeach for x in resourcetypes}
		remainder = total % 5
		for tile in grid.tiles:
			ok = False
			if total <= remainder:
				tile.resource = random.choice(resourcetypes)
			else:
				while ok == False:
					rtype = random.choice(resourcetypes)
					if minnums[rtype] > 0:
						tile.resource = rtype
						minnums[rtype] -= 1
						total -= 1
						ok = True
					else:
						pass
			#print(tile.resource)
					
		
		#print(minnumeach,remainder)
		
		
		
	def addnumbers(self,grid):
		
		
		initnumlist = [2,3,4,5,6,6,7,8,8,9,10,11,12]
		numlist = [2,3,4,5,6,6,7,8,8,9,10,11,12]
			
		for tile in grid.tiles:
			if numlist == []:
				numlist = list(initnumlist)
			randindex = random.randrange(len(numlist))
			tile.number = numlist[randindex]
			del numlist[randindex]
			
			#print(tile.number)
 
		#print(randindex,numlist[randindex])
			
class Grid():
	def __init__(self,numrings):	
		self.numrings = numrings
		self.x = 0
		self.y = 0
		self.hexclusters = []
		self.tiles = []
		self.edges = []
	
		for ring in range(0,self.numrings):
			if self.tiles == []:
				Hexcluster(self,None,0)
			else:
				for tile in self.tiles:
					if tile.ring == (ring):
						Hexcluster(self,tile,ring)		
		
		#print(self.hexclusters)
		
		#print([(obj.x,obj.y) for obj in self.edges])
		# xe = [obj.x for obj in self.edges]
		# ye = [obj.y for obj in self.edges]
		# plt.scatter(xe,ye)
		
		
		#print([(obj.x,obj.y) for obj in self.tiles])
		#x = [obj.x for obj in self.tiles]
		#y = [obj.y for obj in self.tiles]
		#plt.scatter(x,y,marker ='H')
		
			
		plt.show()
		
		
		
		

class Edge():
	def __init__(self,gridobj,tilex,tiley,type):
		print('tile:  ',tilex,tiley)
		if type == 'tl':
			self.x = tilex - 1
			self.y = tiley + 2
		elif type == 'tr':
			self.x = tilex + 1
			self.y = tilex + 2
		elif type == 'r':
			self.x = tilex + 2
			self.y = tiley
		elif type == 'l':
			self.x = tilex - 2
			self.y = tiley
		elif type == 'bl':
			self.x = tilex - 1
			self.y = tiley - 2
		elif type == 'br':
			self.x = tilex + 1
			self.y = tilex - 2
		else:
			return
		
		print('edge:  ',self.x,self.y)
		
		gridobj.edges.extend([self])
		
	
class GameOperator():
	def __init__(self):
		self.gobj = GameSetup()
		self.gameover = None
		
		self.players = self.gobj.players
		self.totalplayers = len(self.players)
		
		self.turn = 0
		self.currentplayerindex = 0
		self.currentplayer = self.players[0]
		
		######################################################
		
		self.play()
		
		
	def startingtwo(self):
		pass
	
	def rolldice(self):
		self.dicetotal = random.randint(1,6) + random.randint(1,6)	
		print(self.dicetotal,self.currentplayer.name)
		
	def play(self):	
		self.startingtwo()
		while self.gameover is None:
			self.startturn()
			self.endturn()	
		
		print('Winner on turn', self.turn,',',self.players[0].name)

		
	def startturn(self):
		self.taketurn()
		
	
	def taketurn(self):
		self.rolldice()
			
		
	def endturn(self):
	
		self.turn += 1
		
		if self.turn > 5:
			self.gameover = 1
		
		self.currentplayerindex += 1
		if self.currentplayerindex > self.totalplayers - 1:
			self.currentplayer = self.players[0]
			self.currentplayerindex = 0
		else:
			self.currentplayer = self.players[self.currentplayerindex]
	
	

gop = GameOperator()
	

