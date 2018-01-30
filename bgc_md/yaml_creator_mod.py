# vim:set ff=unix expandtab ts=4 sw=4:
def example_yaml_string_list2():
    yaml_str_list=[]
    yaml_str_list.append("""\
citationKey: Hilbert1991AnnBot
name: 
version: 1
model-id: V0004
entryAuthor: "Verónika Ceballos-Núñez"
entryAuthorOrcid: 0000-0002-0046-1160
entryCreationDate: 29/7/2015 # cahngeset: 2256
lastModification: _lm_
modApproach: process based
partitioningScheme: dynamic
spaceScale: global 
#    unit: "1°"
timeResolution: monthly 
abstract: "A model is developed that considers the allocation of carbon and nitrogen substrates to a protein compartment in the shoots, shoot structural components, and root biomass. Inclusion of a shoot-protein compartment allows variation in shoot-specific activity to be modelled as a function of leaf nitrogen concentration. Allocation to the biomass compartments is controlled by two partitioning variables that are defined by explicitly using the balanced activity hypothesis. The model produces balanced activity where the shoot-specific activity, as well as root and shoot biomass, vary in response to the above-ground (light and CO$_2$) and below-ground (nitrogen) environments. The predicted patterns of both root: shoot ratio and leaf nitrogen concentration in response to environmental resource availability are qualitatively consistent with general trends observed in plants."
bibtex: "@article{Hilbert1991Annals_of_Botany,
            Author = {Hilbert, David W. and Reynolds, James F.},
            Journal = {Annals of Botany},
            Number = {5},
            Pages = {417-425},
            Title = {A Model Allocating Growth Among Leaf Proteins, Shoot Structure, and Root Biomass to Produce Balanced Activity},
            Url = {http://aob.oxfordjournals.org/content/68/5/417.abstract},
            Volume = {68},
            Year = {1991}
        }"
#t = # units: days, years for allocation
model:
    - state_variables:
        - W_p:
            desc: Mass of leaf proteins
            key: "foliage"
        - W_s:
            desc: Mass of leaf structural components
            key: "foliage"
        - W_r:
            desc: Mass of roots
            key: "fine_roots"
        - W_C:
            desc: Substrate carbon
        - W_N:
            desc: Substrate nitrogen
    - additional_variables:
        - W_g:
            desc: Plant biomass
            type: variable
            exprs: "W_g = W_p + W_s + W_r"
        - kappa:
            desc: growth rate coefficient
            type: parameter
        - sigma_c:
            desc: photosynthetic rate per unit leaf
            type: parameter
        - sigma_r:
            desc: specific root activity 
            type: variable
            unit: "[g N (g root)^{-1} d^{-1}]"
        - h_max:
            desc: leaf max. thickness
            type: parameter
            unit: "[m]"
        - h_half:
            desc: $h_0.5$ leaf half thickness
            type: parameter
        - I:
            desc: photon flux density
            type: variable
        - rho:
            desc: leaf density
            type: variable
        - f_C:
            desc: proportion of carbon
            type: parameter
        - f_N:
            desc: proportion of nitrogen
            type: parameter
        - Beta:
            desc: target whole plant nitrogen:carbon ratio
            type: parameter
        - f_cp:
            desc: proportion of carbon in leaf proteins
            type: parameter
        - f_cs:
            desc: proportion of carbon in leaf structural components
            type: parameter
        - f_cr:
            desc: proportion of carbon in roots
            type: parameter
        - f_np:
            desc: proportion of nitrogen in leaf proteins
            type: parameter
        - f_ns:
            desc: proportion of nitrogen in leaf structural components
            type: parameter
        - f_nr:
            desc: proportion of nitrogen in roots
            type: parameter
        - C:
            desc: Substrate carbon concentration
            type: variable
            exprs: "C = W_C/W_g"
        - N:
            desc: Substrate nitrogen concentration
            type: variable
            exprs: "N = W_N/W_g"
        - h:
            desc:
            type: variable
            exprs: "h = h_max*I/(h_half+I)"
        - A:
            desc: Area
            type: variable
            exprs: "A = W_s/rho*h"
        - P:
            desc:
            type: variable
            exprs: "P = f_C*sigma_r*W_r/f_N*sigma_c*A"
    
        - Q:
            desc:
            type: parameter
            exprs: "Q = f_N/(Beta*f_C)"
    
    - allocation_coefficients:
        - lambda_p:
            desc:
            type: variable
            unit: 
            exprs: "lambda_p = P/(1+P+Q)"
        - lambda_s:
            desc:
            type: variable
            unit: 
            exprs: "lambda_s = Q/(1+P+Q)"
        - lambda_r:
            desc:
            type: variable
            unit:
            exprs: "lambda_r = 1/(1+P+Q)"

    - auxiliary_variables:
        - O_C:
            desc: "output share of $W_C$"
            exprs: "O_C = f_cp*lambda_p*W_p+f_cs*lambda_s*W_s+f_cr*lambda_r*W_r"
            entryAuthorOrcid: 0000-0002-8239-1601
        - O_N:
            desc: "output share of $W_N$"
            exprs: "O_N = f_np*lambda_p*W_p+f_ns*lambda_s*W_s+f_nr*lambda_r*W_r"
            entryAuthorOrcid: 0000-0002-8239-1601
    - components:
        - x: 
            key: state_vector 
            exprs: "x=Matrix(5,1,[W_p, W_s, W_r, W_C, W_N])"
            desc: vector of states for vegetation
            entryAuthorOrcid: 0000-0002-8239-1601
        - Inp:
            exprs: "Inp = Matrix(5, 1, [(1-f_cp-f_np)*C*N*kappa*lambda_p*W_p,
                                        (1-f_cs-f_ns)*C*N*kappa*lambda_s*W_s,
                                        (1-f_cr-f_nr)*C*N*kappa*lambda_r*W_r,
                                        sigma_c*A,
                                        sigma_r*W_r])"

            desc: external inputs through photosysthesis and roots
            entryAuthorOrcid: 0000-0002-8239-1601
        - T:
            exprs: "T = Matrix([[-1,  0,  0, f_cp*lambda_p*W_p/O_C, f_np*lambda_p/O_N*W_p],
                                [ 0, -1,  0, f_cs*lambda_s*W_s/O_C, f_ns*lambda_s/O_N*W_s],
                                [ 0,  0, -1, f_cr*lambda_r*W_r/O_C, f_nr*lambda_r/O_N*W_r],
                                [ 0,  0,  0,                -1,               0],
                                [ 0,  0,  0,                 0,              -1]])"

            entryAuthorOrcid: 0000-0002-8239-1601
        - N_gm: 
            exprs: "N_gm = diag(0, 0, 0, kappa*N/W_g*O_C, kappa*C/W_g*O_N)"
            entryAuthorOrcid: 0000-0002-8239-1601
        - f_v: 
            key: state_vector_derivative  
            exprs: "f_v = Inp + T * N_gm * x"
            desc: the righthandside of the ode
            entryAuthorOrcid: 0000-0002-8239-1601
#        - f_v: 
#            key: state_vector_derivative  
#            exprs: "f_v = Matrix(5,1,[kappa*C*N*lambda_p*W_p, kappa*C*N*lambda_s*W_s, kappa*C*N*lambda_r*W_r, sigma_c*A-f_cp*kappa*C*N*lambda_p*W_p-f_cs*kappa*C*N*lambda_s*W_s-f_cr*kappa*C*N*lambda_r*W_r, sigma_r*W_r-f_np*kappa*C*N*lambda_p*W_p-f_ns*kappa*C*N*lambda_s*W_s-f_nr*kappa*C*N*lambda_r*W_r])"
#            desc: the righthandside of the ode
model_run_data:
    parameter_sets:
        - "Original dataset of the publication":
            values: {lambda_p: 'Rational(1,3)', lambda_s: 'Rational(1,3)', lambda_r: 'Rational(1,3)'}
            bibtex: "@article{Hilbert1991Annals_of_Botany,
                        Author = {Hilbert, David W. and Reynolds, James F.},
                        Journal = {Annals of Botany},
                        Number = {5},
                        Pages = {417-425},
                        Title = {A Model Allocating Growth Among Leaf Proteins, Shoot Structure, and Root Biomass to Produce Balanced Activity},
                        Url = {http://aob.oxfordjournals.org/content/68/5/417.abstract},
                        Volume = {68},
                        Year = {1991}
                    }"
"""
)

    yaml_str_list.append("""\
citationKey: Potter1993GlobalBiogeochemCy
name: CASA
version: 1
model-id: V0002
entryAuthor: "Verónika Ceballos-Núñez"
entryAuthorOrcid: 0000-0002-0046-1160
entryCreationDate: 17/7/2015 # changeset 2200 (.py)
lastModification: _lm_
modApproach: process based
partitioningScheme: fixed
# Seasonal resolution of global climatic and edaphic controlson patterns of terrestrial ecosystem production and soil microbial respiration.
spaceScale: global 
#    unit: "1°"
timeResolution: monthly 
#    unit: month^{-1}
doi: 10.1029/93GB02725
# 10.2307/1313568 1999 paper
model:
    - state_variables:
        - C_f:
            desc: Carbon in foliage
            key: "foliage"
        - C_r: 
            desc: Carbon in roots 
            key: "fine_roots"
        - C_w:
            desc: Carbon in woody tissue
            key: "wood"
    
    - photosynthetic_parameters:
# The model estimate of global terrestrianet primary production is 48 PgC yr -1 with a maximum light use efficiency of 0.39 g C MJ -1 PAR.
        - SOL: 
            desc: Total solar radiation (SOL(x,t))
            type: variable
        - FPAR:
            desc: Fraction of incoming PAR intercerpted by green vegetation (FPAR(x,t))
            type: variable
#            exprs: FPAR is function of NDVI and SR (see page 6 of Potter1993GlobalBiogeochemCy)
        - IPAR:
            desc: "Intercepted photosynthetically active radiation(IPAR(x,t)). The factor of 0.5 accounts for the fact that approx. half of SOL is in PAR" 
            type: variable
            exprs: "IPAR = SOL*FPAR*0.5"
        - epsilon:
            desc: "PAR use efficiency ($\\epsilon(x,t)$). Function that depends on effects of temperature and water stress"
#            exprs: epsilon is function of other functions that depend on soil module (see pages 6-10 of Potter1993GlobalBiogeochemCy)
            type: variable
            unit: km^2
        - NPP:
            desc: New production of plant biomass (NPP(x,t)) at a grid cell ($x$) in month $t$
            # exprs: "NPP = IPAR * epsilon"
            type: variable
            key: NPP
    - allocation_coefficients:
        - alpha_f:
            desc: Proportional allocation constant of available carbon allocated to foliage
            type: parameter
            key: "part_foliage"
        - alpha_r:
            desc: Proportional allocation constant of available carbon allocated to roots
            type: parameter
            key: "part_roots"
        - alpha_w:
            desc: Proportional allocation constant of available carbon allocated to wood
            type: parameter
            key: "part_wood"
    - cycling_rates:
        - tau_f: 
            desc: Residence time of carbon in foliage 
            unit: years
            type: parameter
            key: "cyc_foliage"
        - tau_r:
            desc: Residence time of carbon in roots
            unit: years
            type: parameter
            key: "cyc_roots"
        - tau_w:
            desc: Residence time of carbon in wood
            unit: years
            type: parameter
            key: "cyc_wood"
    - components:
        # you are required to provide at least expressions for f u x and A
        # you are allowed to use as many helper expressions as you want to arrive there
        # e.g.
        # p= x**2 # allowed just for conviniece
        # f =p**2.. #required
        - x: 
            key: state_vector 
            exprs: "x=Matrix(3,1,[C_f, C_r, C_w])"
            desc: vector of states for vegetation
        - u: 
            key: scalar_func_phot    
            exprs: "u=NPP"
            desc: scalar function of photosynthetic inputs
        - b: 
            key: part_coeff    
            exprs: "b=Matrix(3,1,[alpha_f, alpha_r, alpha_w])"
            desc: vector of partitioning coefficients of photosynthetically fixed carbon
        - A: 
            key: cyc_matrix    
            exprs: "A=diag(-tau_f, -tau_r, -tau_w)"
            desc: matrix of turnover (cycling) rates 
        - f_v: 
            key: state_vector_derivative  
            exprs: "f_v = u*b + A*x"
            desc: the righthandside of the ode

model_run_data:
    parameter_sets:
        - "Original dataset of the publication":
            values: {alpha_f: 'Rational(1,3)',alpha_r: 'Rational(1,3)',alpha_w: 'Rational(1,3)'}
# epsilon varies from 1.1 - 1.4 gC*MJ^{-1}PAR in crop ecosystems.
            doi: 10.1029/93GB02725
        - "Tundra":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "High-latitude forest":
            values: {alpha_f: 0.30, alpha_r: 0.25, alpha_w: 0.45, tau_f: 1, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "Boreal coniferous forest":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 2.5, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "Temperate grassland":
            values: {alpha_f: 0.45, alpha_r: 0.55, tau_f: 1.5, tau_r: 5}
            doi: 10.2307/1313568
        - "Mixed coniferous forest":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 3, tau_w: 40}
            doi: 10.2307/1313568
        - "Temperate deciduous forest":
            values: {alpha_f: 0.30, alpha_r: 0.25, alpha_w: 0.45, tau_f: 1, tau_r: 3, tau_w: 40}
            doi: 10.2307/1313568
        - "Desert and bare ground":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "Semi-arid shrubland":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "Savanna and woody grassland":
            values: {alpha_f: 0.30, alpha_r: 0.25, alpha_w: 0.45, tau_f: 1, tau_r: 5, tau_w: 25}
            doi: 10.2307/1313568
        - "Tropical evergreen rain forest":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 2, tau_w: 25}
            doi: 10.2307/1313568
    """
    )
    yaml_str_list.append("""\
citationKey: Potter1993GlobalBiogeochemCy
name: CASA2
version: 1
model-id: V0002
entryAuthor: "Verónika Ceballos-Núñez"
entryAuthorOrcid: 0000-0002-0046-1160
entryCreationDate: 17/7/2015 # changeset 2200 (.py)
lastModification: _lm_
modApproach: process based
partitioningScheme: fixed
# Seasonal resolution of global climatic and edaphic controlson patterns of terrestrial ecosystem production and soil microbial respiration.
spaceScale: global 
#    unit: "1°"
timeResolution: monthly 
#    unit: month^{-1}
doi: 10.1029/93GB02725
# 10.2307/1313568 1999 paper
model:
    - state_variables:
        - C_f:
            desc: Carbon in foliage
            key: "foliage"
        - C_r: 
            desc: Carbon in roots 
            key: "fine_roots"
        - C_w:
            desc: Carbon in woody tissue
            key: "wood"
    
    - photosynthetic_parameters:
# The model estimate of global terrestrianet primary production is 48 PgC yr -1 with a maximum light use efficiency of 0.39 g C MJ -1 PAR.
        - SOL: 
            desc: Total solar radiation (SOL(x,t))
            type: variable
        - FPAR:
            desc: Fraction of incoming PAR intercerpted by green vegetation (FPAR(x,t))
            key: fridolin
            type: variable
#            exprs: FPAR is function of NDVI and SR (see page 6 of Potter1993GlobalBiogeochemCy)
        - IPAR:
            desc: "Intercepted photosynthetically active radiation(IPAR(x,t)). The factor of 0.5 accounts for the fact that approx. half of SOL is in PAR" 
            type: variable
            exprs: "IPAR = SOL*FPAR*0.5"
        - epsilon:
            desc: "PAR use efficiency ($\\epsilon(x,t)$). Function that depends on effects of temperature and water stress"
#            exprs: epsilon is function of other functions that depend on soil module (see pages 6-10 of Potter1993GlobalBiogeochemCy)
            type: variable
            unit: km^2
        - NPP:
            desc: New production of plant biomass (NPP(x,t)) at a grid cell ($x$) in month $t$
            exprs: "NPP = IPAR * epsilon"
            type: variable
            key: NPP
    - allocation_coefficients:
        - alpha_f:
            desc: Proportional allocation constant of available carbon allocated to foliage
            type: parameter
            key: "part_foliage"
        - alpha_r:
            desc: Proportional allocation constant of available carbon allocated to roots
            type: parameter
            key: "part_roots"
        - alpha_w:
            desc: Proportional allocation constant of available carbon allocated to wood
            type: parameter
            key: "part_wood"
    - cycling_rates:
        - tau_f: 
            desc: Residence time of carbon in foliage 
            unit: years
            type: parameter
            key: "cyc_foliage"
        - tau_r:
            desc: Residence time of carbon in roots
            unit: years
            type: parameter
            key: "cyc_roots"
        - tau_w:
            desc: Residence time of carbon in wood
            unit: years
            type: parameter
            key: "cyc_wood"
    - components:
        # you are required to provide at least expressions for f u x and A
        # you are allowed to use as many helper expressions as you want to arrive there
        # e.g.
        # p= x**2 # allowed just for conviniece
        # f =p**2.. #required
        - x: 
            key: state_vector 
            exprs: "x=Matrix(3,1,[C_f, C_r, C_w])"
            desc: vector of states for vegetation
        - u: 
            key: scalar_func_phot    
            exprs: "u=NPP"
            desc: scalar function of photosynthetic inputs
        - b: 
            key: part_coeff    
            exprs: "b=Matrix(3,1,[alpha_f, alpha_r, alpha_w])"
            desc: vector of partitioning coefficients of photosynthetically fixed carbon
        - A: 
            key: cyc_matrix    
            exprs: "A=diag(-tau_f, -tau_r, -tau_w)"
            desc: matrix of turnover (cycling) rates 
        - f_v: 
            key: state_vector_derivative  
            exprs: "f_v = u*b + A*x"
            desc: the righthandside of the ode

model_run_data:
    parameter_sets:
        - "Original dataset of the publication":
            values: {alpha_f: 'Rational(1,3)',alpha_r: 'Rational(1,3)',alpha_w: 'Rational(1,3)'}
# epsilon varies from 1.1 - 1.4 gC*MJ^{-1}PAR in crop ecosystems.
            doi: 10.1029/93GB02725
        - "Tundra":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "High-latitude forest":
            values: {alpha_f: 0.30, alpha_r: 0.25, alpha_w: 0.45, tau_f: 1, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "Boreal coniferous forest":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 2.5, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "Temperate grassland":
            values: {alpha_f: 0.45, alpha_r: 0.55, tau_f: 1.5, tau_r: 5}
            doi: 10.2307/1313568
        - "Mixed coniferous forest":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 3, tau_w: 40}
            doi: 10.2307/1313568
        - "Temperate deciduous forest":
            values: {alpha_f: 0.30, alpha_r: 0.25, alpha_w: 0.45, tau_f: 1, tau_r: 3, tau_w: 40}
            doi: 10.2307/1313568
        - "Desert and bare ground":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "Semi-arid shrubland":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 3, tau_w: 50}
            doi: 10.2307/1313568
        - "Savanna and woody grassland":
            values: {alpha_f: 0.30, alpha_r: 0.25, alpha_w: 0.45, tau_f: 1, tau_r: 5, tau_w: 25}
            doi: 10.2307/1313568
        - "Tropical evergreen rain forest":
            values: {alpha_f: 0.25, alpha_r: 0.25, alpha_w: 0.5, tau_f: 1.5, tau_r: 2, tau_w: 25}
            doi: 10.2307/1313568
    """
    )
    return yaml_str_list






def example_yaml_string_list():
    yaml_str_list=[]
    yaml_str_list.append("""\
              citationKey: Hilbert1991AnnBot
              name: 
              version: 
              model-id: V0001
              entryAuthor: "Verónika Ceballos-Núñez"
              entryAuthorOrcid: 0000-0002-0046-1160
              entryCreationDate: _ecd_
              lastModification: _lm_
              modApproach: process based
              doi:
              abstract: "A model is developed that considers the allocation of carbon and nitrogen substrates to a protein compartment in the shoots, shoot structural components, and root biomass. Inclusion of a shoot-protein compartment allows variation in shoot-specific activity to be modelled as a function of leaf nitrogen concentration. Allocation to the biomass compartments is controlled by two partitioning variables that are defined by explicitly using the balanced activity hypothesis. The model produces balanced activity where the shoot-specific activity, as well as root and shoot biomass, vary in response to the above-ground (light and CO$_2$) and below-ground (nitrogen) environments. The predicted patterns of both root: shoot ratio and leaf nitrogen concentration in response to environmental resource availability are qualitatively consistent with general trends observed in plants."
              bibtex: "@article{Hilbert1991Annals_of_Botany,
                          Author = {HILBERT, DAVID W. and REYNOLDS, JAMES F.},
                          Journal = {Annals of Botany},
                          Number = {5},
                          Pages = {417-425},
                          Title = {A Model Allocating Growth Among Leaf Proteins, Shoot Structure, and Root Biomass to Produce Balanced Activity},
                          Url = {http://aob.oxfordjournals.org/content/68/5/417.abstract},
                          Volume = {68},
                          Year = {1991}
                      }"
              #t = # units: days, years for allocation
              model:
                  - state_variables[State Variables (alternative title used here)]:
                      - W_p:
                          desc: Mass of leaf proteins
                      - W_s:
                          desc: Mass of leaf structural components
                      - W_r:
                          desc: Mass of roots
                      - W_C:
                          desc: Substrate carbon
                      - W_N:
                          desc: Substrate nitrogen
                  - additional_variables:
                      - W_g:
                          desc: Plant biomass
                          exprs: "W_g = W_p + W_s + W_r"
                      - kappa:
                          desc: Growth rate coefficient
                      - sigma_c:
                          desc: Photosynthetic rate per unit leaf
                      - sigma_r:
                          desc: Specific root activity 
                          unit: [g N (g root)^-1 d^-1]
                      - h_max:
                          desc: Leaf max. thickness
                          unit: [m]
                      - h_half:
                          desc: h$_0.5$% leaf half thickness
                      - I:
                          desc: Photon flux density
                          unit: [micro mol m^-2s^-1]
                      - rho:
                          desc: Leaf density
                      - f_C:
                          desc: Proportion of carbon
                      - f_N:
                          desc: Proportion of nitrogen
                      - Beta:
                          desc: Target whole plant nitrogen:carbon ratio
                      - f_cp:
                          desc: Proportion of carbon in leaf proteins
                      - f_cs:
                          desc: Proportion of carbon in leaf structural components
                      - f_cr:
                          desc: Proportion of carbon in roots
                      - f_np:
                          desc: Proportion of nitrogen in leaf proteins
                      - f_ns:
                          desc: Proportion of nitrogen in leaf structural components
                      - f_nr:
                          desc: Proportion of nitrogen in roots
                      - C:
                          desc: Substrate carbon concentration
                          exprs: "C = W_C/W_g"
                      - N:
                          desc: Substrate nitrogen concentration
                          exprs: "N = W_N/W_g"
                      - h:
                          desc:
                          exprs: "h = h_max*I/(h_half+I)"
                      - A:
                          desc: Area
                          exprs: "A = W_s/rho*h"
                      - P:
                          desc:
                          exprs: "P = f_C*sigma_r*W_r/f_N*sigma_c*A"
                      - Q:
                          desc:
                          exprs: "Q = f_N/(Beta*f_C)"
                  
                  - allocation_coefficients:
                      - lambda_p:
                          desc:
                          unit: 
                          exprs: "lambda_p = P/(1+P+Q)"
                      - lambda_s:
                          desc:
                          unit: 
                          exprs: "lambda_s = Q/(1+P+Q)"
                      - lambda_r:
                          desc:
                          unit:
                          exprs: "lambda_r = 1/(1+P+Q)"
                  - components:
                      - f_v: 
                          exprs: "fv = Matrix(5,1,[kappa*C*N*lambda_p*W_p, kappa*C*N*lambda_s*W_s, kappa*C*N*lambda_r*W_r, sigma_c*A-f_cp*kappa*C*N*lambda_p*W_p-f_cs*kappa*C*N*lambda_s*W_s-f_cr*kappa*C*N*lambda_r*W_r, sigma_r*W_r-f_np*kappa*C*N*lambda_p*W_p-f_ns*kappa*C*N*lambda_s*W_s-f_nr*kappa*C*N*lambda_r*W_r])"
             """)

    yaml_str_list.append("""\
               citationKey: Scheiter2009GlobalChangeBiol
               name: aDGVM
               model-id: V0001
               version: 1
               entryAuthor: "Verónika Ceballos-Núñez"
               entryAuthorOrcid: 0000-0002-0046-1160
               entryCreationDate: _ecd_
               lastModification: _lm_
               modApproach: individuals based
               doi: 10.1111/j.1365-2486.2008.01838.x
               #t = # units: days
               model:
                   - state_variables:
                       - B_L:
                           desc: Carbon in foliage
                       - B_R:
                           desc: Carbon in roots
                       - B_S:
                           desc: Carbon in woody tissue
                   - additional_variables:
                       - Q_i:
                           desc: describes light availability
                       - G_i:
                           desc: describes water availability
                       - C_i:
                           desc: deviance of leaf biomass from $a_{0L}$
                           exprs: 
                               - "C_i = (B_L/(a_0L*(B_R+B_S+B_L)))"    
                   - photosynthetic_parameters:
                       - C_delta:
                           desc:  Net carbon gain
                           exprs: 
                               -  "C_delta = A_CC*C-R_g"
                               -  "C_delta = A_CC*2"
                       - A_CC:
                           desc:  Leaf level photosynthetic rate
                       - R_g:
                           desc: Growth respiration # PAR use efficiency
                       - C:
                           desc:  Canopy area of the plant
                   - allocation_coefficients:
                   #CAUTION: Partitions in this work were the following: Leaves, Roots (including woody roots, not only fine roots?) and Stems
                       - a_0R:
                           desc: fraction of carbon allocated to roots when resources are not limiting
                       - a_0S:
                           desc: fraction of carbon allocated to stems when resources are not limiting
                       - a_0L:
                           desc: fraction of carbon allocated to leaves when resources are not limiting
                       - a_L:
                           exprs: 
                               - "a_L = ((1-C_i)/(3+a_0R+a_0S-Q_i-G_i-C_i))" 
                       - a_R:
                           exprs: 
                               - "a_R = ((1+a_0R-G_i)/(3+a_0R+a_0S-Q_i-G_i-C_i))" 
                       - a_S:
                           exprs: 
                               - "a_S = ((1+a_0S-Q_i)/(3+a_0R+a_0S-Q_i-G_i-C_i))" 
                   - cycling_rates:
                       - gamma_f:
                           desc:
                           unit: 
                       - gamma_r:
                           desc:
                           unit: 
                       - gamma_w:
                           desc:
                   - components:
                       - x: 
                           exprs: "x = Matrix(3,1,[B_L, B_R, B_S])"
                       - u:   
                           exprs: "u = C_delta"
                       - b:   
                           exprs: "b = Matrix(3,1,[a_L, a_R, a_S])"
                       - A:   
                           exprs: "A=diag(-gamma_f, -gamma_r, -gamma_w)"
                       - f_v: 
                           exprs: "fv = u*b + A*x"
                           desc: the righthandside of the ode
               
                """)

    yaml_str_list.append("""\
            # vim:set ff: unix expandtab ts: 4 sw: 4: 
            citationKey: King1993TreePhysiol
            name: 
            model-id: V0001
            version: 1
            entryAuthor: "Verónika Ceballos-Núñez"
            entryAuthorOrcid: 0000-0002-0046-1160
            entryCreationDate: _ecd_
            lastModification: _lm_
            modApproach: process based
            doi: 10.1093/treephys/12.2.119
            #t = # units: days, years for allocation
            model:
                - state_variables:
                    - F:
                        desc: Carbon in foliage
                    - R:
                        desc: Carbon in roots
                    - W:
                        desc: Carbon in woody tissue
                
                - photosynthetic_parameters:
                    - Phi:
                        desc:  Annual photosynthetically active radiation (PAR)
                        unit: [M J m^-2 year^-1]
                    - epsilon:
                        desc:  Light utilization coefficient
                        unit: [Kg M J^-1]
                    - G:
                        desc:  Rate of biomass production per unit ground area
                        unit: [Kg m^-2 year-1]
                        exprs: "G=Phi*epsilon"
                - allocation_coefficients:
                    - eta_f:
                        exprs: "eta_f=Piecewise((Piecewise((3,Phi<5),(6,True)),epsilon<=0),(10,epsilon>0))"
                        desc:
                        unit: 
                    - eta_r:
                        desc:
                        unit: 
                    - eta_w:
                        desc:
                        unit:
                        exprs: "eta_w=1-eta_f-eta_r"
                - cycling_rates:
                    - gamma_f:
                        desc:
                        unit: 
                    - gamma_r:
                        desc:
                        unit: 
                    - gamma_w:
                        desc:
                        unit:
                - components:
                    - x: 
                        exprs: "x=Matrix(3,1,[F, R, W])"
                    - u:   
                        exprs: "u=G"
                    - b:   
                        exprs: "b=Matrix(3,1,[eta_f, eta_r, eta_w])"
                    - A:   
                        exprs: "A=diag(-gamma_f, -gamma_r, -gamma_w)"
                    - f_v: 
                        exprs: "fv = u*b + A*x"
                        desc: the righthandside of the ode
                
            """)

    return yaml_str_list











###########################################













soil_yaml_str = """\
              # vim:set ff: unix expandtab ts: 4 sw: 4: 
              citationKey: Hilbert1991AnnBot
              name: 
              version: 
              entryAuthor: "Verónika Ceballos-Núñez"
              entryAuthorOrcid: 0000-0002-0046-1160
              entryCreationDate: _ecd_
              lastModification: _lm_
              modApproach: process based
              doi:
              abstract: "A model is developed that considers the allocation of carbon and nitrogen substrates to a protein compartment in the shoots, shoot structural components, and root biomass. Inclusion of a shoot-protein compartment allows variation in shoot-specific activity to be modelled as a function of leaf nitrogen concentration. Allocation to the biomass compartments is controlled by two partitioning variables that are defined by explicitly using the balanced activity hypothesis. The model produces balanced activity where the shoot-specific activity, as well as root and shoot biomass, vary in response to the above-ground (light and CO$_2$) and below-ground (nitrogen) environments. The predicted patterns of both root: shoot ratio and leaf nitrogen concentration in response to environmental resource availability are qualitatively consistent with general trends observed in plants."
              bibtex: "@article{Hilbert1991Annals_of_Botany,
                          Author = {HILBERT, DAVID W. and REYNOLDS, JAMES F.},
                          Journal = {Annals of Botany},
                          Number = {5},
                          Pages = {417-425},
                          Title = {A Model Allocating Growth Among Leaf Proteins, Shoot Structure, and Root Biomass to Produce Balanced Activity},
                          Url = {http://aob.oxfordjournals.org/content/68/5/417.abstract},
                          Volume = {68},
                          Year = {1991}
                      }"
              #t = # units: days, years for allocation
              model:
                  - state_variables[State Variables (alternative title used here)]:
                      - S:
                          desc: Soil carbon
                      - B:
                          desc: Microbial biomass

                  - components:
                      - f_v: 
                          exprs: "fv = Matrix(2,1,[S,B])"
                  
             """

