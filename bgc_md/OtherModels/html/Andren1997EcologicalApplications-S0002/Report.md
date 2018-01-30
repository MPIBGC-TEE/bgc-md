---
title: "Report of the model: Introductory Carbon Balance Model (ICBM), version: 1"
---

# General Overview

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the Python 3.4 package Sympy (for symbolic mathematics), as means to translate published models to a common language. It was created by Holger Metzler (Orcid ID: \mathrm{None}) on 09/03/2016, and was last modified on \mathrm{None}.

## About the model
The model depicted in this document considers soil organic matter decomposition. It was originally described by @Andren1997EcologicalApplications.  

### Abstract
Atwo-component model was devised,comprisingyoungand old soil C, two decay constants, and parameters for litter input, ‘‘humification,’’ and external influences. Due to the model’s simplicity, the differential equations were solved analytically, and parameter optimizations can be made using generally available nonlinear regression pro- grams. The calibration parameter values were derived from a 35-yr experiment with arable crops on a clay soil in central Sweden. We show how the model can be used for medium- term (30 yr) predictions of the effects of changed inputs, climate, initial pools, litter quality, etc., on soil carbon pools. Equations are provided for calculating steady-state pool sizes as well as model parameters from litter bag or 14 C-labeled litter decomposition data. Strat- egies for model parameterization to different inputs, climatic regions, and soils, as well as the model’s relations to other model families, are briefly discussed

### Available parameter values


Abbreviation|Source
:-----|:-----
Bare fallow|@Andren1997EcologicalApplications
+N +straw|@Andren1997EcologicalApplications

Table:  Information on given parameter sets

### Available initial values


Abbreviation|Source
:-----|:-----
Bare fallow|@Andren1997EcologicalApplications
+N +straw|@Andren1997EcologicalApplications

Table:  Information on given sets of initial values

# State Variables
The following table contains the available information regarding this section:

Name|Description|Units|Values <br> <br>Bare fallow| <br> <br>+N +straw
:-----:|:-----|:-----:|:-----:|:-----:
$Y$|young pool of soil carbon|$kgCm^{-2}$|$0.3$|$0.3$
$O$|old pool of soil carbon|$kgCm^{-2}$|$3.96$|$4.11$

Table: Information on State Variables

# Parameters
The following table contains the available information regarding this section:

Name|Description|Type|Units|Values <br> <br>Bare fallow| <br> <br>+N +straw
:-----:|:-----|:-----:|:-----:|:-----:|:-----:
$i$|mean annual carbon input|parameter|$kgC m^{-2}yr^{-1}$|$0$|$0.285$
$k_{1}$|decomposition rate of young pool|parameter|$yr^{-1}$|$0.8$|$0.8$
$k_{2}$|decomposition rate of old pool|parameter|$yr^{-1}$|$0.00605$|$0.00605$
$h$|humification coefficient|parameter|-|$0.13$|$0.125$
$r$|climatic and edaphic factors|parameter|-|$1.32$|$1.0$

Table: Information on Parameters

# Time Variable
The following table contains the available information regarding this section:

Name|Units|Values <br> <br>Bare fallow| <br> <br>+N +straw
:-----:|:-----:|:-----:|:-----:
$t$|$yr$|-|-

Table: Information on Time Variable

# Components
The following table contains the available information regarding this section:

Name|Description|Expressions
:-----:|:-----|:-----:
$C$|carbon content|$C=\left[\begin{matrix}Y\\O\end{matrix}\right]$
$I$|input vector|$I=\left[\begin{matrix}i\\0\end{matrix}\right]$
$\xi$|environmental effects multiplier|$\xi=r$
$T$|transition operator|$T=\left[\begin{matrix}-1 & 0\\h & -1\end{matrix}\right]$
$N$|decomposition operator|$N=\left[\begin{matrix}k_{1} & 0\\0 & k_{2}\end{matrix}\right]$
$f_{s}$|the right hand side of the ode|$f_{s}=I+\xi\cdot T\cdot N\cdot C$

Table: Information on Components


## Pool model representation
<table><thead><tr><th></th><th>Flux description</th></tr></thead><tbody><tr><td align=center, style='vertical-align: middle'>
<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
</td><td align=left style='vertical-align: middle'>
#### Input fluxes
$Y: i$ <br>

#### Output fluxes
$Y: Y\cdot k_{1}\cdot r\cdot\left(- h + 1\right)$ <br>$O: O\cdot k_{2}\cdot r$ <br>

#### Internal fluxes
$Y > O: Y\cdot h\cdot k_{1}\cdot r$ <br></td></tr></tbody></table>
## The right hand side of the ODE
$\left[\begin{matrix}- Y\cdot k_{1}\cdot r + i\\- O\cdot k_{2}\cdot r + Y\cdot h\cdot k_{1}\cdot r\end{matrix}\right]$

## The Jacobian (derivative of the ODE w.r.t. state variables)
$\left[\begin{matrix}- k_{1}\cdot r & 0\\h\cdot k_{1}\cdot r & - k_{2}\cdot r\end{matrix}\right]$

## Steady state formulas
$Y = \frac{i}{k_{1}\cdot r}$ <br>$O = \frac{h\cdot i}{k_{2}\cdot r}$ <br> <br>

## Steady states (potentially incomplete), according jacobian eigenvalues, damping ratio

### Parameter set: Bare fallow
$Y: 0.0$, $O: 0.0$ <br> <br>$\lambda_{1}: -0.008$ <br>$\lambda_{2}: -1.056$ <br>


### Parameter set: +N +straw
$Y: 0.356$, $O: 5.888$ <br> <br>$\lambda_{1}: -0.006$ <br>$\lambda_{2}: -0.800$ <br>


## Model simulations

<br>
<center>
![Model run 1 - solutions](Model run 1 - solutions.svg)<br>**Model run 1 - solutions:** *Initial values: Bare fallow, Parameter set: Bare fallow, Time step: 0.1*<br>
</center>

<br>
<center>
![Model run 1 - phase planes](Model run 1 - phase planes.svg)<br>**Model run 1 - phase planes:** *Initial values: Bare fallow, Parameter set: Bare fallow, Start: 0, End: 100, Time step: 0.1*<br>
</center>

<br>
<center>
![Model run 1 - system-age-distributions](Model run 1 - system-age-distributions.svg)<br>**Model run 1 - system-age-distributions:** *Initial values: Bare fallow, Parameter set: Bare fallow*<br>
</center>

<br>
<center>
![Model run 2 - solutions](Model run 2 - solutions.svg)<br>**Model run 2 - solutions:** *Initial values: +N +straw, Parameter set: +N +straw, Time step: 0.1*<br>
</center>

<br>
<center>
![Model run 2 - phase planes](Model run 2 - phase planes.svg)<br>**Model run 2 - phase planes:** *Initial values: +N +straw, Parameter set: +N +straw, Start: 0, End: 100, Time step: 0.1*<br>
</center>

<br>
<center>
![Model run 2 - system-age-distributions](Model run 2 - system-age-distributions.svg)<br>**Model run 2 - system-age-distributions:** *Initial values: +N +straw, Parameter set: +N +straw*<br>
</center>


# References
