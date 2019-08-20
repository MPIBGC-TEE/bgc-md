# This script is called by nix
# and sets up the evironment
unset PATH
for p in $baseInputs $buildInputs; do
  if [ -d $p/bin ]; then
    export PATH="$p/bin${PATH:+:}$PATH"
  fi
	#  if [ -d $p/include ]; then
	#    export NIX_CFLAGS_COMPILE="-I $p/include${NIX_CFLAGS_COMPILE:+ }$NIX_CFLAGS_COMPILE"
	#  fi
	#  if [ -d $p/lib ]; then
	#    export NIX_LDFLAGS="-rpath $p/lib -L $p/lib${NIX_LDFLAGS:+ }$NIX_LDFLAGS"
	#  fi
done
# we export some environmentvariables needed by our version "build_nix.ksh"# of build.ksh  
# we could also change the makefile to directly incorporate them
export NCDIR="$ncd/lib${NCDIR:+ }$NCDIR"
export NCMOD="$ncd/include${NCMOD:+ }$NCMOD"

# define some functions 
#function unpackPhase(){
#	tar xfj $src
#}
function prepareBuild(){
  #export CFLAGS='-g -O0 -x f95-cpp-input -Wall'
  export CFLAGS='-x f95-cpp-input'
  export LD='-lnetcdff'
  export LDFLAGS="-L ${NCDIR} -O2"
	echo $ctn
	cd "${ctn}"
}
function buildSerial(){
	echo "########################\n \
    build serial executable \n \
    #################################\n\n"
  prepareBuild
  export FC=gfortran
  make -f Makefile
}
function buildParallel(){
	echo "########################\n \
  build parallel executable \n \
  #################################\n\n"
  prepareBuild
  export FC=mpif90
  make -f Makefile
}

function genericBuild(){
	unpackPhase
	buildSerial
  cd ../../../
	buildParallel
}
