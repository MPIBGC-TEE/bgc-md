with import <nixpkgs> {};
let 
  argset={
    stdenv=stdenv;
    buildPythonPackage=python37.pkgs.buildPythonPackage;
    fetchPypi=python37.pkgs.fetchPypi;
    isPyPy=python37.pkgs.isPyPy;
    pytest =python37.pkgs.pytest;
    numpy=python37.pkgs.numpy;
    zlib=zlib;
    netcdf=netcdf-mpi; #important for parallel IO version
    hdf5=hdf5-mpi; # important for parallel version
    curl=curl;
    libjpeg=libjpeg;
    cython=python37.pkgs.cython;
    cftime=python37.pkgs.cftime;
    mpi4py=python37.pkgs.mpi4py;
    openssh=openssh;
  };  
in 
  import ./default.nix argset
