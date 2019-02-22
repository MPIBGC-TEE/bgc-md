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
  
