#!/bin/ksh

known_hosts()
{
   set -A kh vayu cher burn shin jigg
}


## jiggle
host_jigg()
{
   export NCDIR='/usr/local/lib'
   export NCMOD='/usr/local/include'
   export FC=gfortran
   export CFLAGS='-O0 -x f95-cpp-input'
   export LD='-lnetcdf -lnetcdff'
   export LDFLAGS='-L/usr/local/lib -O2'
   build_build
   cd ../
   build_status
}




## shine-cl.nexus.csiro.au 
host_shin()
{
   export NCDIR='/usr/local/intel/lib'
   export NCMOD='/usr/local/intel/include'
   export FC=ifort
   export CFLAGS='-O2 -fp-model precise -ftz -fpe0'
   export LD='-lnetcdf'
   export LDFLAGS='-L/usr/local/intel/lib -O2'
   build_build
   cd ../
   build_status
}


## burnet.hpsc.csiro.au 
host_burn()
{
   export NCDIR=$NETCDF_ROOT'/lib/'
   export NCMOD=$NETCDF_ROOT'/include/'
   export FC=$F90
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
   export FC=$F90
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
   export FC=$F90
   export CFLAGS='-O2 -fp-model precise'
   if [[ $1 = 'debug' ]]; then      
      export CFLAGS='-O0 -traceback -g -fp-model precise -ftz -fpe0' 
   fi
   export LDFLAGS='-L'$NCDIR' -O2'
   export LD='-lnetcdf'
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
      export NCMOD=$NCDF_ROOT/$NCDF_MOD
   fi

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
   print '   export NCDIR='"'"$NCDIR"'" >> junk
   print '   export NCMOD='"'"$NCMOD"'" >> junk
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
      rm -fr .tmp
      print '\n\tPress Enter too continue buiding, Control-C to abort now.\n'
      read dummy 
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
   print "\n\talong with your new build.ksh so that we can " \
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
   if [[ -f .tmp/cable ]]; then
   	mv .tmp/cable .
   	print '\nBUILD OK\n'
   else
      print '\nOooops. Something went wrong\n'        
      print '\nKnown build issues:\n'        
      print '\nSome systems require additional library. \n'        
      print '\nEdit Makefile_offline; add -lnetcdff to LD = ...\n'        
   fi
   exit
}


      
i_do_now()
{
      cd ../
      host_write
      tail -n +7 build.ksh > build.ksh.tmp
      cat junk build.ksh.tmp > build.ksh.new
      mv build.ksh.new build.ksh
      chmod u+x build.ksh 
      rm -f build.ksh.tmp build.ksh.new junk 
      build_status
}


build_build()
{
   if [[ ! -d .tmp ]]; then
      mkdir .tmp
   fi
   
   if [[ -f cable ]]; then
      print '\ncable executable exists. copying to cable.bu\n' 
      mv cable cable.bu
   fi
   
   UTIL="../core/utils"
   CORE="../core/biogeophys"
   DRV="."
   CASA="../core/biogeochem"
   
   /bin/cp -p $UTIL/*90 ./.tmp
   /bin/cp -p $CORE/*90 ./.tmp
   /bin/cp -p $DRV/*90 ./.tmp
   /bin/cp -p $CASA/*90 ./.tmp
   
   print "\n\n\tPlease note: CASA-CNP files are included in build only for " 
   print "\ttechnical reasons. Implementation is not officially available with" 
   print "\tthe release of CABLE 2.0\n"
    
   /bin/cp -p Makefile_offline  ./.tmp
   
  cd .tmp/
   
   make -f Makefile_offline
}

###########################################
## build.ksh - MAIN SCRIPT STARTS HERE   ##
###########################################

if [[ $1 = 'clean' ]]; then
   clean_build
fi

   
known_hosts

HOST_MACH=`uname -n | cut -c 1-4`

do_i_no_u $1

not_recognized

i_do_now

