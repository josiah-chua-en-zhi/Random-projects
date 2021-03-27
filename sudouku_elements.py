def map_(fn,lst):
    if lst==[]:
        return lst
    else:
        return fn(lst[0])+map_(fn,lst[1:])

class Square(object):
    def __init__(self,coord,value):
        self.coord=coord
        self.value=value

    def get_row(self):
        return self.coord[0]

    def get_col(self):
        return self.coord[1]

    def get_value(self):
        return self.value

    def get_coord(self):
        return self.coord

    def get_box_number(self):
        row=self.coord[0]//3
        col=self.coord[1]//3
        return row*3+col+1

class Empty_Square(Square):
    def __init__(self,coord,possible_numbers):
        super().__init__(coord,0)
        self.possible_numbers=possible_numbers

    def remove_possible_numbers(self,n):
        if n in self.possible_numbers:
            self.possible_numbers.remove(n)

    def get_possible_numbers(self):
        return self.possible_numbers
        
        
class Matrix(object):
    
    def __init__(self,matrix):
        self.matrix=matrix


    def get_row(self,coord):
        return self.matrix[coord[0]]
    
    def get_col(self,coord):
        return self.transpose()[coord[1]]

    def get_box(self,coord):
        x = coord[0] // 3
        y = coord[1] // 3
        box=[]
        for i in range(x*3, x*3 + 3):
            for j in range(y * 3, y*3 + 3):
                box+=[self.matrix[i][j]]
        return box
            
    def transpose(self):
        new_matrix=[]
        for i in range(len(self.matrix)):
            row=[]
            for j in range(len(self.matrix[i])):
                row.append(self.matrix[j][i])
            new_matrix+=[row,]
        return new_matrix
    
    def print_matrix(self):
        for n in range(0,9):
            print(self.matrix[n])
        
    def get_matrix(self):
        return self.matrix

    def get_square(self,coord):
        return self.get_matrix()[coord[0]][coord[1]]
    
            
class Sudouku(Matrix):
    def __init__(self):
        self.matrix=empty_matrix
        
        
    def create_sudouku(self,m):
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    x = i // 3
                    y = j // 3
                    box=[]
                    for k in range(x*3, x*3 + 3):
                        for l in range(y * 3, y*3 + 3):
                            box+=[m[k][l]]
                    possible_numbers=[1,2,3,4,5,6,7,8,9]
                    surrounding_numbers=m[i]+map_(lambda x: [x[j],],m)+box
                    for number in surrounding_numbers:
                        if number in possible_numbers:
                            possible_numbers.remove(number)
                    self.matrix[i][j]=Empty_Square([i,j],possible_numbers)
                    #print(self.matrix[i][j].get_coord(),self.matrix[i][j].get_possible_numbers()) ##TESTER
                    if self.matrix[i][j].get_possible_numbers()==[]:
                        return 'Invalid Sudouku'
                else:
                    self.matrix[i][j]=Square([i,j],m[i][j])

    def fill_in_sudouku(self,coord,number):
        self.matrix[coord[0]][coord[1]]=Square(coord,number)

    def get_surrounding_possible_squares(self,coord):
        area=self.get_row(coord)+self.get_col(coord)+self.get_box(coord)
        surrounding_numbers=[]
        #print(area)
        for square in area:
            if isinstance(square,Empty_Square):
                if square.get_coord()!=coord:
                    surrounding_numbers.append(square)
        return surrounding_numbers


    def flatten(self):
        lst=[]
        for row in self.get_matrix():
            lst+=row
        return lst

    def get_sudouku_values(self):
        matrix=[]
        for rows in self.get_matrix():
            row=[]
            for square in rows:
                row.append(square.get_value())
            matrix+=[row,]
        return matrix

    def print_sudouku(self):
        for rows in self.get_matrix():
            row=[]
            for square in rows:
                row.append(square.get_value())
            print(row)



empty_matrix=[[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]