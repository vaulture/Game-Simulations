import itertools as it
import pprint as pprint
import pdb
import random as rand
 

class GameOperator():
	def __init__(self,automate):
		
		self.gobj = GameObj()
		self.totaltiles = len(self.gobj.grid)
		self.gameover = None
		
		self.housecost = 50
		self.housebenefit = 100
		self.hotelcost = 100
		self.hotelbenefit = 200
		
		plist = ['chris','becky','tom','michelle']
		self.totalplayers = len(plist)
		tlist = ['Dog','Cat','Dog','Thimble']
		ptlist = zip(plist,tlist)
		
		count = it.count(0)
		self.players = [Player(name,next(count),obj,self.gobj) for name,obj in ptlist]
		
		self.turn = 0
		self.currentplayerindex = 0
		self.currentplayer = self.players[0]
		
		######################################################
		
		self.play(automate)
		
	
		
	def play(self,automate):	
		while self.gameover is None:
			self.startturn(automate)
			self.endturn()	
		
		print('Winner on turn', self.turn,',',self.players[0].name)
		self.showPlayerProperties()

		
	def startturn(self,automate):
	
		if automate == 1:
			self.taketurn()
			self.automatedpurchase()
		else:
			self.playeroptions()
		
	
	def taketurn(self):
		
		if self.currentplayer.injail == True:
			self.payjail(),self.rolljail()
		else:	
			self.rolldice()
			self.moveplayer()
			self.propertyaction()		
	
	
		
	def endturn(self):
	
		self.turn += 1
		
		self.checkstatus()
		
		self.currentplayerindex += 1
		if self.currentplayerindex > self.totalplayers - 1:
			self.currentplayer = self.players[0]
			self.currentplayerindex = 0
		else:
			self.currentplayer = self.players[self.currentplayerindex]
	
	def checkstatus(self):
		rplayer = None
		for player in self.players:
			if player.money < 0:
				rplayer = player
			else:
				pass
		
		if rplayer is not None:
			self.removeplayer(rplayer)

		if len(self.players) == 1:
			self.gameover = 1	
	
	
	def automatedpurchase(self):
		player = self.currentplayer	
		if player.properties == {}:
			return
			
		maxvisits = 0
		maxprop = None	
		
		if len(player.properties) == 1:
			first = list(player.properties.keys())[0]
			maxprop = player.properties[first]
			maxvisits = maxprop.visits
			return
			

		
		for index in player.properties:
			if player.properties[index].visits > maxvisits:
				secmaxvisits = maxvisits
				secmaxprop = maxprop
				maxvisits = player.properties[index].visits
				maxprop = player.properties[index]

		if (maxprop.rent - secmaxprop.rent) > 100:
			if secmaxprop.houses > 2:
				self.buyhouseshotels(secmaxprop.tile,0,1)
				secmaxprop.houses = 0
			else:
				self.buyhouseshotels(secmaxprop.tile,1,0)
			return				
				
		if maxprop.houses > 2:
			if player.money > self.hotelcost:
				self.buyhouseshotels(maxprop.tile,0,1)
				maxprop.houses = 0 
			else:
				self.buyhouseshotels(maxprop.tile,1,0)
			return
		
			
				
			
	
	
	def removeplayer(self,targetPlayer):
		for item in targetPlayer.properties:
			targetPlayer.properties[item].owningplayer = None
			targetPlayer.properties[item].houses = 0
			targetPlayer.properties[item].hotels = 0
		
		self.players.remove(targetPlayer)
		self.totalplayers -= 1	
		
	

		# self.showPlayerProperties()
		# self.givepropforprop
		# self.givemoneyforprop
		# self.givepropformoney
		# self.buyhouseshotels(tile,#houses,#hotels)
	def playeroptions(self):
		print('it is ',self.currentplayer.name,"'s turn")
		popts = {1:'Show Player Properties',2:'Trade',3:'Buy Houses or Hotels',4:'Take turn'}
		optfunctions = {1:[self.showPlayerProperties,None],2:[self.trade,None],3:[self.buy,None],4:[self.taketurn,None]}
		#print(self.currentplayer.name,self.turn)
		pchoice = None
		while pchoice is None:
			pchoice = self.choosefromdict(popts)

		if optfunctions[pchoice][1] == None:
			optfunctions[pchoice][0]()
		else:
			optfunctions[pchoice][0](optfunctions[pchoice][1])
			
		if pchoice != 4:
			self.playeroptions()
		
		
	def choosefromdict(self,options):
		icommand = str(options) + ' :  '
		choice = self.inputinteger(icommand)
		if int(choice) in options.keys():
			return int(choice)
		else:
			return
			
	def inputinteger(self,inputcommand):
		#pdb.set_trace()
		value = None 
		while value is None:
			ivalue = input(inputcommand)
			try:
				value = int(ivalue)
			except:
				pass
		return value
			
			
	def inputisinteger(self,inval):
		if inval == '' or not isinstance(inval,int):
			return
		else:
			return inval
	
	def showPlayerProperties(self):
		for targetPlayer in self.players:
			print(targetPlayer.name,targetPlayer.money)
			for item in targetPlayer.properties:
				print('Tile: ',item,'  Rent: ',targetPlayer.properties[item].rent,'  Houses: ',targetPlayer.properties[item].houses \
				,'  Hotels: ',targetPlayer.properties[item].hotels,'  Visits: ',targetPlayer.properties[item].visits)
	
	
	def trade(self):
		modplayers = [x for x in self.players if x != self.currentplayer]
		popts = {x.number:x.name for x in modplayers}
		
		pchoice = None
		while pchoice is None:
			pchoice = self.choosefromdict(popts)
		targetPlayer = self.players[pchoice]
		

		topts = {1:'Property for Property',2:'Give Money, Receive Property',3:'Give Propery, Receive Money'}

		if targetPlayer.properties == {} and self.currentplayer.properties == {}:
			return 
		if self.currentplayer.properties == {}:
			topts = {2:topts[2]}
		if targetPlayer.properties == {}:
			topts = {3:topts[3]}
		
		tchoice = None
		while tchoice is None:
			tchoice = self.choosefromdict(topts)	
			
		if tchoice == 1:
			yourprop,theirprop,yourmoney,theirmoney = self.promptpropforprop(targetPlayer)
		elif tchoice == 2:
			yourprop,theirprop,yourmoney,theirmoney = self.promptmoneyforprop(targetPlayer)
		elif tchoice == 3:
			yourprop,theirprop,yourmoney,theirmoney = self.promptpropformoney(targetPlayer)
		else:
			pass
		
		
		icommand = 'Enter 1 to confirm: '
		confirm = self.inputinteger(icommand)
		if int(confirm) == 1:
			optfunctions = {1:[self.givepropforprop,[targetPlayer,yourprop,theirprop]],2:[self.givemoneyforprop,[targetPlayer,yourmoney,theirprop]],3:[self.givepropformoney,[targetPlayer,yourprop,theirmoney]]}
			optfunctions[tchoice][0](optfunctions[tchoice][1])	
		else:
			return
	
	
	def promptpropforprop(self,targetPlayer):
			icommand = self.currentplayer.name + "'s property to trade away" + str([(x,self.currentplayer.properties[x].name) for x in self.currentplayer.properties]) + ' :  '
			num =self.inputinteger(icommand)
			if num in self.currentplayer.properties:
				yourprop =self.currentplayer.properties[num]
			else:
				print(self.currentplayer.name,'has no property',num)
				return
			icommand = targetPlayer.name+"'s property to trade for" + str([(x,targetPlayer.properties[x].name) for x in targetPlayer.properties]) + ' :  '
			num = self.inputinteger(icommand)
			if num in targetPlayer.properties:
				theirprop = targetPlayer.properties[num]
			else:
				print(targetPlayer.name,'has no property',num)
				return
			yourmoney = None
			theirmoney = None
			return yourprop,theirprop,yourmoney,theirmoney

	
	def promptmoneyforprop(self,targetPlayer):
		icommand = self.currentplayer.name + "'s money to give away, CURRENTLY: " + str(self.currentplayer.money) + ' :  '
		yourmoney = self.inputinteger(icommand)
		if not enoughmoney(self.currentplayer,yourmoney):
			return
		icommand = targetPlayer.name+"' property to trade for" + str([(x,targetPlayer.properties[x].name) for x in targetPlayer.properties]) + ' :  '
		num = self.inputinteger(icommand)
		if num in targetPlayer.properties:
			theirprop = targetPlayer.properties[num]
		else:
			print(targetPlayer.name,'has no property',num)
			return
		yourprop = None
		theirmoney = None	
		return yourprop,theirprop,yourmoney,theirmoney
		
	def promptpropformoney(self,targetPlayer):
		icommand = self.currentplayer.name + "'s property to trade away" + str([(x,self.currentplayer.properties[x].name) for x in self.currentplayer.properties]) + ' :  '
		num =self.inputinteger(icommand)
		if num in self.currentplayer.properties:
			yourprop =self.currentplayer.properties[num]
		else:
			print(self.currentplayer.name,'has no property',num)
			return			
		icommand = targetPlayer.name +"'s money to trade for:  "
		theirmoney = self.inputinteger(icommand)
		if not enoughmoney(targetPlayer,theirmoney):
			return
		yourmoney = None
		theirprop = None
		return yourprop,theirprop,yourmoney,theirmoney	
	
	def givepropforprop(self,args):
		targetPlayer = args[0]
		giveprop = args[1]
		receiveprop = args[2]
		self.currentplayer.properties.update({receiveprop.tile:receiveprop})
		targetPlayer.properties.update({giveprop.tile:giveprop})
		del self.currentplayer.properties[giveprop.tile]
		del targetPlayer.properties[receiveprop.tile]
		
		
	def givemoneyforprop(self,args):
		targetPlayer = args[0]
		givemoney = args[1]
		receiveprop = args[2]
		self.currentplayer.money -= givemoney
		targetPlayer.money += givemoney
		self.currentplayer.properties.update({receiveprop.tile:receiveprop})
		del targetPlayer.properties[receiveprop.tile]
		
		
	def givepropformoney(self,args):
		targetPlayer = args[0]
		giveprop = args[1]
		receivemoney = args[2]
		del self.currentplayer.properties[giveprop.tile]
		targetPlayer.properties.update({giveprop.tile:giveprop})
		self.currentplayer.money += receivemoney
		targetPlayer.money -= receivemoney
		
		
	def buy(self):
		if self.currentplayer.properties == {}:
			print('This player has no properties')
			return
		else:
			icommand = self.currentplayer.name + "' property to improve" + str([(x,self.currentplayer.properties[x].name) for x in self.currentplayer.properties]) + ' :  '
			propnum = self.inputinteger(icommand)
			icommand = 'How many houses to add? '
			houses = self.inputinteger(icommand)
			icommand = 'How many hotels to add? '
			hotels = self.inputinteger(icommand)
			self.buyhouseshotels(propnum,houses,hotels)
			
			
	def buyhouseshotels(self,tile,houses,hotels):
		money = self.currentplayer.money
		if houses != 0:
			if self.enoughmoney(self.currentplayer,self.housecost*houses):
				print(self.currentplayer.name, ' only have ',money)
				return
			money -= self.housecost*houses
			self.currentplayer.properties[tile].rent += self.housebenefit*houses
			self.currentplayer.properties[tile].houses += houses
			
		if hotels != 0:
			if self.enoughmoney(self.currentplayer,self.hotelcost*hotels):
				print(self.currentplayer.name,' only have ',money)
				return
			self.currentplayer.properties[tile].rent += self.hotelbenefit*hotels
			self.currentplayer.properties[tile].hotels += hotels
			money -= self.hotelcost*hotels
	
	def enoughmoney(self,targetPlayer,cost):
		if targetPlayer.money >= cost:
			return False
		else:
			return True
		
	def payjail(self):
		self.currentplayer.money -= 100
		self.currentplayer.injail = False
		
	def rolljail(self):
		if rand.randint(1,6) == rand.randint(1,6):
			self.currentplayer.injail = False
		else:
			pass
		
	
	def rolldice(self):
		self.dicetotal = rand.randint(1,6) + rand.randint(1,6)
		
	def moveplayer(self):
		self.currentplayer.tile += self.dicetotal
		if self.currentplayer.tile > self.totaltiles-1:
			self.currentplayer.tile = self.currentplayer.tile - self.totaltiles
	
	def propertyaction(self):
		currenttile = self.gobj.properties[self.currentplayer.tile]
		currenttile.visits += 1
		if  currenttile.owningplayer is None:
			self.buyproperty(currenttile)
		else:
			self.chargerent(currenttile)
		
		
	def buyproperty(self,tile):
		tile.owningplayer = self.currentplayer
		self.currentplayer.properties.update({tile.tile:tile})
		self.currentplayer.money -= tile.cost
		
		
	def chargerent(self,tile):
		rentowner = tile.owningplayer
		rentowner.money += tile.rent
		self.currentplayer.money -= tile.rent
		#tile.cost 
		
	def drawchance(self):
		pass
		
	def drawcommchest(self):
		pass
	

class Player():
	def __init__(self,name,number,gamepiece,gobj):
	
		self.name = name
		self.number = number
		self.money = 20000
		self.tile = 0
		self.properties = {}
		self.injail = False
		
		if gamepiece not in gobj.gamepieces:
			self.__init__(name,input('Player: ' + name + ' -- Piece Name: ' + str(gobj.gamepieces) + ' :  '),gobj)
		else:
			self.gamepiece = gamepiece
		
 
class Property():
	def __init__(self,tile,name,cost,rent):
		self.tile = tile
		self.name = name
		self.cost = cost
		self.rent = rent
		self.houses = 0
		self.hotels = 0
		self.visits = 0
		self.owningplayer = None
		
		
 
class GameObj():
	def __init__(self):
		count = it.count(0)
		squaresize = 5
		propertycost = 10
		propertyrent = 50
		#self.grid = {next(count):(x,y) for x in range(1,11) for y in range(1,11)}
		self.grid = {next(count):(1,y) for y in range(1,squaresize+1)}
		self.grid.update({next(count):(x,squaresize) for x in range(2,squaresize+1)})
		self.grid.update({next(count):(squaresize,y) for y in range(squaresize-1,1,-1)})
		self.grid.update({next(count):(x,1) for x in range(squaresize,1,-1)})
		
		self.properties = {x:Property(x,('Property'+str(x)),propertycost,propertyrent) for x in self.grid}
		self.gamepieces = ['Dog','Cat','Thimble','House','Car']
		#pprint.pprint(self.grid)
		# for item in self.properties:
			# print(self.properties[item].tile)
		
		

while 1:		
	gop = GameOperator(1)

#pprint.pprint(g.grid)