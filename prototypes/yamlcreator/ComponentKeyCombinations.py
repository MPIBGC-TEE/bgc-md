VegetationModel:
    state_vector
        exprs: "x=Matrix(2,1,[C_il, C_is ])"
    state_vector_derivative 
        exprs: "f_v = u*b + A*x"
    scalar_func_phot   
        exprs: "u=2"
    part_coeff   
        exprs: "b=Matrix(2,1,[1/2*(1-sin(2*pi*t)),1/2*(1+sin(2*pi*t))])"
    cyc_matrix   
        exprs: "A=Matrix([[-1/2*C_il,0],[1/4*C_il, -1/4*(1+sin(2*pi/5*t))]])"

SoilModel:
    state_vector
            exprs: "C = Matrix(2, 1, [Y, O])"
    state_vector_derivative 
            exprs: "f_s = I + xi * T * N * C"
    input_vector
            exprs: "I = Matrix(2, 1, [i, 0])"
    trans_op
            exprs: "T = Matrix([[-1,  0],
                                [ h, -1]])"
    decomp_op_nonlin
            exprs: "N = diag(k_1, k_2)"
    env_eff_mult #optional

#first draft
#CompartmentalModel:
#    state_vector
#    state_vector_derivative 
#    input_vector
#    compartmental_matrix
            exprs: "C = Matrix(2, 1, [Y, O])"

#Fluxes
#    state_vector
#    state_vector_derivative 
#    internal_fluxes
            exprs: {(1,2):x,(2,3):x}}
#    output_fluxes
