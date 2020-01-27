with import <nixpkgs> {};
  let 
    my_netcdf_fortran=import <nixpkgs/pkgs/development/libraries/netcdf-fortran/default.nix> {      
      stdenv=stdenv;
      fetchurl=fetchurl;
      netcdf=netcdf-mpi;
      hdf5=hdf5-mpi;
      curl=curl;
      gfortran =gfortran;
    };
    #my_netcdf4_python=import <nixpkgs/pkgs/development/python-modules/netcdf4/default.nix> {      
    my_netcdf4_python=import ../my_netcdf4_python/default.nix{
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
    mkDerivation = import ./autotools.nix pkgs;
  in mkDerivation {
    name ="cable";
    #src =./CABLE-SRC.tar.bz2;
    ctn ="CABLE-SRC";
    buildInputs = with pkgs; [ 
      gnumake 
      gfortran #cable
      my_netcdf_fortran 
      netcdf-mpi 
      openmpi 
      gdb 
      openssh 
      nodejs #necessary for jupyter lab vi extension 
      (python37.withPackages ((ps: [
        ps.mpi4py 
        ps.numpy 
        ps.sympy 
        ps.bootstrapped-pip 
        ps.jupyterlab
        ps.ipyparallel # mecessarry
        #ps.netcdf4
      ] 
      ++ [my_netcdf4_python]
      )))
    ];
    ncd= with pkgs; my_netcdf_fortran;
}

# jupyter serverextension enable --py ipyparallel 
