baseQuantities=[
    ("mu_leaf","1/time","SI","Turnover rate of plant pool Leaf")
    ,("mu_root","1/time","SI","Turnover rate of plant pool Root")
    ,("mu_wood", "1/time","SI","Turnover rate of plant pool Wood")
]
derivedVariables=[
     (
         "A"
        ,"-mu_leaf*(C.e_C_leaf|C.e_C_leaf) -mu_root*(C.e_C_root|C.e_C_root) -mu_wood*(C.e_C_wood|C.e_C_wood) "
     )
    ,(
         "D"
        ,"-(C.e_sf|C.e_sf) -(C.e_ss|C.e_ss) -(C.e_sm|C.e_sm) "
     )
    ,(
         "B"
        ,"A+D"
     )
]
semanticVariables=[
     (
         "smooth_reservoir_model"
        ,"srm_from_B_u_tens(C,s,time_symbol,B,I)"
     )
]
