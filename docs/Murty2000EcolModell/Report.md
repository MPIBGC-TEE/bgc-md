---
title: 'Report of the model: Murty2000EcolModell, version: 1'
---
  
  
---
title: 'Report of the model: Murty2000EcolModell, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Verónika Ceballos-Núñez (Orcid ID: 0000-0002-0046-1160) on 16/3/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation with a process based approach. It was originally described by @Murty2000EcologicalModelling.  
  
  
  
### Space Scale  
  
global
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$C_{f}$|Foliar carbon mass|$kgC\cdot m^{-2}$  
$C_{r}$|Root carbon|$kgC\cdot m^{-2}$  
$C_{w}$|Carbon in woody tissue|$kgC\cdot m^{-2}$  
  Table: state_variables  
  
  
Name|Description|Expression|Unit  
:-----|:-----|:-----:|:-----  
$C_{sw}$|Sapwood carbon content|$C_{sw}=1.11\cdot C_{w}^{0.77}$|$kgC\cdot m^{-2}$  
$N_{f}$|Nitrogen content of foliage|-|$kgN\cdot m^{-2}$  
$N_{r}$|Nitrogen content of fine roots|-|-  
$n_{f}$|Foliar N:C ratio|-|-  
$n_{crit}$|Foliar N:C ratio below which production is N-limited|-|-  
$T_{a}$|Mean air temperature|-|-  
$Q_{10}$|\mathrm{None}|-|-  
$Q_{010}$|\mathrm{None}|-|-  
  Table: additional_variables  
  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of states for vegetation|$x=\left[\begin{matrix}C_{f}\\C_{r}\\C_{w}\end{matrix}\right]$  
$u$|scalar function of photosynthetic inputs|$u=NPP$  
$b$|vector of partitioning coefficients of photosynthetically fixed carbon|$b=\left[\begin{matrix}a_{f}\\a_{r}\\a_{w}\end{matrix}\right]$  
$A$|matrix of senescence (cycling) rates|$A=\left[\begin{matrix}-\gamma_{f} & 0 & 0\\0 & -\gamma_{r} & 0\\0 & 0 & -\gamma_{w}\end{matrix}\right]$  
$f_{v}$|the righthandside of the ode|$f_{v}=u b + A x$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{f}: a_{f}\cdot\left(- 0.0097236\cdot C_{w}^{0.77}\cdot Q_{010}^{\frac{T_{a}}{10}} + I_{0}\cdot\left(1 - e^{- C_{f}\cdot k\cdot\sigma}\right)\cdot\left(\begin{cases}\epsilon_{young} &\text{for}\: t{\leq} t_{1}\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t_{1} < t\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t < t_{2}\\\epsilon_{old} &\text{for}\: t{\geq} t_{2}\end{cases} &\text{otherwise}\end{cases} &\text{otherwise}\end{cases}\right)\cdot\begin{cases}\frac{\left(n_{crit} + 0.017\right)\cdot\left(1.84\cdot n_{f} - 0.01\right)}{\left(1.84\cdot n_{crit} - 0.01\right)\cdot\left(n_{f} + 0.017\right)} &\text{for}\: n_{f} < n_{crit}\\1 &\text{for}\: n_{f} > n_{crit}\end{cases} - 0.5\cdot N_{f}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - N_{r}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - R_{c}\right)$  
$C_{r}: a_{r}\cdot\left(- 0.0097236\cdot C_{w}^{0.77}\cdot Q_{010}^{\frac{T_{a}}{10}} + I_{0}\cdot\left(1 - e^{- C_{f}\cdot k\cdot\sigma}\right)\cdot\left(\begin{cases}\epsilon_{young} &\text{for}\: t{\leq} t_{1}\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t_{1} < t\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t < t_{2}\\\epsilon_{old} &\text{for}\: t{\geq} t_{2}\end{cases} &\text{otherwise}\end{cases} &\text{otherwise}\end{cases}\right)\cdot\begin{cases}\frac{\left(n_{crit} + 0.017\right)\cdot\left(1.84\cdot n_{f} - 0.01\right)}{\left(1.84\cdot n_{crit} - 0.01\right)\cdot\left(n_{f} + 0.017\right)} &\text{for}\: n_{f} < n_{crit}\\1 &\text{for}\: n_{f} > n_{crit}\end{cases} - 0.5\cdot N_{f}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - N_{r}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - R_{c}\right)$  
$C_{w}: \left(- a_{f} - a_{r} + 1\right)\cdot\left(- 0.0097236\cdot C_{w}^{0.77}\cdot Q_{010}^{\frac{T_{a}}{10}} + I_{0}\cdot\left(1 - e^{- C_{f}\cdot k\cdot\sigma}\right)\cdot\left(\begin{cases}\epsilon_{young} &\text{for}\: t{\leq} t_{1}\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t_{1} < t\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t < t_{2}\\\epsilon_{old} &\text{for}\: t{\geq} t_{2}\end{cases} &\text{otherwise}\end{cases} &\text{otherwise}\end{cases}\right)\cdot\begin{cases}\frac{\left(n_{crit} + 0.017\right)\cdot\left(1.84\cdot n_{f} - 0.01\right)}{\left(1.84\cdot n_{crit} - 0.01\right)\cdot\left(n_{f} + 0.017\right)} &\text{for}\: n_{f} < n_{crit}\\1 &\text{for}\: n_{f} > n_{crit}\end{cases} - 0.5\cdot N_{f}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - N_{r}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - R_{c}\right)$  

  
  
#### Output fluxes  
  
$C_{f}: C_{f}\cdot\gamma_{f}$  
$C_{r}: C_{r}\cdot\gamma_{r}$  
$C_{w}: C_{w}\cdot\gamma_{w}$  
  
  
  
  
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
  
