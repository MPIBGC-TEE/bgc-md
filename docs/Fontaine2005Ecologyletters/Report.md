---
title: 'Report of the model: The C-N model of SOM dynamics, two decomposer types (FB2005 (4)), version: SOM decomposers C limited, FOM composers N limited (case 4)'
---
  
  
---
title: 'Report of the model: The C-N model of SOM dynamics, two decomposer types (FB2005 (4)), version: SOM decomposers C limited, FOM composers N limited (case 4)'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Holger Metzler (Orcid ID: 0000-0002-8239-1601) on 22/03/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers soil organic matter decomposition. It was originally described by @Fontaine2005Ecologyletters.  
  
  
  
### Keywords  
  
differential equations, linear, time invariant, analytic
  
  
### Principles  
  
substrate dependence of decomposition, heterogeneity of speed of decay, internal transformations of organic matter, substrate interactions
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$C_{s}$|carbon stock in soil organic matter|$\text{quantitiy of carbon}$  
$C_{f}$|carbon stock in fresh organic matter|$\text{quantitiy of carbon}$  
$C_{ds}$|carbon stock in soil organic matter decomposers|$\text{quantitiy of carbon}$  
$C_{df}$|carbon stock in fresh organic matter decomposers|$\text{quantitiy of carbon}$  
$N$|mineral nitrogen pool ($N:C$ ratio always constant)|$\text{quantitiy of nitrogen}$  
  Table: state_variables  
The model section in the yaml file has no subsection: parameters.The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$I$|input vector|$I=\left[\begin{matrix}0\\\Phi_{l}\\0\\0\\\Phi_{i} -\Phi_{o} -\Phi_{up}\end{matrix}\right]$  
$C$|carbon content|$C=\left[\begin{matrix}C_{s}\\C_{f}\\C_{ds}\\C_{df}\\N\end{matrix}\right]$  
$A_{GM}$|decomposition operator|$A_{GM}=\left[\begin{matrix}-\frac{A}{C_{s}}\cdot C_{ds} & 0 & s & s & 0\\0 & - y & 0 & -\frac{\alpha\cdot r}{\alpha -\beta} & -\frac{i}{\alpha -\beta}\\\frac{A}{C_{s}}\cdot C_{ds} & y & - r - s & 0 & 0\\0 & 0 & 0 &\frac{\alpha\cdot r}{\alpha -\beta} - r - s &\frac{i}{\alpha -\beta}\\0 & y\cdot\left(-\alpha +\beta\right) &\alpha\cdot r & 0 & - i\end{matrix}\right]$  
$f_{s}$|the right hand side of the ode|$f_{s}=A_{GM} C + I$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{f}: \Phi_{l}$  
$N: \Phi_{i} -\Phi_{o} -\Phi_{up}$  

  
  
#### Output fluxes  
  
$C_{f}: C_{f}\cdot y\cdot\left(\alpha -\beta\right)$  
$C_{ds}: C_{ds}\cdot r\cdot\left(-\alpha + 1\right)$  
$C_{df}: C_{df}\cdot r$  
$N: N\cdot i$  

  
  
#### Internal fluxes  
  
$C_{s} \rightarrow C_{ds}: A\cdot C_{ds}$  
$C_{f} \rightarrow C_{ds}: C_{f}\cdot y$  
$C_{f} \rightarrow N: C_{f}\cdot y\cdot\left(-\alpha +\beta\right)$  
$C_{ds} \rightarrow C_{s}: C_{ds}\cdot s$  
$C_{ds} \rightarrow N: C_{ds}\cdot\alpha\cdot r$  
$C_{df} \rightarrow C_{s}: C_{df}\cdot s$  
$C_{df} \rightarrow C_{f}: -\frac{C_{df}\cdot\alpha\cdot r}{\alpha -\beta}$  
$N \rightarrow C_{f}: -\frac{N\cdot i}{\alpha -\beta}$  
$N \rightarrow C_{df}: \frac{N\cdot i}{\alpha -\beta}$  
  
  
  
  
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
  
