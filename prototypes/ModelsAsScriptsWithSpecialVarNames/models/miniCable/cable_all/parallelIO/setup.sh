# This script is called by nix
# and sets up the evironment
unset PATH
for p in $baseInputs $buildInputs; do
  if [ -d $p/bin ]; then
    export PATH="$p/bin${PATH:+:}$PATH"
  fi
done
# define some functions 
#function unpackPhase(){
#	tar xfj $src
#}
function buildParallel(){
	echo "########################\n \
  build parallel executable \n \
  #################################\n\n"
  export FC=mpif90
  export CFLAGS='-x f95-cpp-input'
	echo $ctn
	cd "${ctn}"
  make -f Makefile
}

function genericBuild(){
	unpackPhase
	buildParallel
  # no installation since we only use the shell
}
