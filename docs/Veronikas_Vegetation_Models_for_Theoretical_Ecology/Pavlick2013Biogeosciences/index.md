---
title: 'Report of the model: The Jena Diversity-Dynamic Global Vegetation Model (JeDi-DGVM), version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Verónika Ceballos-Núñez (Orcid ID: 0000-0002-0046-1160) on \text{None}.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation with a process based approach. It was originally described by @Pavlick2013Biogeosciences.  
  
  
  
### Space Scale  
  
global
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$C_{A}$|Carbon in stored assimilates|$gC\cdot m^{-2}$  
$C_{L}$|Carbon in leaves|$gC\cdot m^{-2}$  
$C_{R}$|Carbon in fine roots|$gC\cdot m^{-2}$  
$C_{WL}$|Carbon in aboveground wood (branches and stems)|$gC\cdot m^{-2}$  
$C_{WR}$|Carbon in belowground wood (coarse roots)|$gC\cdot m^{-2}$  
$C_{S}$|Carbon in seeds (reproductive tisses)|$gC\cdot m^{-2}$  
  Table: state_variables  
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$C_{RES S}$|Growth respiration coefficient|$gC\cdot gC^{-1}$  
$C_{RES L}$|Growth respiration coefficient|$gC\cdot gC^{-1}$  
$C_{RES R}$|Growth respiration coefficient|$gC\cdot gC^{-1}$  
$C_{RES WL}$|Growth respiration coefficient|$gC\cdot gC^{-1}$  
$C_{RES WR}$|Growth respiration coefficient|$gC\cdot gC^{-1}$  
  Table: respiration  
  
  
Name|Description|Expression|Unit  
:-----|:-----|:-----:|:-----  
$A_{S}$|Allocation fraction to seeds|$A_{S}=\frac{f_{SEED}\cdot t_{5}}{t_{5} + t_{6} + t_{7} + t_{8}}$|-  
$A_{L}$|Allocation fraction to leaves|$A_{L}=\frac{f_{GROW}\cdot t_{6}\cdot\left(1 - t_{9}\right)}{t_{5} + t_{6} + t_{7} + t_{8}}$|-  
$A_{R}$|Allocation fraction to fine roots|$A_{R}=\frac{f_{GROW}\cdot t_{7}\cdot\left(1 - t_{10}\right)}{t_{5} + t_{6} + t_{7} + t_{8}}$|-  
$A_{WL}$|Allocation fraction to aboveground wood|$A_{WL}=\frac{f_{GROW}\cdot f_{VEG}\cdot t_{6}\cdot t_{9}}{t_{5} + t_{6} + t_{7} + t_{8}}$|-  
$A_{WR}$|Allocation fraction to belowground wood|$A_{WR}=\frac{f_{GROW}\cdot f_{VEG}\cdot t_{10}\cdot t_{7}}{t_{5} + t_{6} + t_{7} + t_{8}}$|-  
$\tau_{S}$|Seeds turnover rate|-|$days$  
$\tau_{L}$|Stem turnover rate|-|$days$  
$\tau_{R}$|Fine roots turnover rate|-|$days$  
$\tau_{WL}$|Aboveground wood turnover rate|-|$days$  
$\tau_{WR}$|Belowground wood turnover rate|-|$days$  
  Table: cycling_rates  
  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of states for vegetation|$x=\left[\begin{matrix}C_{A}\\C_{S}\\C_{L}\\C_{R}\\C_{WL}\\C_{WR}\end{matrix}\right]$  
$u$|scalar function of photosynthetic inputs|$u=NPP$  
$b$|vector of partitioning coefficients of photosynthetically fixed carbon|$b=\left[\begin{matrix}1\\0\\0\\0\\0\\0\end{matrix}\right]$  
$A$|matrix of cycling rates|$A=\left[\begin{matrix}- A_{L}\cdot\left(1 - C_{RES L}\right) - A_{R}\cdot\left(1 - C_{RES R}\right) - A_{S}\cdot\left(1 - C_{RES S}\right) - A_{WL}\cdot\left(1 - C_{RES WL}\right) - A_{WR}\cdot\left(1 - C_{RES WR}\right) &\frac{f_{GERM}\cdot\gamma_{GERM}}{\max\left(k_{GERM}, p\right)} & 0 & 0 & 0 & 0\\A_{S}\cdot\left(1 - C_{RES S}\right) & -\frac{f_{GERM}\cdot\gamma_{GERM}}{\max\left(k_{GERM}, p\right)} -\frac{1}{\tau_{S}} & 0 & 0 & 0 & 0\\A_{L}\cdot\left(1 - C_{RES L}\right) & 0 & -\frac{1}{\tau_{L}} & 0 & 0 & 0\\A_{R}\cdot\left(1 - C_{RES R}\right) & 0 & 0 & -\frac{1}{\tau_{R}} & 0 & 0\\A_{WL}\cdot\left(1 - C_{RES WL}\right) & 0 & 0 & 0 & -\frac{1}{\tau_{WL}} & 0\\A_{WR}\cdot\left(1 - C_{RES WR}\right) & 0 & 0 & 0 & 0 & -\frac{1}{\tau_{WR}}\end{matrix}\right]$  
$f_{v}$|the righthandside of the ode|$f_{v}=u b + A x$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$C_{A}: GPP - RES_{a}$  

  
  
#### Output fluxes  
  
$C_{S}: \frac{C_{S}}{\tau_{S}}$  
$C_{L}: \frac{C_{L}}{\tau_{L}}$  
$C_{R}: \frac{C_{R}}{\tau_{R}}$  
$C_{WL}: \frac{C_{WL}}{\tau_{WL}}$  
$C_{WR}: \frac{C_{WR}}{\tau_{WR}}$  

  
  
#### Internal fluxes  
  
$C_{A} \rightarrow C_{S}: -\frac{C_{A}\cdot f_{SEED}\cdot t_{5}\cdot\left(C_{RES S} - 1\right)}{t_{5} + t_{6} + t_{7} + t_{8}}$  
$C_{A} \rightarrow C_{L}: \frac{C_{A}\cdot f_{GROW}\cdot t_{6}\cdot\left(C_{RES L} - 1\right)\cdot\left(t_{9} - 1\right)}{t_{5} + t_{6} + t_{7} + t_{8}}$  
$C_{A} \rightarrow C_{R}: \frac{C_{A}\cdot f_{GROW}\cdot t_{7}\cdot\left(C_{RES R} - 1\right)\cdot\left(t_{10} - 1\right)}{t_{5} + t_{6} + t_{7} + t_{8}}$  
$C_{A} \rightarrow C_{WL}: \frac{C_{A}\cdot f_{GROW}\cdot t_{6}\cdot t_{9}\cdot\left(1 - e^{0.5\cdot C_{L}\cdot SLA}\right)\cdot\left(C_{RES WL} - 1\right)\cdot e^{- 0.5\cdot C_{L}\cdot SLA}}{t_{5} + t_{6} + t_{7} + t_{8}}$  
$C_{A} \rightarrow C_{WR}: \frac{C_{A}\cdot f_{GROW}\cdot t_{10}\cdot t_{7}\cdot\left(1 - e^{0.5\cdot C_{L}\cdot SLA}\right)\cdot\left(C_{RES WR} - 1\right)\cdot e^{- 0.5\cdot C_{L}\cdot SLA}}{t_{5} + t_{6} + t_{7} + t_{8}}$  
$C_{S} \rightarrow C_{A}: \frac{10^{\frac{4}{t_{4}^{4}}}\cdot C_{S}\cdot f_{GERM}}{\max\left(k_{GERM}, p\right)}$  
  
  
## References  
  
