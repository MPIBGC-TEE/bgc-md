#!/bin/ksh

known_hosts()
{
   set -A kh vayu cher burn shin pear
}


## raijin.nci.org.au
host_raij()
{
   export NCDIR='/apps/netcdf/4.2.1.1/lib/'
   export NCMOD='/apps/netcdf/4.2.1.1/include/'
   export FC=mpif90
   export CFLAGS='-O2 -fp-model precise'
   export LD='-lnetcdf -lnetcdff'
   export LDFLAGS='-L/apps/netcdf/4.2.1.1/lib -L/apps/netcdf/4.2.1.1/lib/Intel -O2'
   build_build
   cd ../
   build_status
}




## shine-cl.nexus.csiro.au 
host_shin()
{
   export NCDIR='/usr/local/intel/'
   export NCMOD='/usr/local/intel/'
   export FC=ifort    ## need to check ??
#   export CFLAGS='-O2 -fp-model precise -ftz -fpe0'
   export CFLAGS='-O0 -g -debug all -traceback'
#   export CFLAGS='-O0 -g -debug all -traceback'
   export LD='-lnetcdf'
   export LDFLAGS='-L/usr/local/intel/lib -O2'
   build_build
   cd ../
   build_status
}

## pearcey.hpsc.csiro.au 
host_pear()
{
   . /apps/modules/Modules/default/init/ksh
   module add netcdf/4.3.3.1 openmpi/1.8.8-mellanox

   export NCDIR=$NETCDF_ROOT'/lib/'
   export NCMOD=$NETCDF_ROOT'/include/'
   export FC='mpif90'
   export CFLAGS='-O2 -fp-model precise '
   export LDFLAGS='-L'$NCDIR' -O2'
   export LD='-lnetcdf -lnetcdff'
   build_build
   cd ../
   build_status
}

## burnet.hpsc.csiro.au 
host_burn()
{
   . /apps/modules/Modules/default/init/ksh
   module add netcdf/3.6.3 openmpi

   export NCDIR=$NETCDF_ROOT'/lib/'
   export NCMOD=$NETCDF_ROOT'/include/'
   export FC='mpif90'
   export CFLAGS='-O2 -fp-model precise '
   export LDFLAGS='-L'$NCDIR' -O2'
   export LD='-lnetcdf -lnetcdff'
   build_build
   cd ../
   build_status
}


## cherax.hpsc.csiro.au 
host_cher()
{
   export NCDIR=$NETCDF_ROOT'/lib/'
   export NCMOD=$NETCDF_ROOT'/include/'
   export FC='mpif90'
   export CFLAGS='-O2 -fp-model precise'
   export LDFLAGS='-L'$NCDIR' -O2'
   export LD='-lnetcdf -lnetcdff'
   build_build
   cd ../
   build_status
}


## vayu.nci.org.au
host_vayu()
{
   export NCDIR=$NETCDF_ROOT'/lib/Intel'
   export NCMOD=$NETCDF_ROOT'/include/Intel'
   export FC='mpif90'
   export CFLAGS='-O2 -fp-model precise'
   if [[ $1 = 'debug' ]]; then      
      export CFLAGS='-O0 -traceback -g -fp-model precise' 
   fi
   export LDFLAGS='-L'$NCDIR' -O2'
   export LD='-lnetcdf -lnetcdff'
   build_build
   cd ../
   build_status
}



## unknown machine, user entering options stdout 
host_read()
{
   print "\n\tWhat is the root path of your NetCDF library" \
         "and .mod file. "
   print "\tRemember these have to be created by the same " \
         "Fortran compiler you" 
   print "\twant to use to build CABLE. e.g./usr/local/intel"
   read NCDF_ROOT
   
   print "\n\tWhat is the path, relative to this root, of " \
         "your NetCDF library." 
   print "\n\tPress enter for default [lib]."
   read NCDF_DIR
   if [[ $NCDF_DIR == '' ]]; then
      export NCDIR=$NCDF_ROOT/'lib'
   else   
      export NCDIR=$NCDF_ROOT/$NCDF_DIR
   fi

   
   print "\n\tWhat is the path, relative to this root, of " \
         "your NetCDF .mod file."
   print "\n\tPress enter for default [include]."
   read NCDF_MOD
   if [[ $NCDF_MOD == '' ]]; then
      export NCMOD=$NCDF_ROOT/'include'
   else   
      export NCDIR=$NCDF_ROOT/$NCDF_MOD
   fi

   export NCMOD=$NCDF_ROOT/$NCDF_MOD

   print "\n\tWhat is the Fortran compiler you wish to use."
   print "\te.g. ifort, gfortran"
   
   print "\n\tPress enter for default [ifort]."
   read FCRESPONSE 
   if [[ $FCRESPONSE == '' ]]; then
      export FC='ifort'
   else   
      export FC=$FCRESPONSE
   fi

   print "\n\tWhat are the approriate compiler options"
   print "\te.g.(ifort) -O2 -fp-model precise "
   print "\n\tPress enter for default [-O2 -fp-model precise]."
   read CFLAGRESPONSE 
   if [[ $CFLAGRESPONSE == '' ]]; then
      export CFLAGS='-O2 -fp-model precise'
   else   
      export CFLAGS=$CFLAGRESPONSE
   fi

   iflags='-L'$NCDIR' -O2'
   export LDFLAGS=$iflags

   print "\n\tWhat are the approriate libraries to link"
   print "\te.g.(most systems) -lnetcdf "
   print "\n\tPress enter for default [-lnetcdf]."
   read LDRESPONSE 
   if [[ $LDRESPONSE == '' ]]; then
      export LD='-lnetcdf'
   else   
      export LD=$LDRESPONSE
   fi


}


host_write()
{
   print '#!/bin/ksh' > junk
   print '' >> junk
   print 'known_hosts()' >> junk
   print '{' >> junk
   print '   set -A kh' ${kh[*]} $HOST_MACH >> junk
   print '}' >> junk
   print '' >> junk
   print '' >> junk
   print '## '$HOST_COMM >> junk
   print 'host_'$HOST_MACH'()' >> junk
   print '{' >> junk
   print '   export NCDIR='"'"$NCDF_ROOT'/'$NCDF_DIR"'" >> junk
   print '   export NCMOD='"'"$NCDF_ROOT'/'$NCDF_MOD"'" >> junk
   print '   export FC='$FC >> junk
   print '   export CFLAGS='"'"$CFLAGS"'" >> junk
   print '   export LD='"'"$LD"'" >> junk
   print '   export LDFLAGS='"'"$LDFLAGS"'" >> junk
   print '   build_build' >> junk
   print '   cd ../' >> junk
   print '   build_status' >> junk
   print '}' >> junk
   print '' >> junk
   print '' >> junk
}


clean_build()
{
      print '\ncleaning up\n'
      rm -fr .mpitmp
      print '\n\tPress Enter too continue buiding, Control-C to abort now.\n'
      read dummy 
}


set_up_CABLE_AUX()
{
      print "\n\tYou do not have a ~/CABLE-AUX/ directory. This directory"
      print "\tcontains configuration and data essential to using CABLE."
      print "\tNCI account holders can have this set up for you now (anywhere)."
      print "\tOthers will have to use the tarball available for download at ..."
      print "\n\tDo you want to run set up this directory now? y/[n]"
      
      read setup_CABLE_AUX
      if [[ $setup_CABLE_AUX = 'y' ]]; then
         print "\n\tPlease enter your NCI user ID"
         read NCI_USERID 
         mkdir ~/CABLE-AUX 
         
         fscp1="scp -r "
         fscp2="@vayu.nci.org.au:/projects/access/CABLE-AUX/"
         fscp3="offline "
         fscp4=$HOME"/CABLE-AUX/"
         fscp5=$fscp1$NCI_USERID$fscp2
         fscp=$fscp5$fscp3$fscp4$fscp3
         $fscp
          
         RC=$?
         if [[ $RC > 0 ]];then 
            print "ERROR: scp of ~/CABLE-AUX/offline failed" 
            exit $RC 
         fi
         
         fscp3="core "
         fscp=$fscp5$fscp3$fscp4$fscp3
         $fscp
         
         RC=$?
         if [[ $RC > 0 ]];then 
            print "ERROR: scp of ~/CABLE-AUX/core failed" 
            exit $RC 
         fi
      fi        
}



not_recognized()
{  
   print "\n\n\tThis is not a recognized host for which we " \
         "know the location of the" 
   print "\tnetcdf distribution and correct compiler switches."

   print "\n\tPlease enter these details as prompted, and the " \
         "script will be " 
   print "\tupdated accordingly. " 
   print "\n\tIf this is a common machine for CABLE users, " \
         "please email"
   print "\n\t\t cable_help@nf.nci.org.au "  
   print "\n\talong with your new build_mpi.ksh so that we can " \
         "update the script "
   print "\tfor all users. "
   print "\n\tTo enter compile options for this build press " \
         "enter, otherwise " 
   print "\tControl-C to abort script."           
   
   host_read

   print "\n\tPlease supply a comment include the new build " \
         "script." 
   print "\n\tGenerally the host URL e.g. vayu.nci.org.au "
   read HOST_COMM
   
   build_build
}


do_i_no_u()
{
   integer kmax=${#kh[*]}
   integer k=0
   typeset -f subr
   
   while [[ $k -lt $kmax ]]; do
      if [[ $HOST_MACH = ${kh[$k]} ]];then
         print 'Host recognized'
         subr=host_${kh[$k]}
         $subr $1
      fi        
      (( k = k + 1 ))
   done 
}


build_status()
{
   if [[ -f .mpitmp/cable-mpi ]]; then
   	mv .mpitmp/cable-mpi .
   	print '\nBUILD OK\n'
   else
      print '\nOooops. Something went wrong\n'        
      print '\nKnow build issues:\n'        
      print '\nSome systems require additional library. \n'        
      print '\nEdit Makefile_offline; add -lnetcdff to LD = ...\n'        
   fi
   exit
}


      
i_do_now()
{
      cd ../
      host_write
      tail -n +7 build_mpi.ksh > build_mpi.ksh.tmp
      cat junk build_mpi.ksh.tmp > build_mpi.ksh.new
      mv build_mpi.ksh.new build_mpi.ksh
      chmod u+x build_mpi.ksh 
      rm -f build_mpi.ksh.tmp build_mpi.ksh.new junk 
      build_status
}


build_build()
{
   if [[ ! -d .mpitmp ]]; then
      mkdir .mpitmp
   fi
   
   if [[ -f cable-mpi ]]; then
      print '\ncable-mpi executable exists. copying to cable-mpi.bu\n' 
      mv cable-mpi cable-mpi.bu
   fi
   
   CORE="../core/biogeophys"
   DRV="."
   CASA="../core/biogeochem"
   
   /bin/cp -p $CORE/*90 ./.mpitmp
   /bin/cp -p $DRV/*90 ./.mpitmp
   /bin/cp -p $CASA/*90 ./.mpitmp
   
   print "\n\n\tPlease note: CASA-CNP files are included in build only for " 
   print "\ttechnical reasons. Implementation is not officially available with" 
   print "\tthe release of CABLE 2.0\n"
    
   /bin/cp -p Makefile_mpi  ./.mpitmp
   
  cd .mpitmp/

   make -f Makefile_mpi
}

###########################################
## build.ksh - MAIN SCRIPT STARTS HERE   ##
###########################################

if [[ $1 = 'clean' ]]; then
   clean_build
fi

if [[ ! -d ~/CABLE-AUX ]];then
   set_up_CABLE_AUX
else
   print "\n~/CABLE-AUX is at least present.\n"
fi


   
known_hosts

HOST_MACH=`uname -n | cut -c 1-4`

do_i_no_u $1

not_recognized

i_do_now

