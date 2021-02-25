# This is a simple minesweeper game
# In this game, 'O' represents Mines

import tkinter as tk
import random

class Buttons_init:
    def __init__(self,R,C):
        self.row = R
        self.column = C
        self.button = tk.Button( Game, text=" ", command = self.clicked,bg = "grey", 
                                 activebackground = "white", height=1, width=1)
        self.button.grid(row=self.row, column=self.column)
buttons[self.row,self.column]=self.button
	
    def clicked( self ):
        if(game_data[ self.row, self.column ]=="O"):    # if there is Mine, Game over
            buttons[self.row, self.column].configure(activebackground="red",bg="red" )
            game_over()
        # if empty cell, clear neighbour empty cells
        if(game_data[ self.row, self.column ]==" "):
            clear_blocks(self.row, self.column)
        else:
            buttons[self.row, self.column].configure(text=game_data[ self.row, self.column ])
            buttons[self.row, self.column].configure(bg = "white")
    # this function starts when Mine is clicked
    def game_over():
        for  i in range( 23 ):
            for  j in range( 8 ):
                buttons[i,j].configure(text=game_data[i,j])
                buttons[i,j].configure(bg='white')

# this function clears neighbouring empty cells when an empty cell is clicked
def clear_blocks(r,c):
    for block in empty_blocks.values():
        if ((r,c) in block):
            for (rr,cc) in block:
                buttons[rr,cc].configure(text=game_data[rr,cc])
                buttons[rr,cc].configure(bg = "white")
            break

def counter( R,C ):
    rl = start( R, 22)
    cl = start( C, 7 )
    count = 0
    for r in rl:
        for c in cl:
            if (game_data[r,c] == 'O'):
                count += 1
    return count

def start(rc,lm):
    if (rc == 0):
        x=[rc,rc+1]
    elif(rc == lm):
        x=[rc-1,rc]
    else:
        x=[rc-1,rc,rc+1]
    return (x)

def empty_blocks_func(er,ec):
    flag=False
    global num
    if((empty_blocks != {})):
        rl = start( er,22)
        cl = start( ec,7)
        for rr in rl:
            for cc in cl:
                if (empty[rr,cc] == "x"):
                    for block in empty_blocks.values():
                        if((rr,cc) in block):
                            block.add((er,ec))
                            flag=True
    if((empty_blocks=={}) or (flag is False)):
    empty_blocks[ num ] = set( )
    empty_blocks[ num ].add((er,ec))
    num +=1

def merge( ):
    l=len( empty_blocks )
    del_list = [ ]
    for k1 in range(1,l):
        for k2 in range(k1+1,l+1):
            if( empty_blocks[k1].intersection(empty_blocks[k2])):
                if (k2 not in del_list):
                    empty_blocks[k1].update(empty_blocks[k2])
                    del_list.append(k2)
    for key in del_list:
        del empty_blocks[ key ]
    empty_b={}
    for key in empty_blocks.keys():
        empty_b[key] = set( )
    for (r,c) in empty_blocks[key]:
        rl = start(r,22)
	      cl = start(c,7)
        for rr in rl:
            for cc in cl:
                empty_b[ key ].add((rr,cc))
    for key in empty_blocks.keys( ):
        empty_blocks[key].update(empty_b[key])


# From here game begins
# here we initialize game data


Game = tk.Tk( )
# random indices are generated where Mines are placed in game data
mine_index = random.sample(range(8*23),26)    
game_data = { }   # initialize variable to store game data
index=0

# Here 'O' which represents Mines are inserted at mine indices
for i in range(23):
    for j in range(8):
        if (index in mine_index) :
            game_data[i,j] = "O"
        else:
            game_data[i,j] = " "
        index += 1

buttons={ }
empty={ }
num = 1
empty_blocks={ }

# Here, in each cell, a number which represents no of Mines
# around neighbour cells is stored    
for  i in range( 23 ):
    for  j in range( 8 ):
        if ( game_data[i,j] != "O" ):
            count=counter( i, j )
            if(count != 0):
                game_data[i,j]=str(count)
                count = 0
        if (game_data[i,j]==" "):   # empty dict. stores empty cells
            empty[i,j] = "x"
        else:
            empty[i,j] = " "

# Here neighbouring empty cells are grouped
for  i in range( 23 ):
    for  j in range( 8 ):
        if (empty[i,j] == 'x'):
            empty_blocks_func(i,j)

merge()

# Initializing Buttons
for  i in range( 23 ):
    for  j in range( 8 ):
        Buttons_init( i, j )

Game.mainloop( )
