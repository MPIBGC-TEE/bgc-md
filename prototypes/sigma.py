from unittest import TestCase
def remove(mylist,i):
    left =mylist[:i]
    right=mylist[(i+1):]
    rest=left+right
    #print('left',left)
    #print('right',right)
    #print('rest',rest)
    return(rest)

def sigma_alg(myset):
    l=len(myset)
    mylist=list(myset)
    if l==0:
        return []
    if l==1:
        return frozenset([myset]) # a set of one set...
    if l>1:
        # extract all two element lists
        result=set()
        for i in range(l):
            rest=frozenset(remove(mylist,i))
            sub_set=sigma_alg(rest)
            print('sub_set',sub_set)
            for s in sub_set:
                result.add(s)
        result.add(myset)   
        return frozenset(result)

    # a fucntion to compute the sigma algebra of a set represented by a list 
    # (The list of all sublist of mylist)
    

#test it
class SigmaTest(TestCase):
    def test_sigma_alg(self):
        res=sigma_alg(frozenset([1]))
        ref=frozenset([ frozenset([1])]) # a set of sets..
        self.assertEqual(res,ref)

        res=sigma_alg(frozenset([1,2]))
        ref=frozenset(
            [
                frozenset([1]),
                frozenset([2]),
                frozenset([1,2])
            ]
        )
        self.assertEqual(res,ref)
        ## 

        res=sigma_alg(frozenset([1,2,3]))
        ref=frozenset(
            [
                frozenset([1]),
                frozenset([2]),
                frozenset([3]),
                frozenset([1,2]),
                frozenset([1,3]),
                frozenset([2,3]),
                frozenset([1,2,3])
            ]
        )
        self.assertEqual(res,ref)
        
        res=sigma_alg(frozenset([1,2,3,4]))
        ref=frozenset(
            [
                frozenset([1]),
                frozenset([2]),
                frozenset([3]),
                frozenset([4]),
                frozenset([1,2]),
                frozenset([1,3]),
                frozenset([1,4]),
                frozenset([2,3]),
                frozenset([2,4]),
                frozenset([3,4]),
                frozenset([2,3,4]),
                frozenset([1,3,4]),
                frozenset([1,2,4]),
                frozenset([1,2,3]),
                frozenset([1,2,3,4])
            ]
        )
        self.assertEqual(res,ref)
