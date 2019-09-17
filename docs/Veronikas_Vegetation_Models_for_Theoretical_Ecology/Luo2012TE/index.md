---
title: 'Report of the model: Luo2012TE, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Verónika Ceballos-Núñez (Orcid ID: 0000-0002-0046-1160) on 24/3/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation with a process based approach. It was originally described by @Luo2012TE.  
  
  
  
### Space Scale  
  
global
  
  
### Available parameter values  
  
  
  
Abbreviation|Description  
:-----|:-----  
set1|Original parameters of the publication. Parameter value of GPP corresponds to an annual average  
  Table:  Information on given parameter sets  
  
  
### Available initial values  
  
  
  
Abbreviation|Description  
:-----|:-----  
_0|original dataset of the publication. Parameter value of GPP corresponds to an annual average  
  Table:  Information on given sets of initial values  
  
  
Name|Description  
:-----|:-----  
$C_{f}$|Carbon in foliage  
$C_{r}$|Carbon in roots  
$C_{w}$|Carbon in woody tissue  
  Table: state_variables  
The model section in the yaml file has no subsection: additional_variables.  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of states for vegetation|$x=\left[\begin{matrix}C_{f}\\C_{w}\\C_{r}\end{matrix}\right]$  
$u$|scalar function of photosynthetic inputs|$u=GPP\cdot\epsilon_{t}$  
$b$|vector of partitioning coefficients of photosynthetically fixed carbon|$b=\left[\begin{matrix}\eta_{f}\\\eta_{w}\\\eta_{r}\end{matrix}\right]$  
$A$|matrix of turnover (cycling) rates|$A=\left[\begin{matrix}-\gamma_{f} & 0 & 0\\0 & -\gamma_{w} & 0\\0 & 0 & -\gamma_{r}\end{matrix}\right]$  
$f_{v}$|the righthandside of the ode|$f_{v}=u b + A x$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{f}: GPP\cdot Q_{10}^{\frac{T}{10} - 1}\cdot\eta_{f}\cdot\min\left(1, 0.5\cdot W\right)$  
$C_{w}: GPP\cdot Q_{10}^{\frac{T}{10} - 1}\cdot\eta_{w}\cdot\min\left(1, 0.5\cdot W\right)$  
$C_{r}: GPP\cdot Q_{10}^{\frac{T}{10} - 1}\cdot\eta_{r}\cdot\min\left(1, 0.5\cdot W\right)$  

  
  
#### Output fluxes  
  
$C_{f}: C_{f}\cdot\gamma_{f}$  
$C_{w}: C_{w}\cdot\gamma_{w}$  
$C_{r}: C_{r}\cdot\gamma_{r}$  
  
  
## Steady state formulas  
  
$C_f = \frac{GPP}{\gamma_{f}}\cdot Q_{10}^{\frac{T}{10} - 1}\cdot\eta_{f}\cdot\min\left(1.0, 0.5\cdot W\right)$  
  
  
  
$C_w = \frac{GPP}{\gamma_{w}}\cdot Q_{10}^{\frac{T}{10} - 1}\cdot\eta_{w}\cdot\min\left(1.0, 0.5\cdot W\right)$  
  
  
  
$C_r = \frac{GPP}{\gamma_{r}}\cdot Q_{10}^{\frac{T}{10} - 1}\cdot\eta_{r}\cdot\min\left(1.0, 0.5\cdot W\right)$  
  
  
  
  
  
## References  
  
