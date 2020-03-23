---
title: 'Report of the model: Integrated Science Assessment Model (ISAM), version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Verónika Ceballos-Núñez (Orcid ID: 0000-0002-0046-1160) on 3/5/2018.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation with a process based approach. It was originally described by @Arora2005GlobalChangeBiology.  
  
  
  
### Space Scale  
  
regional
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$t$|time step|$year$  
$C_{leaf}$|Amount of carbon for the leaf|$kgC\cdot m^{-2}$  
$C_{stem}$|Amount of carbon for the stem|$kgC\cdot m^{-2}$  
$C_{roots}$|Amount of carbon for the root|$kgC\cdot m^{-2}$  
  Table: state_variables  
The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of states for vegetation|$x=\left[\begin{matrix}C_{leaf}\\C_{stem}\\C_{roots}\end{matrix}\right]$  
$u$|Vector of functions of photosynthetic inputs|$u=\left[\begin{matrix}a_{L}\\a_{S}\\a_{R}\end{matrix}\right]$  
$A$|matrix of cycling rates|$A=\left[\begin{matrix}-\frac{1}{Y_{leaf}} & 0 & 0\\0 & -\frac{1}{Y_{stem}} & 0\\0 & 0 & -\frac{1}{Y_{roots}}\end{matrix}\right]$  
$f_{v}$|the righthandside of the ode|$f_{v}=A x + u$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{leaf}: \begin{cases} -\frac{C_{leaf}}{cn_{leaf}}\cdot gt\cdot k_{leaf}\cdot teta + GPP\cdot\left(- Allo_{fact roots} - Allo_{fact stem} + 1\right) &\text{for}\: NPP < 0\\NPP\cdot\left(- Allo_{fact roots} - Allo_{fact stem} + 1\right) &\text{for}\: NPP > 0\end{cases}$  
$C_{stem}: \begin{cases} Allo_{fact stem}\cdot GPP -\frac{C_{stem}}{cn_{stem}}\cdot gt\cdot k_{stem}\cdot teta &\text{for}\: NPP < 0\\Allo_{fact stem}\cdot NPP &\text{for}\: NPP > 0\end{cases}$  
$C_{roots}: \begin{cases} Allo_{fact roots}\cdot GPP -\frac{C_{roots}}{cn_{roots}}\cdot gt\cdot k_{roots}\cdot teta &\text{for}\: NPP < 0\\Allo_{fact roots}\cdot NPP &\text{for}\: NPP > 0\end{cases}$  

  
  
#### Output fluxes  
  
$C_{leaf}: \frac{C_{leaf}}{Y_{leaf}}$  
$C_{stem}: \frac{C_{stem}}{Y_{stem}}$  
$C_{roots}: \frac{C_{roots}}{Y_{roots}}$  
  
  
## References  
  
