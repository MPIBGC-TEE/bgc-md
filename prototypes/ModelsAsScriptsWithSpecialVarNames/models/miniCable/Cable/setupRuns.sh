# This script is called by nix
# and sets up the evironment
unset PATH
for p in $baseInputs $buildInputs; do
  if [ -d $p/bin ]; then
    export PATH="$p/bin${PATH:+:}$PATH"
  fi
done

# define some functions 
function unpackPhase(){
	tar xfj $src
}
function runPhase(){
  mkdir -p runs
  c
}
