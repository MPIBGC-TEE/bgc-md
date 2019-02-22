---
title: ' Henin's model, version: 1'
---
  
  
---
title: 'Report of the model: Henin's model, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Holger Metzler (Orcid ID: 0000-0002-8239-1601) on 09/03/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers soil organic matter decomposition. It was originally described by @Henin1945Annalesagronomiques.  
  
  
  
### Keywords  
  
differential equations, linear, time invariant, analytic
  
  
### Principles  
  
mass balance, substrate dependence of decomposition, heterogeneity of speed of decay, internal transformations of organic matter
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$A$|labile pool|$MgC\cdot ha^{-1}$  
$B$|stable pool|$MgC\cdot ha^{-1}$  
  Table: state_variables  
The model section in the yaml file has no subsection: parameters.The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$C$|carbon content|$C=\left[\begin{matrix}A\\B\end{matrix}\right]$  
$I$|input vector|$I=\left[\begin{matrix}m\\0\end{matrix}\right]$  
$A_{GeM}$|decomposition operator|$A_{GeM}=\left[\begin{matrix}-\alpha & 0\\K\cdot\alpha & -\beta\end{matrix}\right]$  
$f_{s}$|the right hand side of the ode|$f_{s}=A_{GeM} C + I$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$A: m$  

  
  
#### Output fluxes  
  
$A: A\cdot\alpha\cdot\left(- K + 1\right)$  
$B: B\cdot\beta$  

  
  
#### Internal fluxes  
  
$A \rightarrow B: A\cdot K\cdot\alpha$  
  
  
## References  
  
