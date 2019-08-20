let
  pkgs = import <nixpkgs> {};
  mkDerivation = import ./autotools.nix pkgs;
in mkDerivation {
  name ="cable";
  src =./CABLE2.0_mpi_yp1220.tar.bz2;
  ctn ="CABLE2.0_mpi_yp1220";
  buildInputs = with pkgs; [ mksh gfortran netcdffortran openmpi gdb openssh];
  ncd= with pkgs; netcdffortran;
}
