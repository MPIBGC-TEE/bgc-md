let
  pkgs = import <nixpkgs> {};
  mkDerivation = import ./autotools.nix pkgs;
in mkDerivation {
  name ="cable";
  src =./CABLE-SRC.tar.bz2;
  ctn ="CABLE-SRC";
  buildInputs = with pkgs; [ mksh gfortran netcdffortran openmpi gdb openssh];
  ncd= with pkgs; netcdffortran;
}
