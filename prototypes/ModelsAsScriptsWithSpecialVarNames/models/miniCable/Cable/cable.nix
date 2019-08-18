let
  pkgs = import <nixpkgs> {};
  mkDerivation = import ./autotools.nix pkgs;
in mkDerivation {
  name ="cable";
  src =./cable2.0-trunk.tar.bz;
  ctn ="cable2.0-trunk";
  buildInputs = with pkgs; [ mksh gfortran netcdffortran openmpi gdb openssh];
  ncd= with pkgs; netcdffortran;
}
