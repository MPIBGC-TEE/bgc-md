---
title: "Report of the model: ACONITE, version: 1"
---

# General Overview
This report is the result of the use of the Python 3.4 package Sympy (for symbolic mathematics), as means to translate published models to a common language. It was created by Verónika Ceballos-Núñez (Orcid ID: 0000-0002-0046-1160) on 29/3/2016, and was last modified on _lm_.

## About the model
The model depicted in this document considers carbon allocation with a process based approach. It was originally described by @Thomas2014GeoscientificModelDevelopment.  

### Abstract
National Science Foundation Awards AGS-1020767 and EF-1048481

### Space Scale
global

# State Variables
The following table contains the available information regarding this section:

Name|Description|key
:-----:|:-----|:-----:
$C_{leaf}$|Carbon in foliage|foliage
$C_{wood}$|Carbon in wood|fine_wood
$C_{root}$|Carbon in roots|wood
$C_{labile}$|-|-
$C_{bud}$|-|-
$C_{labileRa}$|-|-
$N_{leaf}$|-|-
$N_{wood}$|-|-
$N_{root}$|-|-
$N_{labile}$|-|-
$N_{bud}$|-|-

Table: Information on State Variables

# Photosynthetic Parameters
The following table contains the available information regarding this section:

Name|Description|key|Type|Units
:-----:|:-----|:-----:|:-----:|:-----:
$GPP$|Photosynthesis; based on ACM model (see article for description)|GPP|variable|$gC\cdot day^{-1}$

Table: Information on Photosynthetic Parameters

# Allocation Fluxes
The following table contains the available information regarding this section:

Name|Description|Type|Units
:-----:|:-----|:-----:|:-----:
$a_{budC2leaf}$|Allocation from bud C pool to leaf C|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$a_{woodC}$|Allocation from labile C to wood C|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$a_{rootC}$|Allocation from labile C to root C|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$a_{budC2Ramain}$|Allocation of bud C pool to maintenance respiration pool when maintain respiration pool reaches zero; represents forgoing future leaf C to prevent carbon starvation.|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$a_{budC}$|Allocation of labile C to bud C; a fraction of the potential maximum leaf C|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$a_{Ramain}$|Allocation of labile C to future maintenance respiration; helps prevent carbon starvation during periods of negative NPP|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$a_{budN2leaf}$|Allocation from bud N pool to leaf C (???); bud N is set in previous year|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$a_{budN2Ramain}$|When bud C is used for maintenance respiration (a$_budC2Ramain$ > 0), bud N is returned to the labile N pool|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$a_{budN}$|Allocation of labile N to bud N; in seasonal environments it occurs in year prior to being displayed as leaf N|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$a_{woodN}$|Allocation from labile N to wood N|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$a_{rootN}$|Allocation from labile N to root N (???)|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$a_{labileRamain}$|Allocation of labile C to respiration of living tissues|variable|$gC\cdot m^{-2}\cdot day^{-1}$

Table: Information on Allocation Fluxes

# Nitrogen Uptake And Fixation
The following table contains the available information regarding this section:

Name|Description|doi|Type|Units
:-----:|:-----|:-----:|:-----:|:-----:
$U_{NH4}$|Uptake of NH$_4^+$ from mineral soil NH$_4^+$|$\frac{10.1007}{BF_{00015315}}$|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$U_{NO3}$|Uptake of NO$_3^-$ from mineral soil NO$_3^-$|$\frac{10.1007}{BF_{00015315}}$|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$U_{Nfix}$|Fixation of N from N$_2$; function of Ra$_excess$ flux, temperature, N demand, and C cost|-|variable|$gN\cdot m^{-2}\cdot day^{-1}$

Table: Information on Nitrogen Uptake And Fixation

# Turnover Fluxes
The following table contains the available information regarding this section:

Name|Description|Expressions|Type|Units
:-----:|:-----|:-----:|:-----:|:-----:
$\tau_{wood}$|Turnover of wood (C and N)|-|parameter|$day^{-1}$
$\tau_{root}$|Turnover of root (C and N)|-|parameter|$day^{-1}$
$t_{leafC}$|Turnover of leaf C to litter C; constant over year in humid tropics; seasonal otherwise|-|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$t_{woodC}$|Turnover of wood C to CWDC pool; occurs throughout year|$t_{woodC}=C_{wood}\cdot \tau_{wood}$|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$t_{rootC}$|Turnover of root C to litter C; occurs throughout year|$t_{rootC}=C_{root}\cdot \tau_{root}$|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$t_{retransN}$|Reabsorption of N from leaves to labile N|-|-|$gN\cdot m^{-2}\cdot day^{-1}$
$t_{leafN}$|Turnover of leaf N to litter N; constant over year in humid tropics; seasonal otherwise|-|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$t_{woodN}$|Turnover of wood N to CWDN pool; occurs throughout year|$t_{woodN}=N_{wood}\cdot \tau_{wood}$|variable|$gN\cdot m^{-2}\cdot day^{-1}$
$t_{rootN}$|Turnover of root N to litter N; occurs throughout year|$t_{rootN}=N_{root}\cdot \tau_{root}$|variable|$gN\cdot m^{-2}\cdot day^{-1}$

Table: Information on Turnover Fluxes

# Respiration Fluxes
The following table contains the available information regarding this section:

Name|Description|Type|Units
:-----:|:-----|:-----:|:-----:
$Ra_{growth}$|Growth respiration that occurs when tissue is allocated; a constant fraction of carbon allocated to tissue|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$Ra_{excess}$|Respiration that occurs when labile C exceeds a maximum labile C store; used for N fixation|variable|$gC\cdot m^{-2}\cdot day^{-1}$
$Ra_{main}$|Respiration of living tissues; a function of N content and temperature|variable|$gC\cdot m^{-2}\cdot day^{-1}$

Table: Information on Respiration Fluxes

# Components
The following table contains the available information regarding this section:

Name|Description|Expressions|key
:-----:|:-----|:-----:|:-----:
$x$|vector of states (C$_i$) for vegetation|$x=\left[\begin{matrix}C_{leaf}\\C_{wood}\\C_{root}\\C_{labile}\\C_{bud}\\C_{labileRa}\\N_{leaf}\\N_{wood}\\N_{root}\\N_{labile}\\N_{bud}\end{matrix}\right]$|state_vector
$I$|vector of fluxes into pool (C$_i$)|$I=\left[\begin{matrix}a_{budC2leaf}\\a_{woodC}\\a_{rootC}\\GPP\\a_{budC}\\a_{budC2Ramain} + a_{labileRamain}\\a_{budN2leaf}\\a_{woodN}\\a_{rootN}\\U_{NH4} + U_{NO3} + U_{Nfix} + a_{budN2Ramain} + t_{retransN}\\a_{budN2leaf}\end{matrix}\right]$|inflows
$O$|vector of fluxes out of pool (C$_i$)|$O=\left[\begin{matrix}- t_{leafC}\\- t_{woodC}\\- t_{rootC}\\- a_{budC} - a_{rootC} - a_{woodC}\\- a_{budC2leaf}\\0\\- t_{leafN} - t_{retransN}\\- t_{woodN}\\- t_{rootN}\\- a_{budN} - a_{rootN} - a_{woodN}\\0\end{matrix}\right]$|outflows
$R$|vector of respiration fluxes of pool (C$_i$)|$R=\left[\begin{matrix}0\\0\\0\\- Ra_{excess} - Ra_{growth} - a_{labileRamain}\\- a_{budC2Ramain}\\- Ra_{main}\\0\\0\\0\\0\\- a_{budN2Ramain}\end{matrix}\right]$|resp_matrix
$f_{v}$|the righthandside of the ode|$f_{v}=I+O+R$|state_vector_derivative

Table: Information on Components

## The right hand side of the ODE
$\left[\begin{matrix}a_{budC2leaf} - t_{leafC}\\- C_{wood}\cdot\tau_{wood} + a_{woodC}\\- C_{root}\cdot\tau_{root} + a_{rootC}\\GPP - Ra_{excess} - Ra_{growth} - a_{budC} - a_{labileRamain} - a_{rootC} - a_{woodC}\\a_{budC} - a_{budC2Ramain} - a_{budC2leaf}\\- Ra_{main} + a_{budC2Ramain} + a_{labileRamain}\\a_{budN2leaf} - t_{leafN} - t_{retransN}\\- N_{wood}\cdot\tau_{wood} + a_{woodN}\\- N_{root}\cdot\tau_{root} + a_{rootN}\\U_{NH4} + U_{NO3} + U_{Nfix} - a_{budN} + a_{budN2Ramain} - a_{rootN} - a_{woodN} + t_{retransN}\\- a_{budN2Ramain} + a_{budN2leaf}\end{matrix}\right]$

## The Jacobian (derivative of the ODE w.r.t. state variables)
$\left[\begin{array}{ccccccccccc}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & -\tau_{wood} & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & -\tau_{root} & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & -\tau_{wood} & 0 & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & -\tau_{root} & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\end{array}\right]$

## Steady state formulas
$C_{leaf} = C_{leaf}$ <br>$C_{wood} = \frac{a_{woodC}}{\tau_{wood}}$ <br>$C_{root} = \frac{a_{rootC}}{\tau_{root}}$ <br>$C_{labile} = C_{labile}$ <br>$C_{bud} = C_{bud}$ <br>$C_{labileRa} = C_{labileRa}$ <br>$N_{leaf} = N_{leaf}$ <br>$N_{wood} = \frac{a_{woodN}}{\tau_{wood}}$ <br>$N_{root} = \frac{a_{rootN}}{\tau_{root}}$ <br>$N_{labile} = N_{labile}$ <br>$N_{bud} = N_{bud}$ <br> <br>

# References
