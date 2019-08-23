#!/bin/ksh

known_hosts()
{
   set -A kh raij
}
## raijin.nci.org.au
host_raij()
{
   NCDF_ROOT=/apps/netcdf/4.2.1.1
   export NCDIR=$NCDF_ROOT'/lib/Intel'
   export NCMOD=$NCDF_ROOT'/include/Intel'
   export FC=ifort
   export CFLAGS='-O2 -g -i8 -r8 -traceback -fp-model precise -ftz -fpe0'  
   export CINC='-I$(NCMOD)'
   if [[ $1 = 'debug' ]]; then      
      export CFLAGS='-O0 -traceback -g -i8 -r8 -fp-model precise -ftz -fpe0'
   fi
   build_build
   cd ../
   build_status
}


## unknown machine, user entering options stdout 
host_read()
{
   print "\n\tWhat is the ROOT path of your NetCDF library" \
         "and .mod file. "
   print "\tRemember these have to be created by the same " \
         "Fortran compiler you" 
   print "\twant to use to build CABLE. e.g./usr/local/intel"
   read NCDF_ROOT
   
   print "\n\tWhat is the path, relative to the above ROOT, of " \
         "your NetCDF library." 
   print "\te.g. lib"
   read NCDF_DIR
   export NCDIR=$NCDF_ROOT/$NCDF_DIR
   
   print "\n\tWhat is the path, relative to the above ROOT, of " \
         "your NetCDF .mod file."
   print "\te.g. include"
   read NCDF_MOD
   export NCMOD=$NCDF_ROOT/$NCDF_MOD

   print "\n\tWhat is the Fortran compiler you wish to use."
   print "\te.g. ifort, gfortran"
   read FC 
   export FC

   print "\n\tWhat are the approriate compiler options"
   print "\te.g.(ifort) -O2 -fp-model precise "
   read CFLAGS 
   export CFLAGS
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
   print '   export NCDIR='$NCDF_ROOT'/'$NCDF_DIR >> junk
   print '   export NCMOD='$NCDF_ROOT'/'$NCDF_MOD >> junk
   print '   export FC='$FC >> junk
   print '   export CFLAGS='$CFLAGS >> junk
   print '   build_build' >> junk
   print '   cd ../' >> junk
   print '   build_status' >> junk
   print '}' >> junk
   print '' >> junk
   print '' >> junk
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
   print "\n\t\t cable_help@nci.org.au "  
   print "\n\talong with your new build.ksh so that we can " \
         "update the script "
   print "\tfor all users. "
   print "\n\tTo enter compile options for this build press " \
         "enter, otherwise " 
   print "\tControl-C to abort script."           
   
   host_read

   print "\n\tPlease supply a comment include the new build " \
         "script." 
   print "\n\tGenerally the host URL e.g. raijin.nci.org.au "
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
   
   # write file for consumption by Fortran code
   # get SVN revision number 
   CABLE_REV=`svn info | grep Revis |cut -c 11-18`

   if [[ $CABLE_REV == "" ]]; then
      echo "this is not an svn checkout"
      CABLE_REV=0
      echo "setting CABLE revision number to " $CABLE_REV 
   fi         
   print $CABLE_REV > ~/.cable_rev
   # get SVN status 
   CABLE_STAT=`svn status`
   print $CABLE_STAT >> ~/.cable_rev

   if [[ ! -d .tmp ]]; then
      mkdir .tmp
   fi

   if [[ ! -d $libroot ]]; then
      print '\n\tCABLE Library path '$libroot' does not exist. I could fix this' 
      print '\tfor you but it suggests to me that you are not as ready as you'
      print '\tthought. Aborting now.\n' 
      exit
   fi
   
   if [[ -f $libpath ]]; then
      print '\n\tCABLE library exists at\n' 
      print $libpath 
      print '\nCopying to\n'
      libpathbu=$libpath'.'`date +%d.%m.%y`
      print $libpathbu'\n' 
      mv $libpath $libpathbu
   fi
  
   CORE="../core/biogeophys"
   DRV="."
   CASA="../core/biogeochem"
   OFL="../offline"
   
   /bin/cp -p $CORE/*90 ./.tmp
   /bin/cp -p $DRV/*90 ./.tmp
   /bin/cp -p $CASA/*90 ./.tmp
   /bin/cp -p $OFL/*90 ./.tmp
   
   print "\n\n\tPlease note: CASA-CNP files are included in build only for " 
   print "\ttechnical reasons. Implementation is not officially available with" 
   print "\tthe release of CABLE 2.0\n"
    
   /bin/cp -p Makefile_CABLE-UM ./.tmp
   
   cd .tmp/
   
   make -f Makefile_CABLE-UM

   if [[ -f cable_explicit_driver.o ]]; then
      print '\nCompile appears successful. Now build library\n'
   else
      print'\nCompile failed\n'
      exit
   fi
   
   ## make library from CABLE object files
   /usr/bin/ar r libcable.a cable_explicit_driver.o cable_implicit_driver.o   \
      cable_rad_driver.o cable_hyd_driver.o cable_common.o  \
      cable_define_types.o cable_data.o cable_diag.o \
      cable_soilsnow.o cable_air.o cable_albedo.o cable_radiation.o  \
      cable_roughness.o cable_carbon.o cable_canopy.o cable_cbm.o    \
      cable_um_tech.o cable_um_init_subrs.o cable_um_init.o \
      casa_variable.o casa_cable.o casa_cnp.o casa_inout.o \
      casa_types.o casa_um_inout.o cable_iovars.o \
      cable_sli_main.o cable_sli_utils.o cable_sli_numbers.o \
      cable_sli_roots.o cable_sli_solve.o POP.o cable_phenology.o cable_climate.o


   if [[ -f libcable.a ]]; then
      print '\nLibrary build successful. Copying libcable.a to ' $libroot
   else
      print '\nBuild failed\n'
      exit
   fi
   
   if [[ -h $libpath ]]; then
      print "\nThis library already exists in some form. Most likely it is the"
      print "\tdefault linked library. If you wish to overwrite this library"
      print "\tthen press Enter to proceeed. Otherwise Control-C to abort. \n"
      read dummy
      mv $libpath $libroot/original_link 
      rm -f $libpath
   fi
   
   /bin/cp -p libcable.a $libroot 
   
   if [[ -f $libpath ]]; then
      print "\nYour timestamped library should be this one:\n"
      echo `ls -alt $libpath`
      print '\nDONE\n'
      exit
   else
      print '\nSomething went wrong!\n'
      exit
   fi

}


###########################################
## build.ksh - MAIN SCRIPT STARTS HERE   ##
###########################################

if [[ $1 = 'clean' ]]; then
   print '\ncleaning up\n'
   rm -fr .tmp
   print '\n\tPress Enter too continue buiding, Control-C to abort now.\n'
   read dummy 
fi
   
export libroot=$CABLE_AUX'/CABLE-AUX/UM'
export libpath=$libroot'/libcable.a'

known_hosts

HOST_MACH=`uname -n | cut -c 1-4`

do_i_no_u $1

not_recognized

