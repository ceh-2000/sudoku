# Sudoku

# Clare Heinbaugh
# 11/9/2017

import time #use to time code
import cProfile #use to check run time of individual methods
import itertools #use to find combination of cell indicies in twin_eval method (find sudoku twins)

global box_size #puzzle box size
global puzzle_size #puzzle width

#only thing to change to switch from 4 by 4 to 9 by 9; type "2" for 4 by 4 and "3" for 9 by 9
box_size = 3
puzzle_size = box_size * box_size

#file name formated (size of puzzle)_by_(size of puzzle).txt; CHANGE IF FILE HAS A DIFFERENT NAME NOT BASED ON PUZZLE SIZE
file_name = str(puzzle_size)+"_by_"+str(puzzle_size)+".txt"

# Dictionary of all puzzles. Key is which number puzzle is from file.
global puz_dict
puz_dict = {}

global correct_set
correct_set = set()

global dict_for_cells
dict_for_cells = {}  # assigns matrices values to values in puzzle (can know which row and which col)

global mark_dict_length
mark_dict_length = {} #relates number or markup values to puzzle index

global row_col_dict
row_col_dict = {}


#map each index to its row,column counterpart
def make_row_col_dict():
    i = 0
    for r in range(puzzle_size):
        for c in range(puzzle_size):
            row_col_dict[i] = (r,c)

            i+=1

class Puzzle:
    # make a default list that will be filled in with fill_puz to create a matrix
    # only thing puzzle knows about itself is its matrix configuration
    def __init__(self, s):
        self.puz_mat = []
        self.str_rep = s
        self.dict_of_boxes = {}
        # makes empy dictionary where box number maps to nothing
        for i in range(puzzle_size):
            self.dict_of_boxes[i] = [] #append empty lists to box dictionary; fill boxes with values later

        self.mark_dict = {}
        for r in range(puzzle_size):
            self.puz_mat.append(".") #use "." for blanks

    # fill puzzle with values passed as a string
    def fill_puz(self, str_puzzle):  # parameter: string representing puzzle
        num = 0
        #create rows
        for r in range(puzzle_size):
            self.puz_mat[r] = []
            #create columns
            for c in range(puzzle_size):
                self.puz_mat[r].append(str_puzzle[num])
                num += 1

    # store values in same box in dictionary where index is box number
    def make_boxes(self):
        # fills boxes with values from puzzles
        for j in range(puzzle_size*puzzle_size):
            box_num = self.get_box(j)
            self.dict_of_boxes.get(box_num).append(self.str_rep[j]) #WRONG??????

    #generate set of possible values for value at each index
    def make_markup(self):
        for i in range(puzzle_size * puzzle_size):
            self.mark_dict[i] = self.get_mark(i)


    def get_mark(self, i):
        if(self.str_rep[i]!="."):
            return set()

        r_set = self.get_row_set(i)
        c_set = self.get_col_set(i)
        b_set = self.get_box_set(i)
        ch_set = set(chars)

        mark_up = ch_set - r_set - c_set - b_set
        return mark_up

    #update markup for single square that has been evaluated
    def update_mark(self, i, value): #delete values from neighbors
        a = set()
        a.add(value) #make subtractable set with only value "value" in it
        self.mark_dict[i] = set() #since value at index i has been evaluated, set markup set to empty

        ya = i // puzzle_size

        row = row_dict.get(ya)

        for r in row: #update all values in same row as square at index i
            cur = self.mark_dict.get(r)
            if(cur!=None):
                cur = cur-a
            self.mark_dict[r] = cur


        ya = i % puzzle_size

        col = col_dict.get(ya)

        for c in col: #update all values in same column as square at index i
            cur = self.mark_dict.get(c)
            if(cur!=None):
                cur = cur - a
            self.mark_dict[c] = cur


        rc_tup = row_col_dict.get(i)  # get value tuple of row and column that matches current index
        la = rc_tup[0] // box_size * box_size
        sa = rc_tup[1] // box_size
        box_num = la + sa

        box = box_dict.get(box_num)

        for b in box: #update all values in same row as square at index i
            cur = self.mark_dict.get(b)
            if(cur!=None):
                cur = cur - a
            self.mark_dict[b] = cur

    #get box number of value at index i
    def get_box(self, i):
        rc_tup = row_col_dict.get(i)
        r = rc_tup[0]
        c = rc_tup[1]
        row = r // box_size * box_size
        col = c // box_size
        box_num = row + col
        return box_num


    #return string representation of contents in column with value at index i
    def get_row_set(self, i):
        r = row_col_dict.get(i)[0]
        return set(self.puz_mat[r])

    #return string representation of contents in column with value at index i
    def get_col_set(self, i):
        c = row_col_dict.get(i)[1]
        check_string = set()
        for r in range(puzzle_size):
            check_string.add(self.puz_mat[r][c])
        return check_string

    #return string representation of contents in box with value at index i
    def get_box_set(self, i):
        box_num = self.get_box(i)
        a = set(self.dict_of_boxes[box_num])
        return a

    #get smallest markup length index
    def get_least(self):
        min = 0
        min_value = 9
        for c in range(puzzle_size * puzzle_size):
            temp_min = len(self.mark_dict.get(c))
            if(temp_min==1):
                return c
            if (temp_min > 0 and temp_min < min_value):
                min = c
                min_value = temp_min
        return min

    #get largest markup length
    def get_most(self):
        for i in range(puzzle_size*puzzle_size):
            if(len(self.mark_dict.get(i)) > 0):
                return 5
        return 0

    # create string that formats a puzzle for printing
    def pretty(self):
        s = ""
        for r in range(puzzle_size):
            if (r % box_size == 0 and r != 0):
                for p in range(puzzle_size * 2 +1):
                    s += "-" #use to separate boxes
                s += "\n"
            for c in range(puzzle_size):
                if (c % box_size == 0 and c != 0):
                    s += "|" #use to separate boxes
                s += self.puz_mat[r][c] + " "
            s += "\n"
        return s

#read all puzzles from text file
def read_in_puzzles():
    with open(file_name, "r") as myfile:  # text file has list of all puzzles
        data = myfile.read()
    values = data.split("\n") #split on each line (each line is a puzzle)
    num = 1
    for c in values:
        if (c != ""):
            cur = Puzzle(c)  # each puzzle is default at the beginning
            cur.fill_puz(c)  # fill puzzle with values read in from text file
            puz_dict[num] = cur #map puzzle number to puzzle
        num += 1 #iterate puzzle number

global row_dict
row_dict = {}

#make dictionary of indicies in same row
def make_row_dict():
    for j in range(puzzle_size):
        row_dict[j] = set()
    for i in range(puzzle_size*puzzle_size):
        row_num = i//puzzle_size
        row_dict.get(row_num).add(i)


global col_dict
col_dict = {}

# make dictionary of indicies in same column
def make_col_dict():
    for j in range(puzzle_size):
        col_dict[j] = set()
    for i in range(puzzle_size * puzzle_size):
        col_num = i % puzzle_size
        col_dict.get(col_num).add(i)

global box_dict
box_dict = {}

# make dictionary of indicies in same column
def make_box_dict():

    #create empty sets to eventually hold all indicies in a specific box
    for j in range(puzzle_size):
        box_dict[j] = set()

    for i in range(puzzle_size * puzzle_size):
        rc_tup = row_col_dict.get(i)  # get value tuple of row and column that matches current index

        #formula to determine which boz an index is in
        a = rc_tup[0] // box_size
        b = rc_tup[1] // box_size
        box_num = a*box_size+b

        #add index to correct box; boxes numbered starting with 0 up to 1 less than size of puzzle
        box_dict.get(box_num).add(i)


# generate the solution set of values for one row, column, or box
def make_correct_set():
    for i in range(puzzle_size):
        correct_set.add(str(i + 1))

#update string representation of puzzle
def update_str(s,i,ch):
    new = list(s)
    new[i] = ch
    return ''.join(new)


def get_groups(puz):
    #make a set of all groups: row indices, column indicies, and box indicies
    groups = set()
    for r in row_dict.keys():
        groups.add(tuple(row_dict.get(r)))
    for c in col_dict.keys():
        groups.add(tuple(col_dict.get(c)))
    for b in box_dict.keys():
        groups.add(tuple(box_dict.get(b)))

    #make set of all indices with empty cells
    empty_set = set()
    #make set of all indicies with filled-in cells
    filled_set = set()
    for i in range(puzzle_size*puzzle_size):
        if(puz.str_rep[i]=="."):
            empty_set.add(i)
        else:
            filled_set.add(i)

    return (groups, empty_set, filled_set)

################################################################
#single possibility rule
#singleton: cell in group that is the only cell with a specific mark-up value in group
def find_hidden_singles(puz):

    groups_tup = get_groups(puz)

    groups = groups_tup[0]
    empty_set = groups_tup[1] #set of all indicies of cells in the puzzle that are blank
    filled_set = groups_tup[2]


    for g in groups: #current group of interest
        set_union = set(g) & empty_set
        for cur in set_union: #current index in group
            master_set = set()

            #iterate through values other than the one in the current group and add their mark-ups to master-set
            for f in g:
                if(f!=cur):
                    master_set = master_set | puz.mark_dict.get(f) #add mark-ups of cells other than current cell to master-set

            #subtract mark-ups of other cells from current cell's mark-up and see if there is a hidden singleton
            subtracted_set = puz.mark_dict.get(cur) - master_set

            #if there is a hidden singleton, change current cell's mark-up to only that one singleton value
            if(len(subtracted_set)>0):
                puz.mark_dict[cur] = subtracted_set



################################################################

#finds "twins" in puzzle
#if two or more cells in the same group in the puzzle have the same mark-up set of a certain length, k,
# then all other cells in that puzzle can't have those mark-up values
def twin_eval(puz):

    groups_tup = get_groups(puz)

    groups = groups_tup[0]
    empty_set = groups_tup[1]
    filled_set = groups_tup[2]

    #make cell combinations of size: 2 to length of puzzle
    for k in range(2,puzzle_size):
        for g in groups:
            #set-union only holds indicies of blank cells
            set_union = set(g) & empty_set

            #use itertools to make combinations (choose k elements)
            j = list(itertools.combinations(set_union, k))

            for m in j: #iterate through each itertool combination set
                new_set = set()
                for p in m: #iterate through indicies in current combination
                    cur_mark = puz.mark_dict.get(p) #current index's mark-up

                    # find union of mark-ups at current index and other mark-ups in current combination of indicies
                    new_set = new_set | cur_mark

                #check if we found a "twin"
                if(len(new_set)==k):
                     #delete values in new-set from other mark-ups in current group
                     remove_set = set(g) - set(m) - filled_set
                     for o in remove_set:
                         check_mark = puz.mark_dict.get(o) #get mark-up of cell in group
                         new_mark_up = check_mark - new_set #elimate twin mark-up values from non-twins
                         puz.mark_dict[o] = new_mark_up #set new mark-up for non-twin

################################################################

# create temporary puzzle with new value at index i
def make_temp(puz, value, i):
    rc_tup = row_col_dict.get(i) #row_col_dict relates row,col to string index
    r = rc_tup[0] #use row_col_dict to get row
    c = rc_tup[1] #use row_col_dict to get row
    temp = Puzzle(puz.str_rep)  # set string representation of temporary puzzle
    temp.str_rep = update_str(temp.str_rep, i, value)  # set string value at i equal to value
    temp.puz_mat = puz.puz_mat.copy() #copy the puzzle matrix to temp
    temp.puz_mat[r][c] = value #change the current cell index value to the new temporary value for temp puzzle
    temp.dict_of_boxes = puz.dict_of_boxes.copy() #copy the box dictionary
    temp.dict_of_boxes.get(temp.get_box(i))[i // puzzle_size] = value  # update the box dictionary for temporary puzzle
    return temp #return the temporary puzzle with only one value changed

#Recursive method used to solve puzzles WITH MARKUPS
def solve_puz_with_marks(puz, i):

    #base case to see if solution was found
    if(puz.get_most()==0): #check if there are any mark-up values left to evaluate
        if("." not in puz.str_rep): #check if there are any blanks left
            return puz #return solution puzzle
        #return None if solution not found because there was a mistake and a different path is correct
        return None

    else:
        # iterate through each possible value of puzzle at current index
        for j in puz.mark_dict.get(i):
            # create temporary puzzle and add in each possible number at the specified index
            # do not change current puzzle
            value = str(j)  # value being tested at current index i
            temp = make_temp(puz, value, i)

            temp.mark_dict = puz.mark_dict.copy()
            temp.update_mark(i, value) #update a cell's mark-up and others in the same group cell is changed from a blank to a number
            find_hidden_singles(temp) #see if there is a value in one of the groups that is a singleton

            # call recursive method
            solution = solve_puz_with_marks(temp, temp.get_least())

            #return if a solution was found
            if(solution != None):
                return solution

        return None

################################################################

def main():
    # make string of all possible number values
    global chars
    chars = ""
    for i in range(puzzle_size):
        chars = chars + str(i + 1)

    make_row_col_dict() #relate row and column to index
    read_in_puzzles()  # make dictionary of all puzzles from file
    make_correct_set()  # create set of correct values

    #create dictionaries of indicies in each row, column, and box
    make_row_dict()
    make_col_dict()
    make_box_dict()


    #set the starting puzzle number
    num = 1
    #num = int(input("Which puzzle? ")) #uncomment to allow user to choose puzzle to start with

    tick = time.time() #start timing as puzzles are read in

    while num <= len(puz_dict.keys()): #will iterate through all puzzles in file

        current_puz = puz_dict.get(num)
        print("Puzzle Number: ", num)
        print("Unsolved: ")
        print(current_puz.pretty())
        current_puz.make_boxes()

        current_puz.make_markup()

        find_hidden_singles(current_puz) #find all hidden singles (singletons) before starting to solve
        twin_eval(current_puz) #find all puzzle "twins"

        print("Solved: ")

        temp = solve_puz_with_marks(current_puz, current_puz.get_least())  # calls recursive method to solve each puzzle

        print(temp.pretty()) #print the solution
        num += 1 #iterate to next puzzle from 137-puzzle file

    tock = time.time() #get time when puzzles are all solved

    print("Time: ", tock-tick)


if __name__ == "__main__":
    main()
