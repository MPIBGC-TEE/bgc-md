---
title: 'Report of the model: Two-pool microbial, version: 1'
---
  
  
---
title: 'Report of the model: Two-pool microbial, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Holger Metzler (Orcid ID: 0000-0002-8239-1601) on 18/01/2018.  
  
  
  
## About the model  
  
The model depicted in this document considers soil organic matter decomposition. It was originally described by @Wang2014BG.  
  
  
  
### Keywords  
  
differential equations, nonlinear, time invariant
  
  
### Principles  
  
mass balance, substrate dependence of decomposition, heterogeneity of speed of decay, internal transformations of organic matter, substrate interaction
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$C_{s}$|soil organic matter|$g C m^{-2}$  
$C_{b}$|microbial biomass|$g C m^{-2}$  
  Table: state_variables  
The model section in the yaml file has no subsection: parameters.The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$C$|carbon content|$C=\left[\begin{matrix}C_{s}\\C_{b}\end{matrix}\right]$  
$I$|input vector|$I=\left[\begin{matrix}F_{NPP}\\0\end{matrix}\right]$  
$A$|decomposition operator|$A=\left[\begin{matrix}-\lambda &\mu_{b}\\\epsilon\cdot\lambda & -\mu_{b}\end{matrix}\right]$  
$f_{s}$|the right hand side of the ode|$f_{s}=A C + I$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{s}: F_{NPP}$  

  
  
#### Output fluxes  
  
$C_{s}: -\frac{C_{b}\cdot C_{s}\cdot V_{s}}{C_{s} + K_{s}}\cdot\left(\epsilon - 1\right)$  

  
  
#### Internal fluxes  
  
$C_{s} \rightarrow C_{b}: \frac{C_{b}\cdot C_{s}\cdot V_{s}}{C_{s} + K_{s}}\cdot\epsilon$  
$C_{b} \rightarrow C_{s}: C_{b}\cdot\mu_{b}$  
  
  
  
  
## Model simulations  
  
  
  
  
  
## Phaseplane plots  
  
  
  
  
  
## Fluxes  
  
  
  
## Steady state formulas  
  
$C_s = \frac{K_{s}\cdot\mu_{b}}{V_{s}\cdot\epsilon -\mu_{b}}$  
  
  
  
$C_b = -\frac{F_{NPP}\cdot\epsilon}{\mu_{b}\cdot\left(\epsilon - 1\right)}$  
  
  
  
  
  
  
  
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
  
