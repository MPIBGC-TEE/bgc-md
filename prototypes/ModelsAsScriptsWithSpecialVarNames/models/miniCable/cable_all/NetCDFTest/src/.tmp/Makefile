#==============================================================================
# these are all the files we are compiling
LSRC = sfc_pres_temp_wr.F90 

# this is the executable we are building
PROG = sfc_pres_temp_wr

# from the compiled object files 
OBJS	= ${LSRC:.F90=.o} 

#compiler switches and flags
CINC = -I$(NCMOD)

#suffixes we use
.SUFFIXES:
.SUFFIXES: .F90 .o 
#default rules for these suffixes
.F90.o:
	$(FC) $(CFLAGS) $(CINC) -c $<

# default target by convention is ``all''
all : $(PROG)

#build PROG (executable) by linking all objects
#$(PROG) : $(OBJS)
$(PROG) : sfc_pres_temp_wr.o 
	$(FC) $(LDFLAGS) -o $@ $(OBJS) $(LD) 


## dependencies
#cable_abort.o: cable_abort.F90 cable_iovars.o cable_define_types.o
#
clean:
	rm -f *.o *.mod 

