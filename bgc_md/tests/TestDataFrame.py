# vim:set ff=unix expandtab ts=4 sw=4:
from bgc_md.DataFrame import DataFrame
import unittest
import sys
import re as regexp


class TestDataFrame(unittest.TestCase):
    def test_init(self):
        # the init method expects a list of row lists
        # the first row list contains the names of the columns as strings

        # test normal usage
        df = DataFrame([["a","b"],
                        [ 2 , 4 ]])
        
        # test header not consisting of strings
        with self.assertRaises(Exception) as cm:
            df = DataFrame([[1,2],
                            [3,4]])
        e = cm.exception
        self.assertEqual(e.__str__(), "The first list will represent the header of the table and should only contain strings")
        
        # test lists not having the same length
        lor = [["a","b"],
               [ 2 , 4, 5 ]]
        with self.assertRaises(Exception) as cm:
            df = DataFrame(lor)
        e = cm.exception
        self.assertEqual(e.__str__(), "All lists in the list of lists  must have the same length, since the resulting table has a fixed number of columns")

        # test list_of_rows is not a list of lists
        with self.assertRaises(Exception) as cm:
            DataFrame(['a','b'])
        e = cm.exception
        self.assertEqual(e.__str__(), "'a' is not a list")


    def test_from_columns(self):
        head = ['Col1', 'Col2']
        col1 = [1, 2, 3]
        col2 = [4, 5, 6]
        df = DataFrame.from_columns(head, [col1, col2])

        ref = DataFrame([['Col1', 'Col2'],
                         [     1,      4],
                         [     2,      5],
                         [     3,      6]])

        self.assertEqual(df, ref)


    def test_str(self):
        df = DataFrame([['Column 1', 'B'],
                        [13, 'long text']])
        lines = df.__str__().splitlines()
        self.assertEqual(lines[0], 'Column 1          B')
        self.assertEqual(lines[1], '-------------------')
        self.assertEqual(lines[2], '      13  long text')


    def test_get_row(self):
        df = DataFrame([["a","b"],
                        [ 1 , 2 ]])

        # test normal usage
        result = df.get_row(1)
        self.assertEqual(result, [1,2])

        # test index error
        with self.assertRaises(IndexError):
           result = df.get_row(2)

 
    def test_head(self):
        df = DataFrame([["a","b"],
                        [ 1 , 2 ]])

        result = df.head
        self.assertEqual(result, ["a","b"])


    def test_nrow(self):
        df = DataFrame([["a","b"],
                      [ 1 , 2 ],
                      [ 3 , 4 ],
                      [ 5 , 6 ]])
        self.assertEqual(df.nrow, 3)


    def test_ncol(self):
        df = DataFrame([["a","b","c"],
                        [1 , 2 , 3]])
        self.assertEqual(df.ncol, 3)


    def test_get_column_index(self):
        # test normal usage
        df = DataFrame([["a","b","c"],
                        [ 1 , 2 , 3]])
        self.assertEqual(df.get_column_index("b"), 1)

        # test invalid head
        with self.assertRaises(KeyError) as cm:
            result = df.get_column_index("d")
        e = cm.exception
        self.assertEqual(e.__str__(), "'There is no column head called d'") # '' apparently needed, because of how KeyError
        

    def test_get_column(self):
        lr = [["a","b"],
              [ 1 , 2 ],
              [ 3 , 4 ],
              [ 5 , 6 ]]
        df = DataFrame(lr)

        # test normal usage with string
        result = df.get_column("b")
        self.assertEqual(result, [2,4,6])
        
        # test normal usage with integers
        result = df.get_column(1)
        self.assertEqual(result, [2,4,6])

        # test invalid head
        with self.assertRaises(KeyError) as cm:
            result = df.get_column("c")
        e = cm.exception
        self.assertEqual(e.__str__(), "'There is no column head called c'") # '' apparently needed, because of how KeyError
                                                                            # error message is built

    def test_append_column(self):
        # test correct use
        df = DataFrame([["a","b"],
                        [ 1 , 2 ],
                        [ 4 , 5 ],
                        [ 7 , 8]])
        new_column = [3,6,9]
        df.append_column("c", new_column)
        self.assertEqual(df.get_column("c"), [3,6,9])

        # test if new column has the wrong length
        new_column = [3,6,9,11]
        with self.assertRaises(Exception) as cm:    
            df.append_column("d", new_column)
        e = cm.exception
        self.assertEqual(e.__str__(), "The new column has the wrong length.")
 

    def test_append_row(self):
        # test correct use
        df = DataFrame([["a","b"],
                        [ 1 , 2 ],
                        [ 4 , 5 ],
                        [ 7 , 8]])
        new_row = [10,11]
        df.append_row(new_row)
        self.assertEqual(df.get_row(4), [10,11])

        # test if new row has the wrong length
        new_row = [3,6,9,11]
        with self.assertRaises(Exception) as cm:    
            df.append_row(new_row)
        e = cm.exception
        self.assertEqual(e.__str__(), "The new row has the wrong length.")


    def test_getitem(self):
        lr = [["a","b","c"], 
              [ 1 , 2 , 3 ], 
              [ 4 , 5 , 6 ], 
              [ 7 , 8 , 9 ]]
        df = DataFrame(lr) 

        # test getting single entry
        # as in R the first argument is the row and the second the column
        result = df[2,"b"]
        self.assertEqual(result, 8)

        ## test slicing in first argument
        result = df[:,"c"]
        self.assertEqual(result, [3,6,9])
        
        ## test slicing in second argument
        #result = df[0,:]
        #self.assertEqual(result, [1,2,3])
       
        ##test indexing with bool list
        #fixme df["a"] would have to give back a 
        #subclass of list for which we could overload bool comparisons
        #the result would be a list of bools 
        #bl=df["a"]<5)
        #which could be used as an idex like in R
        #res=df[bl,:]

    def test_rows(self):
        df = DataFrame([['a','b','c'],
                        [ 1 , 2 , 3 ],
                        [ 4 , 5 , 6 ]])
        lor = df.rows
        self.assertEqual(lor[1], [4,5,6])


    def test_rows_as_dictionary(self):
        df = DataFrame([['a','b','c'],
                        [ 1 , 2 , 3 ],
                        [ 4 , 5 , 6 ]])
        self.assertEqual(df.rows_as_dictionary[1]['b'], 5)


    def test_column_empty(self):
        df = DataFrame([['a','b','c'],
                        [ 1 , '', 3 ],
                        [ 4 , '', 6 ],
                        [ 7 , None,9]])
        self.assertTrue(df.column_empty('b'))
        self.assertTrue(df.column_empty(1))
        self.assertFalse(df.column_empty('c'))


    def remove_column(self):
        df = DataFrame([['a','b','c'],
                        [ 1 , '', 3 ],
                        [ 4 , '', 6 ],
                        [ 7 , None,9]])

        df.remove_column('b')
        self.assertEqual(df[0,1], 3)

        df.remove_column(0)
        self.assertEqual(df[3,0], 9)

        df.remove_column('c')
        self.assertFalse(df)


    def test_remove_empty_columns(self):
        df = DataFrame([['a','b','c'],
                        [ 1 , '', 3 ],
                        [ 4 , '', 6 ],
                        [ 7 , None,9]])
        df.remove_empty_columns
        self.assertTrue([3,1], 9)


    def test_sub_df(self):
        df = DataFrame([['a','b','c'],
                        [ 1 , 2 , 3 ],
                        [ 4 , 0 , 6 ],
                        [ 7 , 0 , 9 ]])

        # test normal usage
        sub_df = df.sub_df(['a','c'], {'b': 0})
        self.assertEqual(sub_df.rows_as_dictionary, [{'a': 4, 'c': 6}, {'a': 7, 'c': 9}])

        # test conditions not met
        sub_df = df.sub_df(['a','c'], {'a': 27})
        self.assertEqual(sub_df.nrow, 0)

        # test empty head
        sub_df = df.sub_df([], {'b': 0})
        print(sub_df)
        self.assertEqual(sub_df.nrow, 2)
        
        # test wrong head
        with self.assertRaises(KeyError) as cm:    
            sub_df = df.sub_df(['a','d'], {'b': 0})
        e = cm.exception
        self.assertEqual(e.__str__(), "'There is no column head called d'")

        # test wrong condition
        with self.assertRaises(KeyError) as cm:
            sub_df = df.sub_df(['a','b'], {'d': 5})
        e = cm.exception
        self.assertEqual(e.__str__(), "'There is no column head called d'")

        # test empty data frame
        sub_df = DataFrame([['a','b']]).sub_df(['a'])
        self.assertEqual(sub_df.head, ['a'])
        self.assertEqual(sub_df.nrow, 0)

        #test one column, not list:
        with self.assertRaises(Exception) as cm:
            df.sub_df('a')
        e = cm.exception
        self.assertEqual(e.__str__(), "a is not a list")

    def test_column_average(self):
        df = DataFrame([['a1','b','c'],
                        [ 1 , 3 , 3 ],
                        [ 4 ,'a', 6 ],
                        [ 7 , 0 , 9 ]])
        
        # test normal usage
        self.assertEqual(df.column_average(['a1','c']), [4.0, 6.0])
        
        # test empty colname_list
        self.assertEqual(df.column_average([]), [])

        # test wrong column name
        with self.assertRaises(KeyError) as cm:
            df.column_average(['d'])
        e = cm.exception
        self.assertEqual(e.__str__(), "'There is no column head called d'")

        # test empty data frame
        self.assertEqual(DataFrame([['a', 'b']]).column_average(['a','b']), [None, None])

        # test NaN
        with self.assertRaises(ValueError) as cm:
            df.column_average(['b'])
        e = cm.exception
        self.assertEqual(e.__str__(), "could not convert string to float: 'a'")

        # test one column, not list
        with self.assertRaises(Exception) as cm:
            self.assertEqual(df.average('a1'), 4.0)
        e = cm.exception
        self.assertEqual(e.__str__(), "a1 is not a list")


    def test_average(self):
        df = DataFrame([['a1','b','c'],
                        [ 1 , 3 , 3 ],
                        [ 4 , 0 , 6 ],
                        [ 7 , 0 ,'h']])
        
        # test normal usage
        self.assertEqual(df.average(['a1','b'], {'b': 0}), [0, 5.5, 0.0])
        
        # test empty colname_list
        self.assertEqual(df.average([], {'a1': 4}), [])

        # test empty conditions
        self.assertEqual(df.average(['a1', 'b']), [4.0, 1.0])

        # test emtpy colname_list and empty_conditions
        self.assertEqual(df.average([], []), [])

        # test wrong column name
        with self.assertRaises(KeyError) as cm:
            df.average(['d'])
        e = cm.exception
        self.assertEqual(e.__str__(), "'There is no column head called d'")

        # test empty data frame
        self.assertEqual(DataFrame([['a', 'b']]).average(['a','b']), [None, None])

        # test NaN
        with self.assertRaises(ValueError) as cm:
            df.average(['c'])
        e = cm.exception
        self.assertEqual(e.__str__(), "could not convert string to float: 'h'")

        #test one column, not list:
        with self.assertRaises(Exception) as cm:
            self.assertEqual(df.average('a1'), 4.0)
        e = cm.exception
        self.assertEqual(e.__str__(), "a1 is not a list")

    
    #fixme: test strange cases
    def test_get_by_cond(self):
        df = DataFrame([['a1','b','c'],
                        [ 1 , 3 , 3 ],
                        [ 4 , 0 , 6 ],
                        [ 7 , 0 ,'h']])

        t = df.get_by_cond('a1', 'c', 6)
        self.assertEqual(t, 4)







