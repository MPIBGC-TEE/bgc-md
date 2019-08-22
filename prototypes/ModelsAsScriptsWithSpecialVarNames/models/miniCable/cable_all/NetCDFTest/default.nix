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
  in stdenv.mkDerivation {
    name ="writeNetCDF";
    src =./writeNetCDF.tar.gz;
    buildInputs = with pkgs; [ gnumake gfortran my_netcdf_fortran openmpi gdb openssh];
    ncd= my_netcdf_fortran;
    exe="simple_xy_par_wr";
    preBuild=''
      makeFlagsArray+=( NCDIR="$ncd/lib$" NCMOD="$ncd/include" CFLAGS="-x f95-cpp-input" LD='-lnetcdff' LDFLAGS="-L $ncd/libs -O2" FC=mpif90)
    '';
}
