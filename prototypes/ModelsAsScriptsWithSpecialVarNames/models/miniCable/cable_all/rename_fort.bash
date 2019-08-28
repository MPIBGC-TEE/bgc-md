OutPath=/home/599/czl599/workdir/cable2.0-trunk-run-MM/out/Tumbarumba
RepPath=/home/599/czl599/workdir/pseudoCable_MM/bgc-md/prototypes/ModelsAsScriptsWithSpecialVarNames/models/pseudoCable/Tumbarumba/
##time dependent variable
if [ -f $OutPath/fort.401 ];then
   mv $OutPath/fort.401 $OutPath/b_tran.txt
   cp -p $OutPath/b_tran.txt $RepPath/T_dependent 
fi
if [ -f $OutPath/fort.402 ];then
   mv $OutPath/fort.402 $OutPath/T_air.txt
   cp -p $OutPath/T_air.txt $RepPath/T_dependent
fi
if [ -f $OutPath/fort.403 ];then
   mv $OutPath/fort.403 $OutPath/T_soil.txt
   cp -p $OutPath/T_soil.txt $RepPath/T_dependent
fi
if [ -f $OutPath/fort.404 ];then
   mv $OutPath/fort.404 $OutPath/ms.txt
   cp -p $OutPath/ms.txt $RepPath/T_dependent
fi
if [ -f $OutPath/fort.405 ];then
   mv $OutPath/fort.405 $OutPath/xk_n_limit.txt
   cp -p $OutPath/xk_n_limit.txt $RepPath/T_dependent
fi
if [ -f $OutPath/fort.406 ];then
   mv $OutPath/fort.406 $OutPath/NPP.txt
   cp -p $OutPath/NPP.txt $RepPath/T_dependent
fi
if [ -f $OutPath/fort.407 ];then
   mv $OutPath/fort.407 $OutPath/phase.txt
   cp -p $OutPath/phase.txt $RepPath/T_dependent
fi
if [ -f $OutPath/fort.408 ];then
   mv $OutPath/fort.408 $OutPath/r_leaf.txt
   cp -p $OutPath/r_leaf.txt $RepPath/T_dependent
fi
if [ -f $OutPath/fort.409 ];then
   mv $OutPath/fort.409 $OutPath/r_wood.txt
   cp -p $OutPath/r_wood.txt $RepPath/T_dependent
fi
if [ -f $OutPath/fort.410 ];then
   mv $OutPath/fort.410 $OutPath/r_froot.txt
   cp -p $OutPath/r_froot.txt $RepPath/T_dependent
fi

##time independent parameters
if [ -f $OutPath/fort.301 ];then
   mv $OutPath/fort.301 $OutPath/soilscalar.txt
   cp -p $OutPath/soilscalar.txt $RepPath/T_independent
fi
if [ -f $OutPath/fort.302 ];then
   mv $OutPath/fort.302 $OutPath/vegpara.txt
   cp -p $OutPath/vegpara.txt $RepPath/T_independent
fi
if [ -f $OutPath/fort.303 ];then
   mv $OutPath/fort.303 $OutPath/k_base.txt
   cp -p $OutPath/k_base.txt $RepPath/T_independent
fi

##CABLE results
 #allocation fraction
if [ -f $OutPath/fort.401 ];then
   mv $OutPath/fort.510 $OutPath/fracNPPtoLeaf.txt
   cp -p $OutPath/fracNPPtoLeaf.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.401 ];then
   mv $OutPath/fort.511 $OutPath/fracNPPtoWood.txt
   cp -p $OutPath/fracNPPtoWood.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.401 ];then
   mv $OutPath/fort.512 $OutPath/fracNPPtoFroot.txt
   cp -p $OutPath/fracNPPtoFroot.txt $RepPath/CABLE_results
fi

 #turnover rate
 # this informations (Some of the ks (or at least the baseline part) should now also be in the output form cable_transit_time runs but this is not sure)
if [ -f $OutPath/fort.513 ];then
   mv $OutPath/fort.513 $OutPath/KLeaf.txt
   cp -p $OutPath/KLeaf.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.514 ];then
   mv $OutPath/fort.514 $OutPath/KWood.txt
   cp -p $OutPath/KWood.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.515 ];then
   mv $OutPath/fort.515 $OutPath/KFroot.txt
   cp -p $OutPath/KFroot.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.523 ];then
   mv $OutPath/fort.523 $OutPath/KMetb.txt
   cp -p $OutPath/KMetb.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.524 ];then
   mv $OutPath/fort.524 $OutPath/KStru.txt
   cp -p $OutPath/KStru.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.525 ];then
   mv $OutPath/fort.525 $OutPath/KCWD.txt
   cp -p $OutPath/KCWD.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.533 ];then
   mv $OutPath/fort.533 $OutPath/KFast.txt
   cp -p $OutPath/KFast.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.534 ];then
   mv $OutPath/fort.534 $OutPath/KSlow.txt
   cp -p $OutPath/KSlow.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.535 ];then
   mv $OutPath/fort.535 $OutPath/KPass.txt
   cp -p $OutPath/KPass.txt $RepPath/CABLE_results
fi

 #C Pool size
if [ -f $OutPath/fort.516 ];then
   mv $OutPath/fort.516 $OutPath/CLeaf.txt
   cp -p $OutPath/CLeaf.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.517 ];then
   mv $OutPath/fort.517 $OutPath/CWood.txt
   cp -p $OutPath/CWood.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.518 ];then
   mv $OutPath/fort.518 $OutPath/CFroot.txt
   cp -p $OutPath/CFroot.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.526 ];then
   mv $OutPath/fort.526 $OutPath/CMetb.txt
   cp -p $OutPath/CMetb.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.527 ];then
   mv $OutPath/fort.527 $OutPath/CStru.txt
   cp -p $OutPath/CStru.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.528 ];then
   mv $OutPath/fort.528 $OutPath/CCWD.txt
   cp -p $OutPath/CCWD.txt  $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.536 ];then
   mv $OutPath/fort.536 $OutPath/CFast.txt
   cp -p $OutPath/CFast.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.537 ];then
   mv $OutPath/fort.537 $OutPath/CSlow.txt
   cp -p $OutPath/CSlow.txt $RepPath/CABLE_results
fi
if [ -f $OutPath/fort.538 ];then
   mv $OutPath/fort.538 $OutPath/CPass.txt
   cp -p $OutPath/CPass.txt $RepPath/CABLE_results
fi
