---
title: ' Emanuel1981, version: 1'
---
  
  
---
title: 'Report of the model: Emanuel1981, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Carlos A. Sierra (Orcid ID: 0000-0003-0009-4169) on 12/9/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation. It was originally described by @Emanuel1981.  
  
  
  
### Keywords  
  
differential equations, linear, time invariant, analytic
  
  
### Principles  
  
mass balance, substrate dependence of decomposition, heterogeneity of speed of decay, internal transformations of organic matter
  
  
### Available parameter values  
  
  
  
Abbreviation|Description  
:-----|:-----  
Original parameters of the publication|Parameter value of GPP corresponds to an annual average  
  Table:  Information on given parameter sets  
  
  
### Available initial values  
  
  
  
Abbreviation|Description  
:-----|:-----  
Original initial values of the publication|original dataset of the publication. Parameter value of GPP corresponds to an annual average  
  Table:  Information on given sets of initial values  
  
  
Name|Description  
:-----|:-----  
$x_{1}$|Non-woody tree parts  
$x_{2}$|Woody tree parts  
$x_{3}$|Ground vegetation  
$x_{4}$|Detritus/Decomposers  
$x_{5}$|Active soil carbon  
  Table: state_variables  
The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of state variables|$x=\left[\begin{matrix}x_{1}\\x_{2}\\x_{3}\\x_{4}\\x_{5}\end{matrix}\right]$  
$u$|vector of photosynthetically fixed carbon|$u=\left[\begin{matrix}I_{1}\\0\\I_{3}\\0\\0\end{matrix}\right]$  
$B$|matrix of cycling rates|$B=\left[\begin{matrix}- F_{1} & 0 & 0 & 0 & 0\\F_{21} & - F_{2} & 0 & 0 & 0\\0 & 0 & - F_{3} & 0 & 0\\F_{41} & F_{42} & F_{43} & - F_{4} & 0\\0 & F_{52} & F_{53} & F_{54} & - F_{5}\end{matrix}\right]$  
$f_{v}$|the righthandside of the ode|$f_{v}=B x + u$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$x_{1}: I_{1}$  
$x_{3}: I_{3}$  

  
  
#### Output fluxes  
  
$x_{1}: x_{1}\cdot\left(F_{1} - F_{21} - F_{41}\right)$  
$x_{2}: x_{2}\cdot\left(F_{2} - F_{42} - F_{52}\right)$  
$x_{3}: x_{3}\cdot\left(F_{3} - F_{43} - F_{53}\right)$  
$x_{4}: x_{4}\cdot\left(F_{4} - F_{54}\right)$  
$x_{5}: F_{5}\cdot x_{5}$  

  
  
#### Internal fluxes  
  
$x_{1} \rightarrow x_{2}: F_{21}\cdot x_{1}$  
$x_{1} \rightarrow x_{4}: F_{41}\cdot x_{1}$  
$x_{2} \rightarrow x_{4}: F_{42}\cdot x_{2}$  
$x_{2} \rightarrow x_{5}: F_{52}\cdot x_{2}$  
$x_{3} \rightarrow x_{4}: F_{43}\cdot x_{3}$  
$x_{3} \rightarrow x_{5}: F_{53}\cdot x_{3}$  
$x_{4} \rightarrow x_{5}: F_{54}\cdot x_{4}$  
  
  
## References  
  
