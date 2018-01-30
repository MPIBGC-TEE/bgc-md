# vim:set ff=unix expandtab ts=4 sw=4:
from pathlib import Path
from subprocess import call
import unittest
import datetime
from bgc_md.helpers import remove_indentation
from testinfrastructure.InDirTest import InDirTest
from bgc_md.YamlEditor import add_last_edit_date,add_edit_date


class TestYamlEditor(InDirTest):
    @unittest.skip("The test is incomplete since it does not check the writing of the yaml file in correct order, to implement this Model should get a write_yaml method")
    def test_edited(self):
        #yaml_str =remove_indentation("""\
        #    edits:
        #        - {time: !!timestamp '2001-12-15 02:59:43', user: mm}
        #""")
        yaml_str ="""\
        citationKey: Arora2005GCB 
        name: CTEM
        version: 1
        entryAuthor: "Verónika Ceballos-Núñez"
        entryAuthorOrcid: 0000-0002-0046-1160
        entryCreationDate: 21/1/2016 # changeset 3032
        entryCreationDate: _ecd_
        lastModification: _lm_
        modApproach: process based
        partitioningScheme: dynamic #if L and W change with time
        # Dynamically performs allocation on the basis of the light, water and phenological status pf the canopy.
        spaceScale: global 
        #    unit: "1°"
        timeResolution: monthly 
        doi: 10.1111/j.1365-2486.2004.00890.x
        model:
            - state_variables:
            # Live vegetation pools: 
                - C_L:
                    desc: Amount of carbon for the leaf
                    key: "foliage"
                    unit: "kgC*m^{-2}" 
                - C_S: 
                    desc: Amount of carbon for the stem
                    key: "wood"
                    unit: "kgC*m^{-2}" 
                - C_R:
                    desc: Amount of carbon for the root
                    key: "fine_roots"
                    unit: "kgC*m^{-2}" 
               # Dead carbon pools:
                - C_D:
                    desc: Amount of carbon for the litter (debris)
                    unit: "kgC*m^{-2}" 
                - C_H:
                    desc: Amount of soil carbon (humus)
                    unit: "kgC*m^{-2}" 
            
            - respiration_fluxes:
                - R_gL:
                    desc: Growth respiration flux for the leaves
                    type: parameter
                - R_mL:
                    desc: Maintenance respiration flux for the leaves
                    type: parameter
                - R_gS:
                    desc: Growth respiration flux for the stem
                    type: parameter
                - R_mS:
                    desc: Maintenance respiration flux for the stem
                    type: parameter
                - R_gR:
                    desc: Growth respiration flux for the root
                    type: parameter
                - R_mR:
                    desc: Maintenance respiration flux for the root    
                    type: parameter
                - R_hD:
                    desc: Heterotrophic respiration from litter (debris)
                    type: parameter
                - R_hH:
                    desc: Heterotrophic respiration from soil carbon (humus)
                    type: parameter
        
            - photosynthetic_parameters:
                - G:
                    desc: Carbon gain via photosynthesis (Gross Primary Productivity, GPP)
                    type: variable
                    key: GPP
                - N:
                    desc: Net primary Productivity (NPP)
                    type: variable
                    key: NPP
                    exprs: "N=G-(R_gL+R_gS+R_gR)-(R_mL+R_mS+R_mR)"
                - LAI:
                    desc: Leaf Area Index
                    type: parameter
                - k_n:
                    desc: PFT-dependent light extinction coefficient
                    type: parameter
                - L:
                    desc: Light availability (scalar index between 0 and 1)
                    type: variable
                    #exprs: "L=(Piecewise(((exp(-k_n*LAI)),FOR TREES AND CROPS),((Max(0,1-(LAI/4.5))),FOR GRASSES)))"
                    exprs: "L=(exp(-k_n*LAI))"
        
            - water_availability:
            # Measured by a linear scalar index (varies from 0 to 1)
                - theta_i:
                    desc: Volumetric soil moisture content
                    type: variable
                - theta_field:
                    desc: Field capacity
                    type: parameter
                - theta_wilt:
                    desc: Wilting point
                    type: parameter
                - W_i:
                    desc: Availability of water in soil layer i. Weighted by the fraction of roots present in each soil layer
                    type: variable
                    exprs: "W_i=(Max(0,(Min(1,((theta_i-theta_wilt)/(theta_field-theta_wilt))))))"
                - W:
                    desc: Averaged soil water availability index
                    type: variable
        
            - allocation_fractions:
                - epsilon_L:
                    desc: PFT-dependent parameter for leaf
                    type: parameter
                - epsilon_S:
                    desc: PFT-dependent parameter for stem
                    type: parameter
                - epsilon_R:
                    desc: PFT-dependent parameter for root
                    type: parameter
                    exprs: "epsilon_R=1-epsilon_L-epsilon_S"
                - omega:
                    desc: PFT-dependent parameter
                    type: parameter
                - a_S:
                    desc: Stem allocation fraction
                    type: variable
                    # vary between 0 and 1
                    exprs: "a_S=((epsilon_S+(omega*(1-L)))/(1+(omega*(2-L-W))))"
                - a_R:
                    desc: Root allocation fration
                    type: variable
                    # vary between 0 and 1
                    exprs: "a_R=((epsilon_R+(omega*(1-W)))/(1+(omega*(2-L-W))))"
                    #exprs: "a_R=((epsilon_R+(omega*(1-W)))/(1+(omega*(1-L-W))))" # For grasses
                - a_L:
                    desc: Leaf allocation fraction
                    type: variable
                    key: "part_foliage"
                    #exprs: "a_L=(epsilon_L/(1+(omega*(2-L-W))))"
                    exprs: "a_L=1-a_S-a_R"
                    #exprs: "a_L=((epsilon_L+(omega*L))/(1+(omega*(1-L-W))))" # For grasses
        
            - allocation_coefficients:
                - A_S:
                    desc: Amount of carbon allocated to the stem
                    type: variable
                    key: "part_wood"
                    exprs: "A_S=(Piecewise((a_S*G,N<0),(a_S*N+R_gS+R_mS,N>0)))"
                - A_R:
                    desc: Amount of carbon allocated to the root 
                    type: variable
                    key: "part_roots"
                    exprs: "A_R=(Piecewise((a_R*G,N<0),(a_R*N+R_gR+R_mR,N>=0)))"
        
            - temperature:
                - T_air:
                    desc: Temperature of the air
                    type: variable
                    key: "air_temperature"
                    unit: "°C"
                - T_cold:
                    desc: Cold temperature threshold for a PFT below which leaf loss begins to occur
                    type: parameter
                    unit: "°C"
                - b_T:
                    desc: "Parameter that describes sensitivity of leaf loss to temp. below the T$_{cold}$"
                    type: parameter
                - beta_T:
                    desc: Temperature measure (varies between 0 and 1)
                    type: variable
                    exprs: "beta_T=(Piecewise((1,T_air>= T_cold),(Piecewise((((T_air-T_cold-5)/5),T_air>(T_cold-5)),(0,T_air<=(T_cold-5))),T_cold>T_air)))"
            - cycling_rates_:
                - gamma_N: 
                    desc: Loss rate (normal turnover)
                    type: parameter 
                    unit: day^{-1} 
                - gamma_W: 
                    desc: Loss rate under drought stress
                    type: parameter 
                    unit: day^{-1} 
                - gamma_Tmax:
                    desc: Maximum loss rate of specified PFT
                    type: parameter 
                - gamma_T: 
                    desc: Loss rate under cold stress
                    type: variable
                    unit: day^{-1} 
                    exprs: "gamma_T=gamma_Tmax*(1-beta_T)**b_T"
                - gamma_S: 
                    desc: Stem turnover rate 
                    type: parameter 
                    key: "cyc_wood"
                    unit: years 
                - gamma_R: 
                    desc: Root turnover rate
                    type: parameter 
                    key: "cyc_roots"
                    unit: years 
        
            - litter_fluxes:
                - D_L:
                    desc: Litter loss from the leaves
                    type: variable
                    exprs: "D_L=(gamma_N+gamma_W+gamma_T)*C_L"
                - D_S: 
                    desc: Litter loss from the stem
                    type: variable
                - D_R:
                    desc: Litter loss from the root
                    type: variable
                    
                - C_D_H:
                    desc: Transfer of humidified litter to the soil carbon pool. Symbolized as C$_D->H$ in the original publication. #I had to change it since this formulation has a conflict when trying to evaluate.
                    type: variable
        
            - components:
                - f_v: 
                    exprs: "fv = Matrix(5,1,[G-A_R-A_S-R_gL-R_mL-D_L, A_S-R_gS-R_mS-D_S, A_R-R_gR-R_mR-D_R, D_L+D_S+D_R-R_hD-C_D_H, C_D_H-R_hH])"
                    desc: the righthandside of the ode
        
            - parameter_sets:
                - "{k_n: 0.5,omega: 0.8,epsilon_L: 0.35,epsilon_S: 0.1,epsilon_R: 0.55}":
                    desc: Eastern US and Germany, cold broadleaf deciduous
        edits:
        -  time: 2001-12-15 02:59:43 
           user: mm
        
        """
        fn="test.yaml"
        p=Path(fn)
        with p.open("w") as f:
            f.write(yaml_str) 
        
        #simulate opening with vim
        test_time=datetime.datetime(2001,12,15,13,45)
        add_edit_date(p,test_time)
        
        
        #assertions
        with p.open("r") as f:
            yaml_str_after=f.read()
        print(yaml_str_after)

        #yaml_str_ref = remove_indentation("""\
        #    edits:
        #        - {time: !!timestamp '2001-12-15 02:59:43', user: mm}
        #        - {time: !!timestamp '2001-12-15 13:45:00', user: mm}
        #""")
        
        yaml_str_ref =remove_indentation("""\
            edits:
            - time: 2001-12-15 02:59:43
              user: mm
            - time: 2001-12-15 13:45:00
              user: mm
        """)
        #self.assertEqual(yaml_str_after,yaml_str_ref)


if __name__=="__main__":
    unittest.main()
