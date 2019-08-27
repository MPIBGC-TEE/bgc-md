!     http://www.unidata.ucar.edu/software/netcdf/docs/netcdf-tutorial
module constants
  real(kind=8), parameter    :: pi = 3.1415927                
end module

program simple_xy_par_wr

  use netcdf
  use mpi
  use constants

  implicit none
 
  INTEGER :: ierr,wnp,rank_in_world,nproc
  integer :: world_group_id,worker_group_id,rank_in_worker_comm,wnptest,worker_comm_id
  character (len = *), parameter :: SERIAL_FILE_NAME = "simple_xy.nc"
  character (len = *), parameter :: PARALLEL_FILE_NAME = "simple_xy_par.nc"
  ! We assume the points to be threaded on a single string
  ! We are writing a temperature timeline 1D
  ! for every point. So the dimension for the temperature data is 2
  integer,      parameter :: NDIMS_data = 3 ,NDIMS_temperature= 2 ,t_dim=48

  integer                 ::i, j,k,l,mland

  ! When we create netCDF files, variables and dimensions, we get back
  ! an ID for each one.
  integer :: ncid_par,ncid_ser, varid_data, varid_temperature&
            ,dimids_data(NDIMS_data)&
            ,dimids_temperature(NDIMS_temperature)&
            ,x_dimid_data, y_dimid_data, temp_dimid_data &
            ,lp_dimid_temp, time_dimid_temp&
            ,my_lp_index_offset ,my_lp_number&
            ,my_patch_ind_offset ,my_patch_number
            
  ! add chunk size for unlimited variables
  integer :: chunk_size_data(NDIMS_data),chunk_size_temperature(NDIMS_temperature)

  ! These will tell where in the data file this processor should write.
  integer :: start_data(NDIMS_data), count_data(NDIMS_data)
  integer :: start_temperature(NDIMS_temperature), count_temperature(NDIMS_temperature)
  
  ! This is the data array we will write. It will just be filled with
  ! the rank_in_world of this processor.
  integer, allocatable :: data_out(:)
  integer, allocatable :: temperature_out(:)
  integer, allocatable :: worker_ranks(:) !array of the ranks of the workers. Note that the entries are w.r.t. COMM_WORLD and not
  real, allocatable :: temp_out(:,:)
  
  real(kind=8), parameter                       :: min_x=0,max_x=1,span_x=max_x-min_x
  real(kind=8)                                  :: d_t,d_x ,my_offset ,patch_extend

  real(kind=8)             , dimension(t_dim)   :: time
  real(kind=8), allocatable, dimension(:)       :: my_xs
  real(kind=8), allocatable, dimension(:,:)     :: my_temperatures
  logical :: i_am_a_worker,i_am_master


  ! Initialize MPI, learn local rank and total number of processors.
  call MPI_Init(ierr)
  call MPI_Comm_rank(MPI_COMM_WORLD, rank_in_world, ierr)
  call MPI_Comm_size(MPI_COMM_WORLD, nproc, ierr)
  call MPI_Comm_group ( MPI_COMM_WORLD, world_group_id, ierr )
  wnp=nproc-1
  allocate ( worker_ranks(1:wnp)) 
  do i = 1, wnp ! we start with 1 since the master will be excluded 
    worker_ranks(i) = i
  end do
  
  !if (rank_in_world ==1) print *,'worker_ranks: ',worker_ranks
  call MPI_Comm_group ( MPI_COMM_WORLD, world_group_id, ierr ) !world group is now the group of all processes in MPI_COMM_WORLD
  call MPI_Group_incl ( world_group_id, wnp,worker_ranks, worker_group_id, ierr )
  ! create the new communicator, the variable worker_comm_id
  ! will be equal to MPI_Comm_null if our process does not belong to the
  ! group and some integer otherwise
  call MPI_Comm_create ( MPI_COMM_WORLD, worker_group_id, worker_comm_id, ierr ) 
  i_am_a_worker=worker_comm_id /= MPI_Comm_null
  i_am_master =rank_in_world==0
  if (i_am_master) then
    ! open a different netcdf file in serial mode and write some 
    ! information to it that does not depend on the workers
    ! we could also use the same file as the workers but would have
    ! to close it first in the master and AFTERWARDS open it in parallel
    ! mode in the workers which would force us to syncronize.
    ! If we use an extra file for the master we can access it 
    ! asyncronously.
    ! After the program is finished we can add the serial variables to the
    ! file that was previously opened for parallel access.
    ! 
    ! I t might be possibe to achive the same effect only using 
    ! the file in parallel mode and let the master write a different variable
    ! but this is not clear yet

    call check(nf90_create(SERIAL_FILE_NAME, NF90_NETCDF4, ncid_ser))
    call check( nf90_close(ncid_ser) )

  endif

  if (i_am_a_worker) then
    ! only workers can get their rank and the size of their communicator
    call MPI_Comm_rank(worker_comm_id, rank_in_worker_comm, ierr)
    call MPI_Comm_size(worker_comm_id, wnptest, ierr)
    !if (rank_in_world ==1)print *,'wnptest: ',wnptest
    ! get cable like information about which worker owns which landpoints and
    ! patches
    call get_offsets_and_sizes(my_lp_index_offset ,my_lp_number&
      ,my_patch_ind_offset ,my_patch_number ,mland,rank_in_worker_comm,wnp)
    
    ! Create some pretend data. We just need one row.
    allocate(data_out(wnp), stat = ierr)
    if (ierr .ne. 0) stop 3
    do i = 1, wnp
       data_out(i) = rank_in_worker_comm
    end do
    allocate(temperature_out(my_lp_number), stat = ierr)
    if (ierr .ne. 0) stop 3
    ! HDF5/netCDF-4 file to be created. The comm and info parameters
    ! cause parallel I/O to be enabled. Use either NF90_MPIIO or
    ! NF90_MPIPOSIX to select between MPI/IO and MPI/POSIX.
    call check(nf90_create(PARALLEL_FILE_NAME, IOR(NF90_NETCDF4, NF90_MPIIO), ncid_par, &
         comm = worker_comm_id, info = MPI_INFO_NULL))

    ! Define the dimensions. NetCDF will hand back an ID for
    ! each. Metadata operations must take place on all processors.
    call check(nf90_def_dim(ncid_par, "x_data", wnp, x_dimid_data))
    call check(nf90_def_dim(ncid_par, "y_data", wnp, y_dimid_data))
    call check(nf90_def_dim(ncid_par, "time_data", NF90_UNLIMITED, temp_dimid_data)) 
    call check(nf90_def_dim(ncid_par, "lp_temperature", mland, lp_dimid_temp))
    call check(nf90_def_dim(ncid_par, "time_temperature", NF90_UNLIMITED, time_dimid_temp)) 

    ! Note that in fortran arrays are stored in
    ! column-major format.
    !dimids_data = (/ y_dimid_data ,x_dimid_data ,temp_dimid_data /)
    dimids_temperature= (/ lp_dimid_temp,time_dimid_temp/)

    ! define the chunk size (1 ayg unlimited time dimension)
    !chunk_size_data = (/ wnp, 1, 1/)
    chunk_size_temperature= (/ my_lp_number-1, 1/)

    ! Define the variable. The type of the variable in this case is
    ! NF90_INT (4-byte integer).
    !call check(&
    !  nf90_def_var(&
    !    ncid_par&
    !    ,"data"&
    !    ,NF90_INT&
    !    ,dimids_data&
    !    ,varid_data&
    !    ,chunksizes=chunk_size_data&
    !  )&
    !)
    call check(&
      nf90_def_var(&
        ncid_par&
        ,"temperature"&
        ,NF90_DOUBLE&
        ,dimids_temperature&
        ,varid_temperature&
        !,chunksizes=chunk_size_temperature&
      )&
    )

    ! End define mode. This tells netCDF we are done defining
    ! metadata. This operation is collective and all processors will
    ! write their metadata to disk.
    call check(nf90_enddef(ncid_par))



  ! Write the pretend data to the file. Each processor writes one row.
    !start_data = (/ 1, rank_in_worker_comm+1, 1/) 
    !count_data = (/ wnp, 1 , 1/)

    ! Unlimited dimensions require collective writes
    !call check(nf90_var_par_access(ncid_par, varid_data, nf90_collective))
    call check(nf90_var_par_access(ncid_par, varid_temperature, nf90_collective))

    !call check(&
    !  nf90_put_var(&
    !    ncid_par&
    !    ,varid_data&
    !    ,data_out& 
    !    ,start = start_data&
    !    ,count = count_data&
    !  )&
    !)
    do i=1,5
      start_temperature=(/ my_lp_index_offset+1,i /)
      count_temperature=(/ my_lp_number,1 /)
      do j = 1, my_lp_number
         temperature_out(j) = i*real(j+my_lp_index_offset)
        !temperature_out(j) = real(rank_in_worker_comm)
      end do
      call check(&
        nf90_put_var(&
          ncid_par&
          ,varid_temperature&
          ,temperature_out& 
          ,start = start_temperature&
          ,count = count_temperature&
        )&
      )
    enddo
    ! Close the file. This frees up any internal netCDF resources
    ! associated with the file, and flushes any buffers.
    call check( nf90_close(ncid_par) )

    ! Free my local memory.
    deallocate(data_out)
    deallocate(temperature_out)
  endif

  ! MPI library must be shut down.
  call MPI_Finalize(ierr)

  if (rank_in_world .eq. 0) then
    print *, "*** SUCCESS writing example files ", SERIAL_FILE_NAME,&
      " and ",PARALLEL_FILE_NAME,"! "
  endif 

contains
  subroutine check(status)
    integer, intent ( in) :: status
    
    if(status /= nf90_noerr) then 
      print *, trim(nf90_strerror(status))
      stop 2
    end if
  end subroutine check  

  subroutine get_offsets_and_sizes(my_lp_index_offset ,my_lp_number&
      ,my_patch_ind_offset ,my_patch_number,mland,rank_in_worker_comm ,wnp)
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
    ! rank_in_worker_comm of the worker as returned by MPI_COMM_RANK at runtime 
    ! possibly reduced by one if rank 0 is the master.
    use mpi
    INTEGER,intent(out):: mland
    integer,intent(out):: my_lp_index_offset ,my_lp_number,my_patch_ind_offset ,my_patch_number 
    integer,intent(in):: rank_in_worker_comm,wnp 
    integer mp,rest,lpw,wk
    integer,parameter,dimension(10)  :: ps_per_lp= (/ 1,1,1,3,2,1,1,3,4,1/)
    integer,allocatable,dimension(:)::lps&
                                      ,lp_index_offsets&
                                      ,ps_per_process&
                                      ,ps_index_offsets
    allocate(lps(0:wnp-1))
    allocate(lp_index_offsets(0:wnp-1))
    allocate(ps_per_process(0:wnp-1))
    allocate(ps_index_offsets(0:wnp-1))
    mland=size(ps_per_lp)
    mp=sum(ps_per_lp)
    
    rest=mod(mland,wnp)
    if (rest>0) then ! we have work left
      lpw=mland/wnp+1
    else
      lpw=mland/wnp
    endif
    
    ! this routine is called by every worker but it always has to consider
    ! what would be assinged to the other workers with lesser index since
    ! the offsets are cumulative
    lps(wnp-1)=mland-(wnp-1)*lpw 
    lps(0)=lpw
    lp_index_offsets(0)=0
    ps_index_offsets(0)=0
    do wk=0,(wnp-2)
      lps(wk)=lpw
      lp_index_offsets(wk+1)=sum(lps(0:wk))
      ps_per_process(wk)=sum(&
        ps_per_lp(&
          (lp_index_offsets(wk)+1):(lp_index_offsets(wk)+lps(wk))&
        )&
      )
      ps_index_offsets(wk+1)=sum(ps_per_process(0:wk))
    end do
    ps_per_process(wnp-1)= sum(&
        ps_per_lp(&
          (lp_index_offsets(wnp-1)+1):(lp_index_offsets(wnp-1)+lps(wnp-1))&
        )&
      )
    if (rank_in_worker_comm .eq. 0) then
      print *,"wnp: ", wnp
      print *,"rest: ", rest
      print *,"lpw: ", lpw
      print *,"ps_per_lp: ", ps_per_lp
      do wk=0,(wnp-1)
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
      my_lp_index_offset=lp_index_offsets(rank_in_worker_comm)
      my_lp_number=lps(rank_in_worker_comm)
      my_patch_ind_offset=ps_index_offsets(rank_in_worker_comm)
      my_patch_number=ps_per_process(rank_in_worker_comm)
     
  end subroutine get_offsets_and_sizes
    
  !function i_am_a_worker (world_rank)
  !  integer :: world_rank 
  !  logical :: i_am_a_worker
  !  i_am_a_worker = world_rank .ne. 0
  !  RETURN 
  !end 
    
end program simple_xy_par_wr
