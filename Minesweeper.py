
import tkinter as tk
import random

class Cell:
	def __init__(self,R,C,click):
		self.row = R
		self.column = C
		self.click = click
	def Button(self):
		self.button = tk.Button( Game, text='', command = lambda:self.click(self.row,self.column), activebackground='white', height=1, width=1)
		self.button.grid(row=self.row, column=self.column)
		return self.button

class game_play:
	def __init__(self, data,clusters, size):
		self.size = size
		self.data = data
		self.clusters = clusters
		self.game_board()
		self.first_hint()
	
	def game_board(self):
		self.buttons = []
		click=self.clicked
		for  i in range( self.size ):
			tmp = []
			for  j in range( self.size ):
				c = Cell( i, j, click )
				tmp.append( c.Button() )
			self.buttons.append(tmp)
	
	def clicked( self,R,C ):
		self.row = R
		self.column = C
		if(self.data[self.row][self.column] == 'X'):
			self.buttons[self.row][self.column].configure(activebackground='red' )
			self.game_over()
		elif(self.data[ self.row][self.column ]==' '):
			self.clear_cluster()
		else:
			self.buttons[self.row][self.column].configure(fg='blue', bg='white', text=self.data[self.row][self.column])

	def game_over(self):
		for  i in range( self.size ):
			for  j in range( self.size ):
				if(self.data[i][j] == 'X'):
					self.buttons[i][j].configure(bg='orange')
				else:
					self.buttons[i][j].configure(text=self.data[i][j], bg='white')
	
	def clear_cluster(self):
		for cluster in self.clusters:
			if ((self.row,self.column) in cluster):
				for (r,c) in cluster:
					self.buttons[r][c].configure( fg='blue', bg='white', text=self.data[r][c]  )
				self.clusters.remove(cluster)
				break
	
	def first_hint(self):
		cluster = list(random.choices(self.clusters)[0])
		not_empty =True
		i = 0
		while(not_empty):
			(r,c)=cluster[i]
			if(self.data[r][c] == ' '):
				not_empty = False
			else:
				i+=1
		self.buttons[r][c].configure(bg='lightblue')


class game_data:
	def __init__(self, size, no_of_mines):
		self.create_empty_data(size)
		self.insert_mines(no_of_mines)
		self.insert_mine_counts()
		self.cluster_empty_cells()
	
	def create_empty_data(self, size):
		self.size = size
		self.data=[ [' ']*self.size for _ in range(self.size) ]
	
	def insert_mines(self, no_of_mines):
		self.mines=[]
		for mine in random.sample(range(self.size*self.size), no_of_mines):
			r = mine//self.size
			c = mine%self.size
			self.mines.append((r,c))
			self.data[r][c] = 'X'
			
	def insert_mine_counts(self):
		for r,c in self.mines:
			for row in self.indices(r):
				for colmn in self.indices(c):
					if(self.data[row][colmn]==' '):
						self.data[row][colmn] = 1
					elif(self.data[row][colmn]!='X'):
						self.data[row][colmn] += 1

	def cluster_empty_cells(self):
		self.clusters = []
		self.empty = self.empty_cells()
		for r,C in enumerate(self.empty):
			for c in C:
				rows = self.indices(r)
				columns = self.indices(c)
				s=set()
				for i in rows:
					for j in columns:
						s.add((i,j))
				self.clusters.append(s)
	
		p1 = 0
		while(p1<len(self.clusters)):
			p2 = p1+1
			not_deleted = True
			while(p2<len(self.clusters)):
				intersection = False
				inter = list(self.clusters[p1].intersection(self.clusters[p2]))
				for r,c in inter:
					if(self.data[r][c]==' '):
						intersection = True
						break
				if (intersection):
					self.clusters[p1].update(self.clusters[p2])
					self.clusters.pop(p2)
					not_deleted = False
				else:
					p2 += 1
			if(not_deleted):
				p1 += 1
	
	def empty_cells(self):
		empty = []
		for r in range(self.size):
			column=list(filter( lambda c:self.data[r][c]==' ', range(self.size)))
			empty.append(column)
		return empty
	
	def indices(self, index):
		if (index == 0):
			return (index, index+1)
		elif(index == self.size-1):
			return (index-1, index)
		else:
			return (index-1, index, index+1)


if __name__ == '__main__':
	Game = tk.Tk( )
	Game.title('Minesweeper')
	
	size = 10
	no_of_mines = 16
	
	g_data = game_data(size, no_of_mines)
	data = g_data.data
	clusters = g_data.clusters
	
	game_play(data, clusters, size)
	
	Game.mainloop( )
