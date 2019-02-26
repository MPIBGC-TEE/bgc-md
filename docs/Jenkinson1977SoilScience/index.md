---
title: 'Report of the model: RothC-26.3, version: 1'
---
  
  
---
title: 'Report of the model: RothC-26.3, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Holger Metzler (Orcid ID: 0000-0002-8239-1601) on 10/03/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers soil organic matter decomposition. It was originally described by @Jenkinson1977SoilScience.  
  
  
  
### Keywords  
  
differential equations, linear, time variant
  
  
### Principles  
  
mass balance, substrate dependence of decomposition, heterogeneity of speed of decay, internal transformations of organic matter, environmental variability effects
  
  
### Space Scale  
  
plot, field, catchment, regional, national, global
  
  
### Available parameter values  
  
  
  
Abbreviation|Description|Source  
:-----|:-----|:-----  
Set1|original values without effects of temperature and soil moisture|@Coleman1996  
  Table:  Information on given parameter sets  
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$C_{1}$|decomposable plant material pool (DPM)|$t C\cdot ha^{-1}$  
$C_{2}$|resistant plant material pool (RPM)|$t C\cdot ha^{-1}$  
$C_{3}$|microbial biomass pool (BIO)|$t C\cdot ha^{-1}$  
$C_{4}$|humified organic matter pool (HUM)|$t C\cdot ha^{-1}$  
$C_{5}$|inert organic matter pool (IOM)|$t C\cdot ha^{-1}$  
  Table: state_variables  
The model section in the yaml file has no subsection: parameters.The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$C$|carbon content|$C=\left[\begin{matrix}C_{1}\\C_{2}\\C_{3}\\C_{4}\\C_{5}\end{matrix}\right]$  
$I$|input vector|$I=\left[\begin{matrix}J\cdot\gamma\\J\cdot\left(-\gamma + 1\right)\\0\\0\\0\end{matrix}\right]$  
$\xi$|environmental effects multiplier|$\xi=f_{T}\cdot f_{W}$  
$A$|decomposition operator|$A=\left[\begin{matrix}- k_{1} & 0 & 0 & 0 & 0\\0 & - k_{2} & 0 & 0 & 0\\a\cdot k_{1} & a\cdot k_{2} & a\cdot k_{3} - k_{3} & a\cdot k_{4} & 0\\b\cdot k_{1} & b\cdot k_{2} & b\cdot k_{3} & b\cdot k_{4} - k_{4} & 0\\0 & 0 & 0 & 0 & 0\end{matrix}\right]$  
$f_{s}$|the right hand side of the ode|$f_{s}=\xi A C + I$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{1}: \frac{DR\cdot J}{DR + 1}$  
$C_{2}: J\cdot\left(-\frac{DR}{DR + 1} + 1\right)$  

  
  
#### Output fluxes  
  
$C_{1}: \frac{C_{1}\cdot f_{T}\cdot f_{W}\cdot k_{1}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}\cdot\left(3.0895\cdot e^{0.0786\cdot pClay} + 2.672\right)$  
$C_{2}: \frac{C_{2}\cdot f_{T}\cdot f_{W}\cdot k_{2}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}\cdot\left(3.0895\cdot e^{0.0786\cdot pClay} + 2.672\right)$  
$C_{3}: \frac{1.0\cdot C_{3}\cdot f_{T}\cdot f_{W}\cdot k_{3}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}\cdot\left(3.0895\cdot e^{0.0786\cdot pClay} + 2.672\right)$  
$C_{4}: \frac{1.0\cdot C_{4}\cdot f_{T}\cdot f_{W}\cdot k_{4}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}\cdot\left(3.0895\cdot e^{0.0786\cdot pClay} + 2.672\right)$  

  
  
#### Internal fluxes  
  
$C_{1} \rightarrow C_{3}: \frac{0.46\cdot C_{1}\cdot f_{T}\cdot f_{W}\cdot k_{1}\cdot e^{0.0786\cdot pClay}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}$  
$C_{1} \rightarrow C_{4}: \frac{0.54\cdot C_{1}\cdot f_{T}\cdot f_{W}\cdot k_{1}\cdot e^{0.0786\cdot pClay}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}$  
$C_{2} \rightarrow C_{3}: \frac{0.46\cdot C_{2}\cdot f_{T}\cdot f_{W}\cdot k_{2}\cdot e^{0.0786\cdot pClay}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}$  
$C_{2} \rightarrow C_{4}: \frac{0.54\cdot C_{2}\cdot f_{T}\cdot f_{W}\cdot k_{2}\cdot e^{0.0786\cdot pClay}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}$  
$C_{3} \rightarrow C_{4}: \frac{0.54\cdot C_{3}\cdot f_{T}\cdot f_{W}\cdot k_{3}\cdot e^{0.0786\cdot pClay}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}$  
$C_{4} \rightarrow C_{3}: \frac{0.46\cdot C_{4}\cdot f_{T}\cdot f_{W}\cdot k_{4}\cdot e^{0.0786\cdot pClay}}{4.0895\cdot e^{0.0786\cdot pClay} + 2.672}$  
  
  
  
  
## Model simulations  
  
  
  
  
  
## Phaseplane plots  
  
  
  
  
  
## Fluxes  
  
  
  
## Steady state formulas  
  
$C_1 = \frac{DR\cdot J}{f_{T}\cdot f_{W}\cdot k_{1}\cdot\left(DR + 1.0\right)}$  
  
  
  
$C_2 = \frac{J}{f_{T}\cdot f_{W}\cdot k_{2}\cdot\left(DR + 1.0\right)}$  
  
  
  
$C_3 = \frac{5.50898203592814\cdot J\cdot\left(8.27935952684223\cdot 10^{55}\cdot e^{0.0786\cdot pClay} + 1.87222904569844\cdot 10^{57}\cdot e^{0.1572\cdot pClay} + 1.97551916500331\cdot 10^{58}\cdot e^{0.2358\cdot pClay} + 1.29026883354201\cdot 10^{59}\cdot e^{0.3144\cdot pClay} + 5.83351513562129\cdot 10^{59}\cdot e^{0.393\cdot pClay} + 1.93389656805942\cdot 10^{60}\cdot e^{0.4716\cdot pClay} + 4.85638310836312\cdot 10^{60}\cdot e^{0.5502\cdot pClay} + 9.40672416237321\cdot 10^{60}\cdot e^{0.6288\cdot pClay} + 1.41699653217698\cdot 10^{61}\cdot e^{0.7074\cdot pClay} + 1.65998203700997\cdot 10^{61}\cdot e^{0.786\cdot pClay} + 1.49996699688935\cdot 10^{61}\cdot e^{0.8646\cdot pClay} + 1.02667590856449\cdot 10^{61}\cdot e^{0.9432\cdot pClay} + 5.1526782641926\cdot 10^{60}\cdot e^{1.0218\cdot pClay} + 1.79010152464143\cdot 10^{60}\cdot e^{1.1004\cdot pClay} + 3.84938573978872\cdot 10^{59}\cdot e^{1.179\cdot pClay} + 3.86239155892181\cdot 10^{58}\cdot e^{1.2576\cdot pClay}\right)}{f_{T}\cdot f_{W}\cdot k_{3}\cdot\left(6.29746924872818\cdot 10^{58}\cdot e^{0.0786\cdot pClay} + 7.01438607491901\cdot 10^{59}\cdot e^{0.1572\cdot pClay} + 4.85980235838567\cdot 10^{60}\cdot e^{0.2358\cdot pClay} + 2.34412431180936\cdot 10^{61}\cdot e^{0.3144\cdot pClay} + 8.34686961797004\cdot 10^{61}\cdot e^{0.393\cdot pClay} + 2.26958432485819\cdot 10^{62}\cdot e^{0.4716\cdot pClay} + 4.80701348205378\cdot 10^{62}\cdot e^{0.5502\cdot pClay} + 8.01487684304444\cdot 10^{62}\cdot e^{0.6288\cdot pClay} + 1.05548296874867\cdot 10^{63}\cdot e^{0.7074\cdot pClay} + 1.09418279269828\cdot 10^{63}\cdot e^{0.786\cdot pClay} + 8.83524079589696\cdot 10^{62}\cdot e^{0.8646\cdot pClay} + 5.44755790623023\cdot 10^{62}\cdot e^{0.9432\cdot pClay} + 2.47932344563652\cdot 10^{62}\cdot e^{1.0218\cdot pClay} + 7.85517907790568\cdot 10^{61}\cdot e^{1.1004\cdot pClay} + 1.54786925360733\cdot 10^{61}\cdot e^{1.179\cdot pClay} + 1.42908487680107\cdot 10^{60}\cdot e^{1.2576\cdot pClay} + 2.64939504858951\cdot 10^{57}\right)}$  
  
  
  
$C_4 = \frac{6.46706586826347\cdot J\cdot\left(1.89961020789331\cdot 10^{37}\cdot e^{0.0786\cdot pClay} + 2.8746533965631\cdot 10^{38}\cdot e^{0.1572\cdot pClay} + 1.95732429065687\cdot 10^{39}\cdot e^{0.2358\cdot pClay} + 7.89657547413316\cdot 10^{39}\cdot e^{0.3144\cdot pClay} + 2.09038005944651\cdot 10^{40}\cdot e^{0.393\cdot pClay} + 3.79397672088011\cdot 10^{40}\cdot e^{0.4716\cdot pClay} + 4.78123268745007\cdot 10^{40}\cdot e^{0.5502\cdot pClay} + 4.13109421978841\cdot 10^{40}\cdot e^{0.6288\cdot pClay} + 2.34204313247406\cdot 10^{40}\cdot e^{0.7074\cdot pClay} + 7.86709759349002\cdot 10^{39}\cdot e^{0.786\cdot pClay} + 1.18899128159813\cdot 10^{39}\cdot e^{0.8646\cdot pClay}\right)}{f_{T}\cdot f_{W}\cdot k_{4}\cdot\left(9.90174664592246\cdot 10^{39}\cdot e^{0.0786\cdot pClay} + 7.32705948683033\cdot 10^{40}\cdot e^{0.1572\cdot pClay} + 3.25111413926565\cdot 10^{41}\cdot e^{0.2358\cdot pClay} + 9.6109491156581\cdot 10^{41}\cdot e^{0.3144\cdot pClay} + 1.98751317267684\cdot 10^{42}\cdot e^{0.393\cdot pClay} + 2.93376584670966\cdot 10^{42}\cdot e^{0.4716\cdot pClay} + 3.09100624468882\cdot 10^{42}\cdot e^{0.5502\cdot pClay} + 2.27795866371341\cdot 10^{42}\cdot e^{0.6288\cdot pClay} + 1.11830308200708\cdot 10^{42}\cdot e^{0.7074\cdot pClay} + 3.29130331970271\cdot 10^{41}\cdot e^{0.786\cdot pClay} + 4.39926774191307\cdot 10^{40}\cdot e^{0.8646\cdot pClay} + 6.0787526652586\cdot 10^{38}\right)}$  
  
  
  
$C_5 = C_{5}$  
  
  
  
  
  
  
  
## Mean ages  
  
To compute the moments we need a start_age distribution.  This distribution can be chosen arbitrarily by the user or contributor of the yaml file and should in this case be defined in the model run data.  If the model run data do not contain age distributions, we can compute some distributions for special situations  
  
### Zero age for the whole initial mass  
  
We assume that the contents of all pools (as described by the start values of a model run combination are zero  
  
### Steady state start age distribution   
  
In the general non autonomous case The model can be frozen at a time t_0. The resulting model is in general autonomous but nonlinear and might have fixed points. If fixedpoints can be found we can compute the age distribution that would have developed if the system had stayed in this equilibrium for infinite time. Note that any startvalues given in the model run data section will not influence this start distribution since it will use the equilibrium values if such can be found.  
  
  
  
## Age Density Evolution  
  

    To compute the moments we need a start_age distribution.  
    This distribution can be chosen arbitrarily by the user.
    At the moment the yaml files do not contain startdistributions.
    The package CompartmentalSystems has a module "start_age_densities"  which contains functions to compute some distributions for special situations.
    In this template we use only the simplest ones.  
  
### Zero age for the whole initial mass  
  
We assume that the contents of all pools (as described by the start values of a model run combination are zero  
  
## References  
  
