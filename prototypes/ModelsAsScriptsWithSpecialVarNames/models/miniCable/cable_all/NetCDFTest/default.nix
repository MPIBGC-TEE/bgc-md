# we want to use the library as defined in our own nix expression 
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
    #  stdenv=stdenv;
    #  buildPythonPackage=python37.pkgs.buildPythonPackage;
    #  fetchPypi=python37.pkgs.fetchPypi;
    #  isPyPy=python37.pkgs.isPyPy;
    #  pytest =python37.pkgs.pytest;
    #  numpy=python37.pkgs.numpy;
    #  zlib=zlib;
    #  netcdf=netcdf-mpi; #important for parallel IO version
    #  hdf5=hdf5-mpi; # important for parallel version
    #  curl=curl;
    #  libjpeg=libjpeg;
    #  cython=python37.pkgs.cython;
    #  cftime=python37.pkgs.cftime;
    #};
  in stdenv.mkDerivation {
    name ="writeNetCDF";
    src =./writeNetCDF.tar.gz;
    buildInputs = with pkgs; [ gnumake gfortran my_netcdf_fortran openmpi gdb openssh 
   # (python37.withPackages ((ps: [ps.mpi4py ps.numpy ps.sympy ps.bootstrapped-pip ] ++ [my_netcdf4_python])))
    ];
    ncd= my_netcdf_fortran;
    exe="simple_xy_par_wr";
    preBuild=''
      makeFlagsArray+=( NCDIR="$ncd/lib$" NCMOD="$ncd/include" CFLAGS="-x f95-cpp-input" LD='-lnetcdff' LDFLAGS="-L $ncd/libs -O2" FC=mpif90)
    '';
}
