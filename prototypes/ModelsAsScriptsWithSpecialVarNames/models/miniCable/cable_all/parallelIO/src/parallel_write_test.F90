! - example of parallel MPI write into a single file, in Fortran

program test
  use mpi 
  implicit none
  
  integer                       :: ierr, i, myrank, thefile 
  integer ,parameter            :: BUFSIZE=10 
  !integer (kind=MPI_INTEGER)    :: buf(BUFSIZE) 
  integer                       :: buf(BUFSIZE) 
  integer (kind=MPI_OFFSET_KIND):: disp 
  
  call MPI_INIT(ierr) 
  call MPI_COMM_RANK(MPI_COMM_WORLD, myrank, ierr) 
  
  do i = 0, BUFSIZE 
      buf(i) = myrank 
  enddo 
  call MPI_FILE_OPEN(MPI_COMM_WORLD, 'datafile.contig', & 
                     MPI_MODE_WRONLY + MPI_MODE_CREATE, & 
                     MPI_INFO_NULL, thefile, ierr) 
  ! assume 4-byte integers 
  !disp = myrank * BUFSIZE * sizeof(MPI_INTEGER)
  disp = myrank * sizeof(buf)
  !call MPI_FILE_SET_VIEW(&
  !  thefile,       &
  !  disp,          &
  !  MPI_INTEGER,   & 
  !  MPI_INTEGER,   &
  !  'native',      &                      
  !  MPI_INFO_NULL, &
  !  ierr) 

  !call MPI_FILE_WRITE(&
  !  thefile, &
  !  buf, &
  !  BUFSIZE, &
  !  MPI_INTEGER, &
  !  MPI_STATUS_IGNORE, & 
  !  ierr &
  !) 
  call MPI_FILE_WRITE_AT_ALL( &
    thefile, &
    disp, &
    buf, & 
    BUFSIZE, &
    MPI_INTEGER, &
    MPI_STATUS_IGNORE, &
    ierr &
  ) 
  print *,'ierr',ierr
  print *,'offset',disp
  call MPI_FILE_CLOSE(thefile, ierr) 
  call MPI_FINALIZE(ierr) 
 
end program test


