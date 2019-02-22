---
title: 'Report of the model: CTEM, version: 1'
---
  
  
---
title: 'Report of the model: CTEM, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Verónika Ceballos-Núñez (Orcid ID: 0000-0002-0046-1160) on 21/1/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation with a process based approach. It was originally described by @Arora2005GlobalChangeBiology.  
  
  
  
### Space Scale  
  
global
  
  
### Available parameter values  
  
  
  
Abbreviation|Description|Source  
:-----|:-----|:-----  
Original dataset of the publication|Eastern US and Germany, cold broadleaf deciduous|@Arora2005GlobalChangeBiology  
  Table:  Information on given parameter sets  
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$t$|time step|$year$  
$C_{L}$|Amount of carbon for the leaf|$kgC\cdot m^{-2}$  
$C_{S}$|Amount of carbon for the stem|$kgC\cdot m^{-2}$  
$C_{R}$|Amount of carbon for the root|$kgC\cdot m^{-2}$  
  Table: state_variables  
The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of states for vegetation|$x=\left[\begin{matrix}C_{L}\\C_{S}\\C_{R}\end{matrix}\right]$  
$u$|Vector of functions of photosynthetic inputs|$u=\left[\begin{matrix}G - R_{mL}\\a_{S}\\a_{R}\end{matrix}\right]$  
$A$|matrix of cycling rates|$A=\left[\begin{matrix}-\gamma_{N} -\gamma_{T} -\gamma_{W} & 0 & 0\\0 & - R_{gS} - R_{mS} -\gamma_{S} & 0\\0 & 0 & - R_{gR} - R_{mR} -\gamma_{R}\end{matrix}\right]$  
$f_{v}$|the righthandside of the ode|$f_{v}=A x + u$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{L}: G - R_{mL}$  
$C_{S}: \frac{\epsilon_{S} +\omega\cdot\left(1 - e^{- LAI\cdot k_{n}}\right)}{\omega\cdot\left(- W + 2 - e^{- LAI\cdot k_{n}}\right) + 1}$  
$C_{R}: \frac{-\epsilon_{L} -\epsilon_{S} +\omega\cdot\left(- W + 1\right) + 1}{\omega\cdot\left(- W + 2 - e^{- LAI\cdot k_{n}}\right) + 1}$  

  
  
#### Output fluxes  
  
$C_{L}: C_{L}\cdot\left(\gamma_{N} +\gamma_{Tmax}\cdot\left(-\beta_{T} + 1\right)^{b_{T}} +\gamma_{W}\right)$  
$C_{S}: C_{S}\cdot\left(R_{gS} + R_{mS} +\gamma_{S}\right)$  
$C_{R}: C_{R}\cdot\left(R_{gR} + R_{mR} +\gamma_{R}\right)$  
  
  
  
  
## Model simulations  
  
  
  
  
  
## Phaseplane plots  
  
  
  
  
  
## Fluxes  
  
  
  
## Steady state formulas  
  
$C_L = \frac{G - R_{mL}}{\gamma_{N} +\gamma_{Tmax}\cdot\left(-\beta_{T} + 1\right)^{b_{T}} +\gamma_{W}}$  
  
  
  
$C_S = \frac{-\epsilon_{S}\cdot e^{LAI\cdot k_{n}} -\omega\cdot e^{LAI\cdot k_{n}} +\omega}{R_{gS}\cdot W\cdot\omega\cdot e^{LAI\cdot k_{n}} - 2\cdot R_{gS}\cdot\omega\cdot e^{LAI\cdot k_{n}} + R_{gS}\cdot\omega - R_{gS}\cdot e^{LAI\cdot k_{n}} + R_{mS}\cdot W\cdot\omega\cdot e^{LAI\cdot k_{n}} - 2\cdot R_{mS}\cdot\omega\cdot e^{LAI\cdot k_{n}} + R_{mS}\cdot\omega - R_{mS}\cdot e^{LAI\cdot k_{n}} + W\cdot\gamma_{S}\cdot\omega\cdot e^{LAI\cdot k_{n}} - 2\cdot\gamma_{S}\cdot\omega\cdot e^{LAI\cdot k_{n}} +\gamma_{S}\cdot\omega -\gamma_{S}\cdot e^{LAI\cdot k_{n}}}$  
  
  
  
$C_R = \frac{\left(W\cdot\omega +\epsilon_{L} +\epsilon_{S} -\omega - 1\right)\cdot e^{LAI\cdot k_{n}}}{R_{gR}\cdot W\cdot\omega\cdot e^{LAI\cdot k_{n}} - 2\cdot R_{gR}\cdot\omega\cdot e^{LAI\cdot k_{n}} + R_{gR}\cdot\omega - R_{gR}\cdot e^{LAI\cdot k_{n}} + R_{mR}\cdot W\cdot\omega\cdot e^{LAI\cdot k_{n}} - 2\cdot R_{mR}\cdot\omega\cdot e^{LAI\cdot k_{n}} + R_{mR}\cdot\omega - R_{mR}\cdot e^{LAI\cdot k_{n}} + W\cdot\gamma_{R}\cdot\omega\cdot e^{LAI\cdot k_{n}} - 2\cdot\gamma_{R}\cdot\omega\cdot e^{LAI\cdot k_{n}} +\gamma_{R}\cdot\omega -\gamma_{R}\cdot e^{LAI\cdot k_{n}}}$  
  
  
  
  
  
  
  
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
  