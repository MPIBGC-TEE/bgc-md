let
  pkgs = import <nixpkgs> {};
  mkDerivation = import ./autotools.nix pkgs;
in mkDerivation {
  name ="writeNetCDF";
  #src =.src.tar.bz;
  ctn ="src";
  buildInputs = with pkgs; 
  #[ gfortran openmpi openssh 
  (python37.withPackages (ps: [ps.mpi4py ps.numpy ps.sympy ps.bootstrapped-pip])).env;
  #];
  exe="parallel_write_test";
}
