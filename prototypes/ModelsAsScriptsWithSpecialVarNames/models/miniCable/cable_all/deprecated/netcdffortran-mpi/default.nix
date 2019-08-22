{ stdenv, fetchurl, netcdf, hdf5, curl, gfortran }:
let 
  mpiSupport = hdf5.mpiSupport;
  mpi=hdf5.mpi;
in
  stdenv.mkDerivation rec {
    name = "netcdf-fortran-${version}";
    version = "4.4.5";
  
    src = fetchurl {
      url = "https://github.com/Unidata/netcdf-fortran/archive/v${version}.tar.gz";
      sha256 = "00qwg4v250yg8kxp68srrnvfbfim241fnlm071p9ila2mihk8r01";
    };
  
    buildInputs = [ netcdf hdf5 mpi curl gfortran ];
    doCheck = true;
    
    passthru = {
    mpiSupport = mpiSupport;
    inherit mpi;

    configureFlags =(stdenv.lib.optionals mpiSupport [ "--enable-parallel-tests" "FC=${mpi}/bin/mpif90"]);
  };
  
    #meta = with stdenv.lib; {
    #  description = "Fortran API to manipulate netcdf files";
    #  homepage = https://www.unidata.ucar.edu/software/netcdf/;
    #  license = licenses.free;
    #  maintainers = [ maintainers.bzizou ];
    #  platforms = platforms.unix;
    #};
  }
