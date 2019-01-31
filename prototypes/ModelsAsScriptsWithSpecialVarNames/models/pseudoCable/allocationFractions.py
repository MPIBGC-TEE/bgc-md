def allocationFractions(
        leaf
        ,wood
        ,fine_root
        ,r_leaf
        ,r_wood
        ,r_fine_root
        ,Npp
        ,phase
        ,glaimax
        ,b_leaf
        ,b_fine_root
        ,b_wood
        ,sla
        ,planttype
    ):
    #print(
    #    "leaf=",leaf
    #    ,"wood=",wood
    #    ,"fine_root=",fine_root
    #    ,"r_leaf=",r_leaf
    #    ,"r_wood=",r_wood
    #    ,"r_fine_root=",r_fine_root
    #    ,"Npp=",Npp
    #    ,"phase=",phase
    #    ,"glaimax=",glaimax
    #    ,"b_leaf=",b_leaf
    #    ,"b_fine_root=",b_fine_root
    #    ,"b_wood=",b_wood
    #    ,"sla=",sla
    #    ,"planttype=",planttype
    #)
    (bvec_leaf,bvec_wood,bvec_fine_root)=(None,None,None)
    #l=["phase","Npp","leaf","sla","glaimax","planttype","leaf","wood","fine_root","r_leaf","r_wood","r_fine_root"]
    #for var in l:
    #    print(var+"=",eval(var))

    if (phase==2)  and  (Npp>=0)  and (leaf*sla<glaimax):
        (bvec_leaf,bvec_wood,bvec_fine_root)=(b_leaf,b_wood,b_fine_root) 
    elif ((phase ==0) or (leaf*sla>=glaimax)) and (Npp>=0): 
        (bvec_leaf,bvec_wood,bvec_fine_root)=(0,b_wood/(b_fine_root +b_wood),b_fine_root/(b_fine_root+b_wood)) 

    elif (phase==1) and (Npp >=0) and (leaf*sla < glaimax) and (planttype==1):
        (bvec_leaf,bvec_wood,bvec_fine_root)=(0.8,0,0.2)
    
    elif (phase==1) and (Npp >=0) and (leaf*sla < glaimax) and (planttype==0):
        (bvec_leaf,bvec_wood,bvec_fine_root)=(0.8,0.1,0.1)
    
    elif (phase==3) and (Npp >=0) and (leaf*sla < glaimax): 
        (bvec_leaf,bvec_wood,bvec_fine_root)=(0,b_wood,1-b_wood)

    elif (Npp < 0) and (leaf+wood+fine_root >0): 
        (bvec_leaf,bvec_wood,bvec_fine_root)=(
                leaf/(leaf+wood+fine_root),wood/(leaf+wood+fine_root),fine_root/(leaf+wood+fine_root))

    elif (Npp<0) and (leaf+wood+fine_root <=0):     
        (
                bvec_leaf
                ,bvec_wood
                ,bvec_fine_root
        )=(
                r_leaf/(r_leaf+r_wood+r_fine_root)
                ,r_wood/(r_leaf+r_wood+r_fine_root)
                ,r_fine_root/(r_leaf+r_wood+r_fine_root)
        )
    
    if bvec_leaf is None:
        raise Exception("bvec_leaf should not be None")
    return (bvec_leaf,bvec_wood,bvec_fine_root)

def bvec_leaf_num( leaf ,wood ,fine_root ,r_leaf ,r_wood ,r_fine_root ,Npp ,phase ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype):
    return allocationFractions(leaf ,wood ,fine_root ,r_leaf ,r_wood ,r_fine_root ,Npp ,phase ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)[0]

def bvec_wood_num( leaf ,wood ,fine_root ,r_leaf ,r_wood ,r_fine_root ,Npp ,phase ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype):
    return allocationFractions(leaf ,wood ,fine_root ,r_leaf ,r_wood ,r_fine_root ,Npp ,phase ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)[1]

def bvec_fine_root_num( leaf ,wood ,fine_root ,r_leaf ,r_wood ,r_fine_root ,Npp ,phase ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype):
    return allocationFractions(leaf ,wood ,fine_root ,r_leaf ,r_wood ,r_fine_root ,Npp ,phase ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)[2]

