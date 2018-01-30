# vim:set ff=unix expandtab ts=4 sw=4:

class DataFrame(list):
    def __init__(self, list_of_rows = []):
        #fr means first row
        
        if list_of_rows:
            fr = list_of_rows[0]
            # list of lists given?
            if type(fr) != type([]):
                raise(Exception("'" + fr + "' is not a list"))

            nc = len(fr) # for number of columns
            for el in fr:
                if type(el) != type(""):
                    raise(Exception("The first list will represent the header of the table and should only contain strings"))
            nc = len(fr) # for number of columns
            for row in list_of_rows:
                if len(row) != nc:
                    raise(Exception("All lists in the list of lists  must have the same length, since the resulting table has a fixed number of columns"))
            self.list_of_rows = list_of_rows
        else:
            self.list_of_rows = []


    @classmethod
    def from_columns(cls, head, list_of_cols = []):
        lor = [head]
        
        for rn in range(len(list_of_cols[0])):
            lor.append([list_of_cols[cn][rn] for cn in range(len(list_of_cols))])

        return cls(lor)


    def __str__(self):
        # get maximum lengths of columns for formatting
        lens = []
        for col_name in self.head:
            l = [col_name]
            l += self.get_column(col_name)

            lens.append(max([len(str(e)) for e in l]))

        #result = str(self.head)
        #for row_index in range(1, self.nrow+1):
        #    result += "\n" + str(self.get_row(row_index))
        result = "  ".join([('{:>'+str(lens[col_nr])+'}').format(str(col_name)) for col_nr, col_name in enumerate(self.head)]) + "\n"
        result += '-'*(len(result)-1) + "\n"
        for row in self.rows:
            result += "  ".join([('{:>'+str(lens[col_nr])+'}').format(str(col_name)) for col_nr, col_name in enumerate(row)]) + "\n"
        
        return result


    @property
    def nrow(self):
        return(len(self.list_of_rows)-1) # -1 because the head is not counted


    @property 
    def ncol(self):
        return(len(self.head))
   

    def get_row(self, row_number):
        # row_mumber = 0 means the head line of the DataFrame
        # return a list
        return self.list_of_rows[row_number]


    @property
    def head(self):
        return self.get_row(0)


    @property
    def rows(self):
        return self.list_of_rows[1:] # do not return head


    @property
    def rows_as_dictionary(self):
        list_of_dics = []
        for row in self.rows:
            dic = {}
            for index in range(len(self.head)):
                dic[self.head[index]] = row[index]
            list_of_dics.append(dic)
        return list_of_dics        


    def get_column_index(self, column_head):
        # return the column index belonging to column_head
        # column_head is a either a string
        # or an integer as is working on lists
        
        col_index = None

        if isinstance(column_head, int):
            col_index = column_head
        elif isinstance(column_head, str):
            head = self.head
            #for col_index, ch in enumerate(head):
            #    if ch == column_head:
            #        break
            try:
                col_index = head.index(column_head)
            except ValueError:
                # column_head is no head in the DataFrame
                raise(KeyError("There is no column head called " + column_head))
        return col_index
            

    def get_column(self, column_head):
        # return a list without column head
        col_index = self.get_column_index(column_head)
        col_list = []
        for row_index in range(1, len(self.list_of_rows)):
            col_list.append(self.list_of_rows[row_index][col_index])
        return col_list
        
        
    def __getitem__(self, index_tuple):
        # slicing in first argument possible
        # return a list without head
        # counting: row_index = 0 means first line below the head
        row_index = index_tuple[0] 
        column_head = index_tuple[1]


        column = self.get_column(column_head)
        return column[row_index]
        

    def column_empty(self, column_head):
        col = self.get_column(column_head)

        empty = True
        for entry in col:
            if entry:
                empty = False

        return empty


    def remove_column(self, column_head):
        col_index = self.get_column_index(column_head)
        for row_index in range(0, len(self.list_of_rows)):
            del self.list_of_rows[row_index][col_index]
    

    def remove_empty_columns(self):
        empty_column_list = []
        for column_head in self.head:
            if self.column_empty(column_head):
                empty_column_list.append(column_head)

        for col in empty_column_list:
            self.remove_column(col)


    def append_column(self, column_head, column_list):
        # add a column at the end of the data frame
        if len(column_list) != self.nrow:
            raise(Exception("The new column has the wrong length."))

        self.list_of_rows[0].append(column_head)
        for row_index in range(1, len(self.list_of_rows)):
            self.list_of_rows[row_index].append(column_list[row_index-1])


    def append_row(self, row_list):
        # add a row to the end of the data frame
        if len(row_list) != self.ncol:
            raise(Exception("The new row has the wrong length."))

        self.list_of_rows.append(row_list)
            

    def sub_df(self, head = [], conditions = {}):
        # return sub data frame with head meeting the conditions given as dictionary, like {'Year': '2000', 'Month': '8'}
        if not head: 
            head = self.head
        
        if type(head) != type([]):
            raise(Exception(head + " is not a list"))

        lor = []
        lor.append(head)
        for line_dic in self.rows_as_dictionary:
            cond_met = True            
            for cond_dic in conditions.items():
                if not cond_dic[0] in line_dic.keys():
                    raise(KeyError("There is no column head called " + cond_dic[0]))
                    
                if line_dic[cond_dic[0]] != cond_dic[1]:
                    cond_met = False

            if cond_met:
                row = []
                for col_head in head:
                    if not col_head in line_dic.keys():
                        raise(KeyError("There is no column head called " + col_head))

                    row.append(line_dic[col_head])
                lor.append(row)
        return DataFrame(lor)
                
    
    def column_average(self, colname_list):
        # return a list containig the averages of the columns in colname_list

        def list_avg(lst):
            s = 0
            nr = 0
            # ignore empty values
            for el in lst:
                if el != None:
                    s += float(el)
                    nr += 1
            return s/nr

        if type(colname_list) != type([]):
            raise(Exception(colname_list + " is not a list"))

        # if no rows return emtpy list of the length of colname_list
        if self.nrow == 0:
            return [None]*len(colname_list)

        result = []
        for colname in colname_list:
            result.append(list_avg(self[:,colname]))

        return result


    # needs a test
    def average(self, colname_list = [], conditions = {}):
        # return a list beginning with the values given in conditions, followed by the averages of the columns in colname_list over the rows that meet the conditions
        # first part needs to be sorted because the order of keys/values in a dictionary is not clear

        if colname_list == []:
            return []

        if type(colname_list) != type([]):
            raise(Exception(colname_list + " is not a list"))

        sub_df = self.sub_df(colname_list, conditions)

        sorted_keys = sorted(list((conditions)))
        result = []
        for key in sorted_keys:
            result.append(conditions[key])

        result += sub_df.column_average(colname_list)
        return result

    #fixme: to be tested
    def get_by_cond(self, target, condition, value):
        #example: get 'name' where 'condition' == 'value'
        if target in self.head and condition in self.head:
            for i, c in enumerate(self.get_column(condition)):
                if c == value:
                    return self[i, target]

        return None


#    def add_row(self, new_row, position = -1):
#        # insert row into data frame
#        # position = 1: immediately below the head
#
#        if position == -1:
#            position = self.nrow + 1 # insert new_line at the end
#
#        self.list_of_rows.insert(position, new_row)
#
#    def remove_head(self):
#        del self.list_of_rows[0]

#    def change_head(self, new_head):
#        self.list_of_rows[0] = new_head
