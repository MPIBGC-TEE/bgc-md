pkgs: attrs:
  with pkgs;
  let defaultAttrs = {
    builder = "${bash}/bin/bash";
    args= [ ./builder.sh ];
    setup = ./setup.sh;
    baseInputs= [ gnutar gzip bzip2 gnumake gcc binutils-unwrapped coreutils gawk gnused gnugrep patchelf findutils which ];
    buildInputs= [];
    system =builtins.currentSystem;
  };
  in
  derivation (defaultAttrs // attrs)
