from sudouku_elements import Matrix
from sudouku_elements import Empty_Square
from sudouku_elements import Sudouku
from sudouku_elements import Square
from sudouku_elements import map_


def naked_singles(sudouku):
	s=sudouku.flatten()
	process_possible = True
	all_filled= True
	for square in s:
		if isinstance(square,Empty_Square):
			all_filled=False
			possible_numbers=square.get_possible_numbers()
			print(square.get_coord(),possible_numbers)
			if len(possible_numbers)==1:
				process_possible = False
				sudouku.fill_in_sudouku(square.get_coord(),possible_numbers[0])
				surrounding=sudouku.get_surrounding_possible_squares(square.get_coord())
				for square in surrounding:
					square.remove_possible_numbers(possible_numbers[0])
					
			elif len(possible_numbers)==0:
				return 'sudouku broken'
				break
	if all_filled:
		return 'Finish'
	else:
		return process_possible



def sort_possible_numbers(sudouku):
	all_squares=sudouku.flatten()
	possible_numbers_by_box={}
	possible_numbers_by_col={}
	possible_numbers_by_row={}
	for square in all_squares:
		if isinstance(square,Empty_Square):
			square_possible_numbers=square.get_possible_numbers()
			coord = square.get_coord()
			square_box_number=square.get_box_number()
			square_row_number=square.get_row()
			square_col_number=square.get_col()
			for number in square_possible_numbers:
				put(possible_numbers_by_box,square_box_number,number,coord)
				put(possible_numbers_by_row,square_row_number,number,coord)
				put(possible_numbers_by_col,square_col_number,number,coord)
	return [possible_numbers_by_box,possible_numbers_by_row,possible_numbers_by_col]

def put(dic,key1,number,values):
	if key1 not in dic.keys():
		dic[key1]={}
		dic[key1][number]=[]
		dic[key1][number]+=[values,]
	else:
		if number not in dic[key1].keys():
			dic[key1][number]=[]
			dic[key1][number]+=[values,]
		else:
			dic[key1][number]+=[values,]

def get_remove_from_other_squares_r_c(dic):
	remove_from_other_squares_row=[]
	remove_from_other_squares_col=[]
	boxes=dic.keys()
	for box in boxes:
		numbers=dic[box].keys()
		for number in numbers:
			coords=dic[box][number]
			same_row=test_rows_cols(coords,'row')
			same_col=test_rows_cols(coords,'col')
			if same_row !=False:
				remove_from_other_squares_row+=[[[same_row],number,coords],]
			elif same_col != False:
				remove_from_other_squares_col+=[[[same_col],number,coords],]
	print("get_remove_from_other_squares_r_c",[remove_from_other_squares_row,remove_from_other_squares_col] )
	return [remove_from_other_squares_row,remove_from_other_squares_col]

def test_rows_cols(coords,r_c):
	number=0
	return_=True
	if r_c=='row':
		n=0
	else:
		n=1
	for i in range(len(coords)):
		if i==0:
			number=coords[i][n]
		else:
			if coords[i][n] == number:
				continue
			else:
				return_=False
	if return_:
		return number 
	else:
		return False


def determine_only_possibilities_in_square(dic):
	only_possibilities_in_square=[]
	areas=dic.keys()
	for area in areas:
		sort={}
		numbers=dic[area].keys()
		for number in numbers:
			coords=dic[area][number]
			for coord in coords:
				put(sort,len(coords),number,coord)
		lengths=sort.keys()
		for length in lengths:
			numbers_=list(sort[length].keys())
			if length == len(numbers_):
				fixed_set=True
				current_coords=sort[length][numbers_[0]]
				for i in range(len(numbers_)):
					if test_if_coords_are_same(sort[length][numbers_[i]],current_coords):
						continue
					else:
						fixed_set=False
				if fixed_set:
					only_possibilities_in_square+=[[numbers_,current_coords]]	
	print("only_possibilities_in_square", only_possibilities_in_square)	
	return only_possibilities_in_square

def test_if_coords_are_same(coords1,coords2):
	same= True
	if len(coords1)!=len(coords2):
		same=False
	for coord in coords1:
		if coord not in coords2:
			same=False
	return same 

def determine_cross_box_elimination_numbers(dic,n,m):
	big_rows=[[0,1,2],[3,4,5],[6,7,8]]
	cross_box_elimination=[]
	for big_row in big_rows:
		numbers=range(1,10)
		for number in numbers:
			distribution_1=[[],[]]
			distribution_2=[[],[]]
			distribution_3=[[],[]]
			for rows in big_row:
				if rows in list(dic.keys()):
					if number in list(dic[rows].keys()):
						possible_coords=dic[rows][number]
						for coord in possible_coords:
							if coord[m]<3:
								distribution_1[1].append(coord)
								if coord[n] not in distribution_1[0]:
									distribution_1[0].append(coord[n])
							elif coord[m]>2 and coord[m]<6:
								distribution_2[1].append(coord)
								if coord[n] not in distribution_2[0]:
									distribution_2[0].append(coord[n])
							elif coord[m]>5:
								distribution_3[1].append(coord)
								if coord[n] not in distribution_3[0]:
									distribution_3[0].append(coord[n])
			count=3
			filtered_distribution=[]
			distributions=[distribution_1,distribution_2,distribution_3]
			for distribution in distributions:
				if distribution==[[],[]]:
					count-=1
				else: 
					filtered_distribution+=[distribution,]
			if count==3:
				break_=False
				for i in range(count):
					if break_:
						break
					for j in range(count):
						if i!=j and filtered_distribution[j][0]==filtered_distribution[i][0] and len(filtered_distribution[j][0])==count-1:
							a=[0,1,2]
							a.remove(i)
							a.remove(j)
							if len(filtered_distribution[a[0]][0])==count:
								cross_box_elimination+=[[filtered_distribution[j][0],number,filtered_distribution[j][1]+filtered_distribution[i][1]],]
								break_=True
								break
			elif count==2:
				if len(filtered_distribution[0][0])>len(filtered_distribution[1][0]) and len(filtered_distribution[1][0])==1 and filtered_distribution[1][0][0] in filtered_distribution[0][0]:
					cross_box_elimination+=[[filtered_distribution[1][0],number,filtered_distribution[1][1]],]
				elif len(filtered_distribution[1][0])>len(filtered_distribution[0][0]) and len(filtered_distribution[0][0])==1 and filtered_distribution[0][0][0] in filtered_distribution[0][0]:
					cross_box_elimination+=[[filtered_distribution[0][0],number,filtered_distribution[0][1]],]
	print("cross_box_elimination", cross_box_elimination)
	return cross_box_elimination


def process_possible_numbers(sudouku):
	possible_numbers_by_box=sort_possible_numbers(sudouku)[0]
	possible_numbers_by_row=sort_possible_numbers(sudouku)[1]
	possible_numbers_by_col=sort_possible_numbers(sudouku)[2]
	remove_from_other_squares_row=get_remove_from_other_squares_r_c(possible_numbers_by_box)[0]
	remove_from_other_squares_col=get_remove_from_other_squares_r_c(possible_numbers_by_box)[1]
	only_possibilities_in_square_by_box=determine_only_possibilities_in_square(possible_numbers_by_box)
	only_possibilities_in_square_by_row=determine_only_possibilities_in_square(possible_numbers_by_row)
	only_possibilities_in_square_by_col=determine_only_possibilities_in_square(possible_numbers_by_col)
	cross_box_elimination_row=determine_cross_box_elimination_numbers(possible_numbers_by_row,0,1)
	cross_box_elimination_col=determine_cross_box_elimination_numbers(possible_numbers_by_col,1,0)
	s=sudouku.flatten()
	for square in s:
		if isinstance(square,Empty_Square):
			remove_possibilities(remove_from_other_squares_row,0,square)
			remove_possibilities(remove_from_other_squares_col,1,square)
			remove_possibilities(cross_box_elimination_row,0,square)
			remove_possibilities(cross_box_elimination_col,1,square)
			remove_non_possibilities(only_possibilities_in_square_by_box,square)
			remove_non_possibilities(only_possibilities_in_square_by_row,square)
			remove_non_possibilities(only_possibilities_in_square_by_col,square)



def remove_possibilities(lst,n,square):
	coord=square.get_coord()
	possible_numbers=square.get_possible_numbers()
	for term in lst:
		r_c=term[0]
		number=term[1]
		coords=term[2]
		if coord[n] in r_c and number in possible_numbers and coord not in coords:
			square.remove_possible_numbers(number)

def remove_non_possibilities(lst,square):
	coord=square.get_coord()
	possible_numbers=square.get_possible_numbers()
	for term in lst:
		numbers=term[0]
		coords=term[1]
		if coord in coords:
			for number in possible_numbers:
				if number not in numbers:
					square.remove_possible_numbers(number)

	

def solve(sudouku):
	sudouku.print_sudouku()
	sort_sudouku=naked_singles(sudouku)
	if sort_sudouku == True:
		process_possible_numbers(sudouku)
		solve(sudouku)
	elif sort_sudouku== 'sudouku broken':
		return print('sudouku broken')
	elif sort_sudouku== 'Finish':
		return print('Finish')
	else:
		solve(sudouku)

matrix=[[0,7,0,0,0,4,0,0,2],
        [0,0,1,0,3,0,0,4,0],
        [0,0,0,5,0,0,1,0,0],
        [0,4,0,0,0,3,0,0,8],
        [0,0,3,0,0,0,7,0,0],
        [1,0,0,6,0,0,0,9,0],
        [0,0,4,0,0,1,0,0,0],
        [0,2,0,0,7,0,8,0,0],
        [5,0,0,9,0,0,0,6,0]]

matrix1=[[0,0,6,0,0,0,0,9,0],
      [0,0,0,2,5,0,8,0,7],
      [4,7,0,0,0,0,0,3,0],
      [0,5,3,0,2,9,0,0,0],
      [0,8,0,5,0,6,0,2,0],
      [0,0,0,0,7,0,0,8,0],
      [0,0,0,0,0,5,0,0,9],
      [9,0,0,0,4,1,3,0,0],
      [0,1,0,0,0,0,7,0,0]]

matrix2=[[0,0,5,3,0,0,0,0,0],
        [8,0,0,0,0,0,0,0,2],
        [0,7,0,0,1,0,5,0,0],
        [4,0,0,0,0,5,3,0,0],
        [0,1,0,0,7,0,0,0,6],
        [0,0,3,2,0,0,0,8,0],
        [0,6,0,5,0,0,0,0,9],
        [0,0,4,0,0,0,0,3,0],
        [0,0,0,0,0,9,7,0,0]]

testbest=[[8,0,0,0,0,0,0,0,9],
      [0,0,3,6,0,0,0,0,0],
      [0,7,5,0,9,0,2,0,0],
      [0,5,0,0,0,7,0,0,0],
      [0,0,0,0,4,5,7,0,0],
      [0,0,0,1,0,0,0,3,0],
      [0,0,1,0,0,0,0,6,8],
      [0,0,8,5,0,0,0,1,0],
      [0,9,0,0,0,0,4,0,0]]

        
m=Matrix(matrix1)
s=Sudouku()
s.create_sudouku(m.get_matrix())
solve(s)
