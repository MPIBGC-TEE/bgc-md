let
  pkgs = import <nixpkgs> {};
  mkDerivation = import ../autotools.nix pkgs;
in mkDerivation {
  name ="cable";
  src =./CABLE-AUX-2.3.4_nix.tar.bz2
  buildInputs = with pkgs; [ cable ];
}
