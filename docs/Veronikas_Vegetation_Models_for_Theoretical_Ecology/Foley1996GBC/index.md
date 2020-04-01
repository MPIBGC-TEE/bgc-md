---
title: 'Report of the model: IBIS, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Verónika Ceballos-Núñez (Orcid ID: 0000-0002-0046-1160) on 26/1/2016.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation with a process based approach. It was originally described by @Foley1996GlobalBiogeochemicalCycles.  
  
  
  
### Space Scale  
  
global
  
  
### Available parameter values  
  
  
  
Abbreviation|Source  
:-----|:-----  
Tropical evergreen trees|@Foley1996GlobalBiogeochemicalCycles  
  Table:  Information on given parameter sets  
  
  
Name|Description  
:-----|:-----  
$C_{il}$|Carbon in leaves of plant functional type (PFT) i  
$C_{is}$|Carbon in transport tissue (mainly stems) of PFT$_{i}$  
$C_{ir}$|Carbon in fine roots of PFT$_{i}$  
  Table: state_variables  
  
  
Name|Description|Expression|Unit  
:-----|:-----|:-----:|:-----  
$t$|time step|-|$s$  
$Q_{p}$|Flux density of photosynthetically active radiation absorbed by the leaf|-|$Einstein\cdot m^{-2}\cdot s^{-1}$  
$\alpha_{3}$|Intrinsic quantum efficiency for CO_2 uptake in C_3 plants|-|$mol CO_2\cdot Einstein^{-1}$  
$\alpha_{4}$|\text{None}|-|-  
$O_{2}$|Atmospheric [O_2] (value: 0.209)|-|$mol\cdot mol^{-1}$  
$\tau$|Ratio of kinetic parameters describing the partitioning of enzyme activity to carboxylase or oxygenase function|-|-  
$\Gamma$|Gamma^* is the compensation point for gross photosynthesis|$\Gamma=\frac{O_{2}}{2\cdot\tau}$|$mol\cdot mol^{-1}$  
$C_{i}$|[CO_2] in the intercellular air spaces of the leaf|-|$mol\cdot mol^{-1}$  
$J_{e}$|Light-limited rate of photoynthesis|$J_{e}=\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\Gamma\right)}{C_{i} + 2\cdot\Gamma}$|-  
$J_{e4}$|Rubisco-limited rate of photosynthesis (C4 plants)|$J_{e4}=V_{m}$|-  
$V_{m}$|Maximum capacity of Rubisco to perform the carboxylase fuction|-|$mol CO_2\cdot m^{-2}\cdot s^{-1}$  
$K_{c}$|Michaelis-Menten coefficient for CO$_{2}$|-|$mol\cdot mol^{-1}$  
$K_{o}$|Michaelis-Menten coefficient for O$_{2}$|-|$mol\cdot mol^{-1}$  
$J_{c}$|Rubisco-limited rate of photosynthesis|$J_{c}=\frac{V_{m}\cdot\left(C_{i} -\Gamma\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}$|-  
$k$|\text{None}|-|-  
$J_{c4}$|CO$_{2}$-limited rate of photosynthesis at low [CO$_{2}$] (C4 plants)|$J_{c4}=C_{i}\cdot k$|-  
$T$|Rate of triose phosphate utilization|$T=0.121951219512195\cdot V_{m}$|-  
$J_{p}$|see section 6a|-|-  
$J_{s}$|Triose phosphate-limited rate of photosynthesis|$J_{s}=3\cdot T\cdot\left(1 -\frac{\Gamma}{C_{i}}\right) +\frac{\Gamma\cdot J_{p}}{C_{i}}$|-  
$J_{i}$|Light-limited rate of photosynthesis (C4 plants)|$J_{i}=Q_{p}\cdot\alpha_{4}$|-  
$A_{g}$|Gross photosynthesis rate per unit of area|$A_{g}=\min\left(J_{c}, J_{e}, J_{s}\right)$|$mol CO_2\cdot m^{-2}\cdot s^{-2}$  
$\gamma$|Leaf respiration cost of Rubisco acivity|-|-  
$B_{stem}$|Maintenance respiration coefficient defined at 15°C|-|-  
$B_{root}$|Maintenance respiration coefficient defined at 15°C|-|-  
$\lambda_{sapwood}$|Sapwood fraction of the total stem biomass (estimated from an assumed sap velocity and the maximum rate of transpiration experienced during the previous year)|-|-  
$E_{0}$|Temperature sensitivity factor|-|-  
$T_{0}$|Set to absolute zero (-273.16 °C)|-|-  
$T_{stem}$|Stem temperature|-|$°C$  
$T_{soil}$|Temperature of the soil in the rooting zone|-|$°C$  
$fT_{stem}$|f(T) is the Arrenhius temperature function|$fT_{stem}=e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)}$|-  
$fT_{soil}$|f(T) is the Arrenhius temperature function|$fT_{soil}=e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)}$|-  
$R_{leaf}$|Leaf maintenance respiration|$R_{leaf}=V_{m}\cdot\gamma$|$mol CO_2\cdot m^{-2}\cdot s^{-1}$  
$R_{stem}$|Stem maintenance respiration|$R_{stem}=B_{stem}\cdot C_{is}\cdot fT_{stem}\cdot\lambda_{sapwood}$|-  
$R_{root}$|Root maintenance respiration|$R_{root}=B_{root}\cdot C_{ir}\cdot fT_{soil}$|-  
$A_{n}$|Net leaf assimilation rate|$A_{n}=A_{g} - R_{leaf}$|$mol CO_2\cdot m^{-2}\cdot s^{-1}$  
$GPP - i$|Gross primary productivity|$GPP_{i}=A_{g}\cdot t$|-  
$\eta$|Fraction of carbon lost in the construction of net plant material because of growth respiration (value 0.33)|-|-  
$NPP_{i}$|Net Primary Production for PFT$_{i}$|$NPP_{i}=t\cdot\left(1 -\eta\right)\cdot\left(A_{g} - R_{leaf} - R_{root} - R_{stem}\right)$|-  
  Table: photosynthesis_and_respiration  
  
  
Name|Description  
:-----|:-----  
$a_{il}$|Fraction of annual NPP allocated to leaves for PFT$_{i}$  
$a_{is}$|Fraction of annual NPP allocated to stem for PFT$_{i}$  
$a_{ir}$|Fraction of annual NPP allocated to roots for PFT$_{i}$  
  Table: allocation_coefficients  
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$\tau_{il}$|Residence time of carbon in leaves for PFT$_{i}$|-  
$\tau_{is}$|Residence time of carbon in stem for PFT$_{i}$|-  
$\tau_{ir}$|Residence time of carbon in roots for PFT$_{i}$|-  
  Table: cycling_rates  
  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of states for vegetation|$x=\left[\begin{matrix}C_{il}\\C_{is}\\C_{ir}\end{matrix}\right]$  
$u$|scalar function of photosynthetic inputs|$u=NPP_{i}$  
$b$|vector of partitioning coefficients of photosynthetically fixed carbon|$b=\left[\begin{matrix}a_{il}\\a_{is}\\a_{ir}\end{matrix}\right]$  
$A$|matrix of turnover (cycling) rates|$A=\left[\begin{matrix}-\frac{1}{\tau_{il}} & 0 & 0\\0 & -\frac{1}{\tau_{is}} & 0\\0 & 0 & -\frac{1}{\tau_{ir}}\end{matrix}\right]$  
$f_{v}$|the righthandside of the ode|$f_{v}=u b + A x$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{il}: a_{il}\cdot\left(1 -\eta\right)\cdot\left(\begin{cases} t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} +\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}} - V_{m}\cdot\gamma\right) &\text{for}\:\left(\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\vee\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\\t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} - V_{m}\cdot\gamma +\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\right) &\text{for}\:\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\right)\vee\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\vee\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\\t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} - V_{m}\cdot\gamma + 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right) &\text{otherwise}\end{cases}\right)$  
$C_{is}: a_{is}\cdot\left(1 -\eta\right)\cdot\left(\begin{cases} t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} +\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}} - V_{m}\cdot\gamma\right) &\text{for}\:\left(\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\vee\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\\t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} - V_{m}\cdot\gamma +\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\right) &\text{for}\:\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\right)\vee\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\vee\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\\t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} - V_{m}\cdot\gamma + 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right) &\text{otherwise}\end{cases}\right)$  
$C_{ir}: a_{ir}\cdot\left(1 -\eta\right)\cdot\left(\begin{cases} t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} +\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}} - V_{m}\cdot\gamma\right) &\text{for}\:\left(\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\vee\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\\t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} - V_{m}\cdot\gamma +\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\right) &\text{for}\:\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq}\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}\right)\vee\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\wedge\frac{Q_{p}\cdot\alpha_{3}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} +\frac{O_{2}}{\tau}}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\vee\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)}{\leq} 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\\t\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{15 - T_{0}}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{15 - T_{0}}\right)} - V_{m}\cdot\gamma + 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right) &\text{otherwise}\end{cases}\right)$  

  
  
#### Output fluxes  
  
$C_{il}: \frac{C_{il}}{\tau_{il}}$  
$C_{is}: \frac{C_{is}}{\tau_{is}}$  
$C_{ir}: \frac{C_{ir}}{\tau_{ir}}$  
  
  
## References  
  
