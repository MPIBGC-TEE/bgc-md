# script will will create soft links to rcp nedpo secenarios 
# cable will access ndepo data in /hist folder with soft linked rcp ndepo data after 1999

startyr=2000
endyr=2100
yr=$startyr

while [ $yr -le $endyr ]
do

ln -fs ../rcp85/ndep_${yr}_1.9x2.5_KF.nc ./

yr=`expr $yr + 1`

done

