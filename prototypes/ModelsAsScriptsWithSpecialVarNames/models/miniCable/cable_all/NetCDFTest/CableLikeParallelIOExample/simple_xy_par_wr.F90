!     http://www.unidata.ucar.edu/software/netcdf/docs/netcdf-tutorial
module constants
  real(kind=8), parameter    :: pi = 3.1415927                
end module

program simple_xy_par_wr

  use netcdf
  use mpi
  use constants

  implicit none
 
  INTEGER :: ierr,wnp,rank,nproc
  integer :: my_worker_rank, ierr,world_group_id,worker_group_id,worker_comm_id,wnptest
  character (len = *), parameter :: FILE_NAME = "simple_xy_par.nc"
  ! We assume the points to be threaded on a single string
  ! We are writing a temperature timeline 1D
  ! for every point. So the dimension for the temperature data is 2
  integer,      parameter :: NDIMS_data = 3 ,NDIMS_temperature= 2 ,t_dim=48

  integer                 ::i, j,k,l

  ! When we create netCDF files, variables and dimensions, we get back
  ! an ID for each one.
  integer :: ncid, varid_data, varid_temperature&
            ,dimids_data(NDIMS_data) ,dimids_temperature(NDIMS_temperature)&
            ,x_dimid_data, y_dimid_data, temp_dimid_data &
            ,lp_dimid_temp, time_dimid_temp&
            ,my_lp_index_offset ,my_lp_number&
            ,my_patch_ind_offset ,my_patch_number&
            
  ! add chunk size for unlimited variables
  integer :: chunk_size_data(NDIMS_data),chunk_size_temperature(NDIMS_temperature)

  ! These will tell where in the data file this processor should write.
  integer :: start_data(NDIMS_data), count_data(NDIMS_data)
  integer :: start_temperature(NDIMS_temperature), count_temperature(NDIMS_temperature)
  
  ! This is the data array we will write. It will just be filled with
  ! the rank of this processor.
  integer, allocatable :: data_out(:)
  real, allocatable :: temp_out(:,:)
  
  real(kind=8), parameter                       :: min_x=0,max_x=1,span_x=max_x-min_x
  real(kind=8)                                  :: d_t,d_x ,my_offset ,patch_extend

  real(kind=8)             , dimension(t_dim)   :: time
  real(kind=8), allocatable, dimension(:)       :: my_xs
  real(kind=8), allocatable, dimension(:,:)     :: my_temperatures


  ! Initialize MPI, learn local rank and total number of processors.
  call MPI_Init(ierr)
  call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
  call MPI_Comm_size(MPI_COMM_WORLD, nproc, ierr)
  call MPI_Comm_group ( MPI_COMM_WORLD, world_group_id, ierr )
  wnp=nproc-1
  allocate ( worker_ranks(1:wnp)) 
  do i = 1, wnp ! we start with 1 since the master will be excluded 
    worker_ranks(i) = i
  end do
  if (rank ==1) print *,'worker_ranks: ',worker_ranks
  call MPI_Comm_group ( MPI_COMM_WORLD, world_group_id, ierr ) !world group is now the group of all processes in MPI_COMM_WORLD
  call MPI_Group_incl ( world_group_id, wnp,worker_ranks, worker_group_id, ierr )
  call MPI_Comm_create ( MPI_COMM_WORLD, worker_group_id, worker_comm_id, ierr ) 
  if (my_rank>0) then
    call MPI_Comm_rank(worker_comm_id, my_worker_rank, ierr)
    call MPI_Comm_size(worker_comm_id, wnptest, ierr)
    if (my_rank ==1)print *,'wnptest: ',wnptest
    ! Create some pretend data. We just need one row.
    allocate(data_out(wnp), stat = stat)
    if (stat .ne. 0) stop 3
    do x = 1, wnp
       data_out(x) = my_worker_rank
    end do

    ! Create some pretend data. 
    ! We build a 1D array of patches and timeline for every patch
    ! In cable the number of patches per landpoint is send to workers
    ! from the master. In this example we replace this information by 
    ! a function that the worker can call
 
    ! all processes use the same time array so we could in theory read it by a
    ! master and distribute it to the workers but its cheaper
    ! if every process computes it 
    d_t=24*pi/t_dim !(assume a day and count t in hours)
    do k = 1,t_dim
      time(k)=k*d_t 
    end do  
    ! Create the netCDF file. The NF90_NETCDF4 flag causes a
    ! HDF5/netCDF-4 file to be created. The comm and info parameters
    ! cause parallel I/O to be enabled. Use either NF90_MPIIO or
    ! NF90_MPIPOSIX to select between MPI/IO and MPI/POSIX.
    call check(nf90_create(FILE_NAME, IOR(NF90_NETCDF4, NF90_MPIIO), ncid, &
         comm = worker_comm_id, info = MPI_INFO_NULL))

    ! Define the dimensions. NetCDF will hand back an ID for
    ! each. Metadata operations must take place on all processors.
    call check(nf90_def_dim(ncid, "x_data", wnp, x_dimid_data))
    call check(nf90_def_dim(ncid, "y_data", wnp, y_dimid_data))
    call check(nf90_def_dim(ncid, "time_data", NF90_UNLIMITED, temp_dimid_data)) 

    !call check(nf90_def_dim(ncid, "x_temperature", x_dim, x_dimid_temperature))
    !call check(nf90_def_dim(ncid, "time_temperature", NF90_UNLIMITED, temp_dimid_temperature)) 

    ! The dimids_data array is used to pass the IDs of the dimensions of
    ! the variables. Note that in fortran arrays are stored in
    ! column-major format.
    dimids_data = (/ y_dimid_data ,x_dimid_data ,temp_dimid_data /)

    ! define the chunk size (1 ayg unlimited time dimension)
    chunk_size_data = (/ wnp, 1, 1/)

    ! Define the variable. The type of the variable in this case is
    ! NF90_INT (4-byte integer).
    call check(nf90_def_var(  ncid, "data", NF90_INT, dimids_data  &
                              ,varid_data, chunksizes=chunk_size_data))

    ! End define mode. This tells netCDF we are done defining
    ! metadata. This operation is collective and all processors will
    ! write their metadata to disk.
    call check(nf90_enddef(ncid))
    !if (rank .ne. 0) then
    allocate(data_out(wnp), stat = stat)
    if (stat .ne. 0) stop 3
    do i = 1, wnp
       data_out(i) = rank
    end do
    call get_offsets_and_sizes(my_lp_index_offset ,my_lp_number&
      ,my_patch_ind_offset ,my_patch_number ,rank,wnp)
    ! for a temperature field we assume that it is indedpendent of the patches in a landpoint
    ! and only depend on the index of the landpoint
    !allocate(temp_out(1,my_lp_number))
    ! just to make the result easier to check we assume 
    ! temperature linearly increasing with the landpoint index
    !do i = 1,my_lp_number 
    !   temp_out(1,i) = real(my_lp_index_offset+i)/10.0
    !end do


  ! Write the pretend data to the file. Each processor writes one row.
    start_data = (/ 1, rank, 1/) !remember rank is a worker and starts from 1 
    !count_data = (/ wnp, 1 , 1/)
    call sleep(rank)
    print *,'rank: ',rank
    print *,'start_data: ',start_data
    print *,'count_data: ',count_data 

    ! Unlimited dimensions require collective writes
    call check(nf90_var_par_access(ncid, varid_data, nf90_collective))

    ! The unlimited axis prevents independent write tests
    ! Re-enable the worker_rank test if independent writes are used in the future
    call check(nf90_put_var(ncid, varid_data, data_out& 
                          ,start = start_data, count = count_data))

    ! Close the file. This frees up any internal netCDF resources
    ! associated with the file, and flushes any buffers.

    ! Free my local memory.
    deallocate(data_out)
    deallocate(temp_out)
  endif
  call check( nf90_close(ncid) )

  ! MPI library must be shut down.
  call MPI_Finalize(ierr)

  if (rank .eq. 0) print *, "*** SUCCESS writing example file ", FILE_NAME, "! "

contains
  subroutine check(status)
    integer, intent ( in) :: status
    
    if(status /= nf90_noerr) then 
      print *, trim(nf90_strerror(status))
      stop 2
    end if
  end subroutine check  

  subroutine get_offsets_and_sizes(my_lp_index_offset ,my_lp_number&
      ,my_patch_ind_offset ,my_patch_number ,worker_rank ,wnp)
    use mpi
    INTEGER,parameter :: mland=10 
    integer,intent(out):: my_lp_index_offset ,my_lp_number,my_patch_ind_offset ,my_patch_number 
    integer,intent(in):: worker_rank,wnp 
    integer mp,rest,lpw,wk
    integer,parameter,dimension(mland)  :: ps_per_lp= (/ 1,1,1,3,2,1,1,3,4,1/)
    integer,allocatable,dimension(:)::lps&
                                      ,lp_index_offsets&
                                      ,ps_per_process&
                                      ,ps_index_offsets
    allocate(lps(wnp))
    allocate(lp_index_offsets(wnp))
    allocate(ps_per_process(wnp))
    allocate(ps_index_offsets(wnp))
    ! this is a pretend subroutine that mimics the behaviour in cable
    ! where the number of patches/per landpoint is input from a file
    ! which is eveluated by the master process and send to the workers
    ! So every worker gets a message telling it how many patches it 
    ! is responsible for and where the first of these is (offset).
    ! and the same for the landpoints. 
    ! While most subroutines will write out data patchwise some will write
    ! landpoint wise
    ! all this information can be inferred from the patches array which 
    ! represents the cable input file the number of workers determined by
    ! the n parameter with which mpirun was startded and the
    ! worker_rank of the worker as returned by MPI_COMM_RANK at runtime 
    ! possibly reduced by one if rank 0 is the master.
    if (worker_rank<1) stop 3
    if (worker_rank==1) then
      print *,"wnp: ", wnp
      print *,"ps_per_lp: ", ps_per_lp
    endif
    mp=sum(ps_per_lp)
    
    lpw=mland/wnp
    rest=mod(mland,wnp)
    if (rest>0) then ! we have work left
      lpw=lpw+1
    endif
    
    ! this routine is called by every worker but it always has to consider
    ! what would be assinged to the other workers with lesser index since
    ! the offsets are cumulative
    lps(wnp)=mland-(wnp-1)*lpw
    lp_index_offsets(1)=0
    ps_index_offsets(1)=0
    do wk=1,(wnp-1)
      lps(wk)=lpw
      lp_index_offsets(wk+1)=sum(lps(1:wk))
      ps_per_process(wk)=sum(&
        ps_per_lp(&
          (lp_index_offsets(wk)+1):(lp_index_offsets(wk)+lps(wk))&
        )&
      )
      ps_index_offsets(wk+1)=sum(ps_per_process(1:wk))
    end do
    ps_per_process(wnp)= sum(&
        ps_per_lp(&
          (lp_index_offsets(wnp)+1):(lp_index_offsets(wnp)+lps(wnp))&
        )&
      )
    if (worker_rank .eq. 1) then
      print *,ps_per_lp(10:10)
      print *,sum(ps_per_lp(10:10))
      do wk=1,(wnp)
        print *,'###########################'
        print *,'wk',wk
        print *,'lps(wk)',lps(wk)
        print *,'lp_index_offsets(wk)',lp_index_offsets(wk)
        print *,'part',&
          ps_per_lp((lp_index_offsets(wk)+1):(lp_index_offsets(wk)+lps(wk)))
        print *,'sum(part)',&
          sum(ps_per_lp((lp_index_offsets(wk)+1):(lp_index_offsets(wk)+lps(wk))))
        print *,'lps(wk)',lps(wk)
        print *,'lp_index_offsets(wk)+lps',lp_index_offsets(wk)+lps(wk)
        print *,'ps_per_process(wk)',ps_per_process(wk)
        print *,'ps_index_offsets(wk)',ps_index_offsets(wk)
       end do
      endif
      my_lp_index_offset=lp_index_offsets(worker_rank)
      my_lp_number=lps(worker_rank)
      my_patch_ind_offset=ps_index_offsets(worker_rank)
      my_patch_number=ps_per_process(worker_rank)
     
  end subroutine get_offsets_and_sizes
    
  !function npatches (worker_rank,wnp)
  !  npatches=wland
  !  RETURN npatches
  !end function 
    
end program simple_xy_par_wr
