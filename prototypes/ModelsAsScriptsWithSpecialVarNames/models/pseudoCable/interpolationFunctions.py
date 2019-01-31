import csv
from scipy.interpolate import interp1d
from pathlib import Path
#def shiftedTimeLine(p:Path):#uses space 
#    with open (p) as csvfile:
#        r=csv.reader(csvfile,delimiter=' ')
#        values=[ row[-1] for row in r]
#    n=len(values)
#    times=range(n)    
#    f=interp1d(x=times,y=values)
#    return f

def timeLine2(p:Path): #uses comma
    with open (p) as csvfile:
        r=csv.reader(csvfile,delimiter=',')
        values=[ row[-1] for row in r]
    n=len(values)
    times=range(n) #-0.5    
    f=interp1d(x=times,y=values)
    return f
#f=timeLine(Path('Tumbarumba/T_dependent/b_tran.txt'))
#import matplotlib.pyplot  as plt
#fig=plt.figure(figsize=(7,7))
#ax1=fig.add_subplot(1,1,1)
#times=f.x
#ax1.plot(times,f(times))
#fig.savefig("b_trans.pdf")
