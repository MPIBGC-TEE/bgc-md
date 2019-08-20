let
  pkgs = import <nixpkgs> {};
  mkDerivation = import ./autotools.nix pkgs;
in mkDerivation {
  name ="writeNetCDF";
  #src =.src.tar.bz;
  ctn ="src";
  buildInputs = with pkgs; [ mksh gfortran hdf5-fortran hdf5-mpi netcdffortran openmpi gdb openssh];
  ncd= with pkgs; netcdffortran;
  exe="simple_xy_par_wr";
}
