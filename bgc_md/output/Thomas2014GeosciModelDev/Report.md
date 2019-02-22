---
title: 'Report of the model: A new, simple model of ecosystem C–N cycling and interactions (ACONITE), version: 1'
---
  
  
---
title: 'Report of the model: A new, simple model of ecosystem C–N cycling and interactions (ACONITE), version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Verónika Ceballos-Núñez (Orcid ID: 0000-0002-0046-1160) on 29/3/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation with a process based approach. It was originally described by @Thomas2014GeoscientificModelDevelopment.  
  
  
  
### Space Scale  
  
global
  
  
Name|Description  
:-----|:-----  
$C_{leaf}$|Carbon in foliage  
$C_{wood}$|Carbon in wood  
$C_{root}$|Carbon in roots  
$C_{labile}$|Labile carbon  
$C_{bud}$|Bud carbon  
$C_{labileRa}$|Maintenance respiration pool  
  Table: state_variables  
The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of states (C$_{i}$) for vegetation|$x=\left[\begin{matrix}C_{labile}\\C_{bud}\\C_{leaf}\\C_{wood}\\C_{root}\\C_{labileRa}\end{matrix}\right]$  
$u$|scalar function of photosynthetic inputs|$u=GPP$  
$b$|vector of partitioning coefficients of photosynthetically fixed carbon|$b=\left[\begin{matrix}1\\0\\0\\0\\0\\0\end{matrix}\right]$  
$A_{x}$|matrix of cycling rates|$A_{x}=\left[\begin{matrix}\frac{1}{C_{labile}}\cdot\left(- Ra_{excess} - Ra_{growth} - a_{budC} - a_{labileRamain} - a_{rootC} - a_{woodC}\right) & 0 & 0 & 0 & 0 & 0\\\frac{a_{budC}}{C_{labile}} &\frac{1}{C_{bud}}\cdot\left(- a_{budC2Ramain} - a_{budC2leaf}\right) & 0 & 0 & 0 & 0\\0 &\frac{a_{budC2leaf}}{C_{bud}} & -\tau_{leaf} & 0 & 0 & 0\\\frac{a_{woodC}}{C_{labile}} & 0 & 0 & -\tau_{wood} & 0 & 0\\\frac{a_{rootC}}{C_{labile}} & 0 & 0 & 0 & -\tau_{root} & 0\\\frac{a_{labileRamain}}{C_{labile}} &\frac{a_{budC2Ramain}}{C_{bud}} & 0 & 0 & 0 & -\frac{Ra_{main}}{C_{labileRa}}\end{matrix}\right]$  
$f_{v}$|the righthandside of the ode|$f_{v}=u b + A_{x} x$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{labile}: GPP$  

  
  
#### Output fluxes  
  
$C_{labile}: Ra_{excess} + Ra_{growth}$  
$C_{leaf}: C_{leaf}\cdot\tau_{leaf}$  
$C_{wood}: C_{wood}\cdot\tau_{wood}$  
$C_{root}: C_{root}\cdot\tau_{root}$  
$C_{labileRa}: Ra_{main}$  

  
  
#### Internal fluxes  
  
$C_{labile} \rightarrow C_{bud}: a_{budC}$  
$C_{labile} \rightarrow C_{wood}: a_{woodC}$  
$C_{labile} \rightarrow C_{root}: a_{rootC}$  
$C_{labile} \rightarrow C_{labileRa}: a_{labileRamain}$  
$C_{bud} \rightarrow C_{leaf}: a_{budC2leaf}$  
$C_{bud} \rightarrow C_{labileRa}: a_{budC2Ramain}$  
  
  
  
  
## Model simulations  
  
  
  
  
  
## Phaseplane plots  
  
  
  
  
  
## Fluxes  
  
  
  
## Steady state formulas  
  
$C_labile = C_{labile}$  
  
  
  
$C_bud = C_{bud}$  
  
  
  
$C_leaf = \frac{a_{budC2leaf}}{\tau_{leaf}}$  
  
  
  
$C_wood = \frac{a_{woodC}}{\tau_{wood}}$  
  
  
  
$C_root = \frac{a_{rootC}}{\tau_{root}}$  
  
  
  
$C_labileRa = C_{labileRa}$  
  
  
  
  
  
  
  
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
  