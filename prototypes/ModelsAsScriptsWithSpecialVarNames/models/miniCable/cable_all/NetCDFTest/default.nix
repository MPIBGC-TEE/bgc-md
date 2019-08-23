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
    };
  in stdenv.mkDerivation {
    name ="writeNetCDF";
    src =./writeNetCDF.tar.gz;
    buildInputs = with pkgs; [ gnumake gfortran my_netcdf_fortran netcdf-mpi openmpi gdb openssh 
    (python37.withPackages ((ps: [
        ps.mpi4py 
        ps.numpy 
        ps.sympy 
        ps.bootstrapped-pip 
        #ps.netcdf4
      ] 
    ++ [my_netcdf4_python]
    )))
    ];
    ncf= my_netcdf_fortran;
    ncc= netcdf-mpi;
    exe="simple_xy_par_wr";
    preBuild=''
      makeFlagsArray+=( NCDIR="$ncf/lib$" NCMOD="$ncf/include" CFLAGS="-x f95-cpp-input" LD='-lnetcdff' LDFLAGS="-L $ncf/libs -O2" FC=mpif90)
    '';
}
