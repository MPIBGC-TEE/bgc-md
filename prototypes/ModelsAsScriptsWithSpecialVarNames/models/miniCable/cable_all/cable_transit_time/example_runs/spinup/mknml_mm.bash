startyr=1901
endyr=2100
yr=$startyr
while [ $yr -le $endyr ]
do
cat>./cable_C_spindump_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .TRUE.  ! input met data
   output%flux = .TRUE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .TRUE.  ! vegetation states
   output%params    = .TRUE.  ! input parameters used to produce run
   output%balances  = .FALSE.  ! energy and water balances
   output%casacnp   = .TRUE.
   output%averaging = 'monthly' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = 295.8   ! if not found in met file, in ppmv
   spincasainput = .TRUE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.   ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .FALSE. ! using prognostic Vcmax
   icycle = 1   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX//core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

cat>./cable_C_spincasa_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .TRUE.  ! input met data
   output%flux = .TRUE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .TRUE.  ! vegetation states
   output%params    = .TRUE.  ! input parameters used to produce run
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'monthly' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = 295.8   ! if not found in met file, in ppmv
   spincasainput = .TRUE.    ! input required to spin casacnp offline
   spincasa      = .TRUE.   ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .FALSE. ! using prognostic Vcmax
   icycle = 1   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX//core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

cat>./cable_C_spinup_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .TRUE.  ! input met data
   output%flux = .TRUE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .TRUE.  ! vegetation states
   output%params    = .TRUE.  ! input parameters used to produce run
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'monthly' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = 295.8   ! if not found in met file, in ppmv
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.   ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .FALSE. ! using prognostic Vcmax
   icycle = 1   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX//core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

cat>./cable_CN_spindump_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .TRUE.  ! input met data
   output%flux = .TRUE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .TRUE.  ! vegetation states
   output%params    = .TRUE.  ! input parameters used to produce run
   output%balances  = .FALSE.  ! energy and water balances
   output%casacnp   = .TRUE.
   output%averaging = 'monthly' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = 295.8   ! if not found in met file, in ppmv
   spincasainput = .TRUE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.   ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .TRUE. ! using prognostic Vcmax
   icycle = 2   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

cat>./cable_CN_spincasa_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .TRUE.  ! input met data
   output%flux = .TRUE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .TRUE.  ! vegetation states
   output%params    = .TRUE.  ! input parameters used to produce run
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'monthly' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = 295.8   ! if not found in met file, in ppmv
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .TRUE.   ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .TRUE. ! using prognostic Vcmax
   icycle = 2   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

cat>./cable_CN_spinup_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .TRUE.  ! input met data
   output%flux = .TRUE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .TRUE.  ! vegetation states
   output%params    = .TRUE.  ! input parameters used to produce run
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'monthly' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = 295.8   ! if not found in met file, in ppmv
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.   ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .TRUE. ! using prognostic Vcmax
   icycle = 2   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

cat>./cable_C_CCO2VMet_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc' 
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%grid    = 'land'
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .FALSE.  ! input met data
   output%flux = .FALSE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .FALSE.  ! NEE, GPP, NPP, stores
   output%GPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%NPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%HeteroResp= .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .FALSE.  ! vegetation states
   output%LAI       = .TRUE.
   output%params    = .FALSE.  ! input parameters used to produce run
   output%casacnp   = .TRUE.
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'daily' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = 295.8   ! if not found in met file, in ppmv
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.   ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE 
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .FALSE. ! using prognostic Vcmax
   icycle = 1   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       ! 
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp   
   casafile%dump_cnpspin ='output/cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are: 
                                                 ! 1. standard 
                                                 ! 2. non-linear extrapolation 
                                                 ! 3. Lai and Ktaul 2000 
   cable_user%DIAG_SOIL_RESP = 'ON ' 
   cable_user%LEAF_RESPIRATION = 'ON ' 
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are: 
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run 
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

lev=$(echo `awk -v x=$yr '{if($1==x) print $2;}' rcp85_conc_kf.txt`)

cat>./cable_C_VCO2CMet_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%grid    = 'land'
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .FALSE.  ! input met data
   output%flux = .FALSE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .FALSE.  ! NEE, GPP, NPP, stores
   output%GPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%NPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%HeteroResp= .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .FALSE.  ! vegetation states
   output%LAI       = .TRUE.
   output%params    = .FALSE.  ! input parameters used to produce run
   output%casacnp   = .TRUE.
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'daily' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = $lev ! if not found in met file, in ppmv;
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.    ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .FALSE.  ! using prognostic Vcmax
   icycle = 1   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='output/fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='output/cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = 1901 ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

lev=$(echo `awk -v x=$yr '{if($1==x) print $2;}' rcp85_conc_kf.txt`)

cat>./cable_C_VCO2VMet_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%grid    = 'land'
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .FALSE.  ! input met data
   output%flux = .FALSE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .FALSE.  ! NEE, GPP, NPP, stores
   output%GPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%NPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%HeteroResp= .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .FALSE.  ! vegetation states
   output%LAI       = .TRUE.
   output%params    = .FALSE.  ! input parameters used to produce run
   output%casacnp   = .TRUE.
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'daily' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = $lev ! if not found in met file, in ppmv;
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.    ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .FALSE.  ! using prognostic Vcmax
   icycle = 1   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='output/fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='output/cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

cat>./cable_CN_CCO2VMet_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc' 
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%grid    = 'land'
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .FALSE.  ! input met data
   output%flux = .FALSE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .FALSE.  ! NEE, GPP, NPP, stores
   output%GPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%NPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%HeteroResp= .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .FALSE.  ! vegetation states
   output%LAI       = .TRUE.
   output%params    = .FALSE.  ! input parameters used to produce run
   output%casacnp   = .TRUE.
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'daily' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = 295.8   ! if not found in met file, in ppmv
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.   ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE 
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .TRUE.  ! using prognostic Vcmax
   icycle = 2   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       ! 
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp   
   casafile%dump_cnpspin ='output/cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are: 
                                                 ! 1. standard 
                                                 ! 2. non-linear extrapolation 
                                                 ! 3. Lai and Ktaul 2000 
   cable_user%DIAG_SOIL_RESP = 'ON ' 
   cable_user%LEAF_RESPIRATION = 'ON ' 
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are: 
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run 
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

lev=$(echo `awk -v x=$yr '{if($1==x) print $2;}' rcp85_conc_kf.txt`)

cat>./cable_CN_VCO2CMet_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%grid    = 'land'
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%iveg = .TRUE.
   output%met = .FALSE.  ! input met data
   output%flux = .FALSE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .FALSE.  ! NEE, GPP, NPP, stores
   output%GPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%NPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%HeteroResp= .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .FALSE.  ! vegetation states
   output%LAI       = .TRUE.
   output%params    = .FALSE.  ! input parameters used to produce run
   output%casacnp   = .TRUE.
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'daily' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = $lev ! if not found in met file, in ppmv;
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.    ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .TRUE.  ! using prognostic Vcmax
   icycle = 2   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='output/fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='output/cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = 1901  ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.mean-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

lev=$(echo `awk -v x=$yr '{if($1==x) print $2;}' rcp85_conc_kf.txt`)

cat>./cable_CN_VCO2VMet_${yr}.nml<<EOF
&cable
   filename%met = ''
   filename%out = 'out_cable.nc'
   filename%log = './log_cable.txt'
   filename%restart_in  = './restart_in.nc'
   filename%restart_out = './restart_out.nc'
   filename%type    = '../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised.nc'
   filename%veg     = '../../CABLE-AUX/core/biogeophys/veg_params_cable_MK3L_v2_kf.txt'
   filename%soil    = '../../CABLE-AUX/core/biogeophys/def_soil_params.txt'
   vegparmnew = .TRUE.  ! using new format when true
   soilparmnew = .TRUE.  ! using new format when true
   spinup = .FALSE.  ! do we spin up the model?
   delsoilM = 0.001   ! allowed variation in soil moisture for spin up
   delsoilT = 0.01    ! allowed variation in soil temperature for spin up
   output%restart = .TRUE.  ! should a restart file be created?
   output%patch = .TRUE.
   output%patchfrac = .TRUE.
   output%grid = 'land'
   output%iveg = .TRUE.
   output%met = .FALSE.  ! input met data
   output%flux = .FALSE.  ! convective, runoff, NEE
   output%soil = .FALSE.  ! soil states
   output%snow = .FALSE.  ! snow states
   output%radiation = .FALSE.  ! net rad, albedo
   output%carbon    = .FALSE.  ! NEE, GPP, NPP, stores
   output%GPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%NPP       = .TRUE.  ! NEE, GPP, NPP, stores
   output%HeteroResp= .TRUE.  ! NEE, GPP, NPP, stores
   output%veg       = .FALSE.  ! vegetation states
   output%LAI       = .TRUE.
   output%params    = .FALSE.  ! input parameters used to produce run
   output%casacnp   = .TRUE.
   output%balances  = .FALSE.  ! energy and water balances
   output%averaging = 'daily' ! choices: all, daily, monthly, userNNN where NNN is the number of hours
   check%ranges     = .FALSE.  ! variable ranges, input and output
   check%energy_bal = .FALSE.  ! energy balance
   check%mass_bal   = .FALSE.  ! water/mass balance
   verbose = .FALSE. ! write details of every grid cell init and params to log?
   leaps = .FALSE. ! calculate timing with leap years?
   logn = 88      ! log file number - declared in input module
   fixedCO2 = $lev ! if not found in met file, in ppmv;
   spincasainput = .FALSE.    ! input required to spin casacnp offline
   spincasa      = .FALSE.    ! spin casa before running the model if TRUE, and should be set to FALSE if spincasainput = .TRUE.
   l_casacnp     = .TRUE.  ! using casaCNP with CABLE
   l_laiFeedbk   = .TRUE.  ! using prognostic LAI
   l_vcmaxFeedbk = .TRUE.  ! using prognostic Vcmax
   icycle = 2   ! BP pull it out from casadimension and put here; 0 for not using casaCNP, 1 for C, 2 for C+N, 3 for C+N+P
   casafile%cnpipool     ='./poolcnp_in.csv'       !
   casafile%cnpbiome     ='../../CABLE-AUX/core/biogeochem/pftlookup_csiro_v16_17tiles_K1.csv'  ! biome specific BGC parameters
   casafile%cnpepool     ='./poolcnp_out.csv'       ! end of run pool size
   casafile%cnpmetout    ='output/casamet.nc'            ! output daily met forcing for spinning casacnp
   casafile%cnpmetin     ='output/fcasamet.lst'          ! list of daily met files for spinning casacnp
   casafile%cnpspin      ='output/fcnpspin.lst'          ! list of cnp dump file for spinning up casacnp
   casafile%dump_cnpspin ='output/cnpspindump${yr}.nc'          ! list of daily met files for spinning casacnp
   casafile%phen         ='../../CABLE-AUX/core/biogeochem/modis_phenology_csiro.txt'        ! modis phenology
   casafile%cnpflux      ='cnpflux${yr}.csv'
   casafile%ndep         ='../../CABLE-AUX/ndep/ndep_${yr}_1.9x2.5_KF.nc'
   casafile%l_ndep       =.TRUE.
   ncciy = ${yr} ! 0 for not using gswp; 4-digit year input for year of gswp met
   gswpfile%l_gpcc =.FALSE.
   gswpfile%l_gswp =.FALSE.
   gswpfile%l_ncar =.TRUE.
   gswpfile%rainf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%snowf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%LWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%SWdown= '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%PSurf = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Qair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%Tair  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   gswpfile%wind  = '../NCAR/CLM45sp_2deg45r086_hist.clm2.h1.${yr}-01-01-00000.nc'
   redistrb = .FALSE.  ! Turn on/off the hydraulic redistribution
   wiltParam = 0.5
   satuParam = 0.8
   cable_user%FWSOIL_SWITCH = 'standard'        ! choices are:
                                                 ! 1. standard
                                                 ! 2. non-linear extrapolation
                                                 ! 3. Lai and Ktaul 2000
   cable_user%DIAG_SOIL_RESP = 'ON '
   cable_user%LEAF_RESPIRATION = 'ON '
   cable_user%RUN_DIAG_LEVEL= 'BASIC'        ! choices are:
                                                 ! 1. BASIC
                                                 ! 1. NONE
   cable_user%CONSISTENCY_CHECK= .TRUE.      ! TRUE outputs combined fluxes at each timestep for comparisson to A control run
   cable_user%CASA_DUMP_READ = .FALSE.      ! TRUE reads CASA forcing from netcdf format
   cable_user%CASA_DUMP_WRITE = .FALSE.      ! TRUE outputs CASA forcing in netcdf format
   cable_user%SSNOW_POTEV= 'P-M'      ! Humidity Deficit Method
&end

EOF

yr=`expr $yr + 1`
done