let
  pkgs = import <nixpkgs> {};
  mkDerivation = import ./autotools.nix pkgs;
in mkDerivation {
  name ="writeNetCDF";
  buildInputs = with pkgs;
  [(python37.withPackages (ps: [ps.mpi4py ps.numpy ps.sympy ps.bootstrapped-pip]))
  gfortran openmpi gdb openssh ];
  exe="parallel_write_test";
}
