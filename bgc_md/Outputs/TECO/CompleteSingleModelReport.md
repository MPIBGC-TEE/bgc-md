---
title: 'Report of the model: Terrestrial Ecosystem Model, version: 1'
---
  
  
# General Overview  
  

<br>
<center>
![Logo](Logo.svg)
</center>
This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by Carlos A. Sierra (Orcid ID: 0000-0003-0009-4169) on 12/4/2018.  
  
  
  
## About the model  
  
The model depicted in this document considers carbon allocation. It was originally described by @Luo2012TE.  
  
  
  
### Available parameter values  
  
  
  
Abbreviation|Description  
:-----|:-----  
Set1|Parameter values as described in Wang and Luo  
  Table:  Information on given parameter sets  
  
  
### Available initial values  
  
  
  
Abbreviation|Description  
:-----|:-----  
IV1|Initial values as in Wang and Luo  
  Table:  Information on given sets of initial values  
  
  
Name|Description  
:-----|:-----  
$x_{1}$|Carbon in foliage  
$x_{2}$|Carbon in roots  
$x_{3}$|Carbon in woody tissue  
$x_{4}$|Carbon in metabolic litter  
$x_{5}$|Carbon in structural litter  
$x_{6}$|Carbon in fast SOM  
$x_{7}$|Carbon in slow SOM  
$x_{8}$|Carbon in passive SOM  
  Table: state_variables  
  
  
Name|Description|Unit  
:-----|:-----|:-----  
$t$|time|$day$  
  Table: additional_variables  
  
  
Name|Description|Expression  
:-----|:-----|:-----:  
$x$|vector of state variables|$x=\left[\begin{matrix}x_{1}\\x_{2}\\x_{3}\\x_{4}\\x_{5}\\x_{6}\\x_{7}\\x_{8}\end{matrix}\right]$  
$u$|scalar function of photosynthetic inputs|$u=GPP$  
$b$|vector of partitioning coefficients of photosynthetically fixed carbon|$b=\left[\begin{matrix}b_{1}\\b_{2}\\b_{3}\\0\\0\\0\\0\\0\end{matrix}\right]$  
$C$|matrix of cycling rates|$C=\left[\begin{matrix}c_{1} & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & c_{2} & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & c_{3} & 0 & 0 & 0 & 0 & 0\\0 & 0 & 0 & c_{4} & 0 & 0 & 0 & 0\\0 & 0 & 0 & 0 & c_{5} & 0 & 0 & 0\\0 & 0 & 0 & 0 & 0 & c_{6} & 0 & 0\\0 & 0 & 0 & 0 & 0 & 0 & c_{7} & 0\\0 & 0 & 0 & 0 & 0 & 0 & 0 & c_{8}\end{matrix}\right]$  
$A$|matrix of transfer coefficients|$A=\left[\begin{matrix}-1 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\0 & -1 & 0 & 0 & 0 & 0 & 0 & 0\\0 & 0 & -1 & 0 & 0 & 0 & 0 & 0\\f_{41} & 0 & f_{43} & -1 & 0 & 0 & 0 & 0\\f_{51} & f_{52} & f_{53} & 0 & -1 & 0 & 0 & 0\\0 & 0 & 0 & f_{64} & f_{65} & -1 & f_{67} & f_{68}\\0 & 0 & 0 & 0 & f_{75} & f_{76} & -1 & 0\\0 & 0 & 0 & 0 & 0 & f_{86} & f_{87} & -1\end{matrix}\right]$  
$B$|matrix of cycling and tansfer rates|$B=A C$  
$f_{v}$|the righthandside of the ode|$f_{v}=u b + B x$  
  Table: components  
  
  
## Pool model representation  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Pool model representation*<br>
</center>
  
  
#### Input fluxes  
  
$x_{1}: GPP\cdot b_{1}$  
$x_{2}: GPP\cdot b_{2}$  
$x_{3}: GPP\cdot b_{3}$  

  
  
#### Output fluxes  
  
$x_{1}: c_{1}\cdot x_{1}\cdot\left(- f_{41} - f_{51} + 1\right)$  
$x_{2}: c_{2}\cdot x_{2}\cdot\left(- f_{52} + 1\right)$  
$x_{3}: c_{3}\cdot x_{3}\cdot\left(- f_{43} - f_{53} + 1\right)$  
$x_{4}: c_{4}\cdot x_{4}\cdot\left(- f_{64} + 1\right)$  
$x_{5}: c_{5}\cdot x_{5}\cdot\left(- f_{65} - f_{75} + 1\right)$  
$x_{6}: c_{6}\cdot x_{6}\cdot\left(- f_{76} - f_{86} + 1\right)$  
$x_{7}: c_{7}\cdot x_{7}\cdot\left(- f_{67} - f_{87} + 1\right)$  
$x_{8}: c_{8}\cdot x_{8}\cdot\left(- f_{68} + 1\right)$  

  
  
#### Internal fluxes  
  
$x_{1} \rightarrow x_{4}: c_{1}\cdot f_{41}\cdot x_{1}$  
$x_{1} \rightarrow x_{5}: c_{1}\cdot f_{51}\cdot x_{1}$  
$x_{2} \rightarrow x_{5}: c_{2}\cdot f_{52}\cdot x_{2}$  
$x_{3} \rightarrow x_{4}: c_{3}\cdot f_{43}\cdot x_{3}$  
$x_{3} \rightarrow x_{5}: c_{3}\cdot f_{53}\cdot x_{3}$  
$x_{4} \rightarrow x_{6}: c_{4}\cdot f_{64}\cdot x_{4}$  
$x_{5} \rightarrow x_{6}: c_{5}\cdot f_{65}\cdot x_{5}$  
$x_{5} \rightarrow x_{7}: c_{5}\cdot f_{75}\cdot x_{5}$  
$x_{6} \rightarrow x_{7}: c_{6}\cdot f_{76}\cdot x_{6}$  
$x_{6} \rightarrow x_{8}: c_{6}\cdot f_{86}\cdot x_{6}$  
$x_{7} \rightarrow x_{6}: c_{7}\cdot f_{67}\cdot x_{7}$  
$x_{7} \rightarrow x_{8}: c_{7}\cdot f_{87}\cdot x_{7}$  
$x_{8} \rightarrow x_{6}: c_{8}\cdot f_{68}\cdot x_{8}$  
  
  
  
  
## Model simulations  
  

<br>
<center>
![Model run 1 - solutions](Model run 1 - solutions.svg)<br>**Model run 1 - solutions:** *Initial values: IV1, Parameter set: Set1, Time step: 1*<br>
</center>
  
  
  
  
## Phaseplane plots  
  

<br>
<center>
![Model run 1 - phase planes](Model run 1 - phase planes.svg)<br>**Model run 1 - phase planes:** *Initial values: IV1, Parameter set: Set1, Start: 0, End: 200, Time step: 1*<br>
</center>
  
  
  
  
## Fluxes  
  

<br>
<center>
![Model run 1 - external input](Model run 1 - external input.svg)<br>**Model run 1 - external input:** *Initial values: IV1, Parameter set: Set1*<br>
</center>

<br>
<center>
![Model run 1 - external output](Model run 1 - external output.svg)<br>**Model run 1 - external output:** *Initial values: IV1, Parameter set: Set1*<br>
</center>

<br>
<center>
![Model run 1 - internal fluxes](Model run 1 - internal fluxes.svg)<br>**Model run 1 - internal fluxes:** *Initial values: IV1, Parameter set: Set1*<br>
</center>
  
  
## Steady state formulas  
  
$x_1 = \frac{GPP}{c_{1}}\cdot b_{1}$  
  
  
  
$x_2 = \frac{GPP}{c_{2}}\cdot b_{2}$  
  
  
  
$x_3 = \frac{GPP}{c_{3}}\cdot b_{3}$  
  
  
  
$x_4 = \frac{GPP}{c_{4}}\cdot\left(b_{1}\cdot f_{41} + b_{3}\cdot f_{43}\right)$  
  
  
  
$x_5 = \frac{GPP}{c_{5}}\cdot\left(b_{1}\cdot f_{51} + b_{2}\cdot f_{52} + b_{3}\cdot f_{53}\right)$  
  
  
  
$x_6 = -\frac{GPP}{c_{6}\cdot\left(f_{67}\cdot f_{76} + f_{68}\cdot f_{76}\cdot f_{87} + f_{68}\cdot f_{86} - 1\right)}\cdot\left(b_{1}\cdot\left(f_{41}\cdot f_{64} + f_{51}\cdot f_{65} + f_{51}\cdot f_{67}\cdot f_{75} + f_{51}\cdot f_{68}\cdot f_{75}\cdot f_{87}\right) + b_{2}\cdot f_{52}\cdot\left(f_{65} + f_{67}\cdot f_{75} + f_{68}\cdot f_{75}\cdot f_{87}\right) + b_{3}\cdot\left(f_{43}\cdot f_{64} + f_{53}\cdot f_{65} + f_{53}\cdot f_{67}\cdot f_{75} + f_{53}\cdot f_{68}\cdot f_{75}\cdot f_{87}\right)\right)$  
  
  
  
$x_7 = -\frac{GPP}{c_{7}\cdot\left(f_{67}\cdot f_{76} + f_{68}\cdot f_{76}\cdot f_{87} + f_{68}\cdot f_{86} - 1\right)}\cdot\left(b_{1}\cdot\left(f_{41}\cdot f_{64}\cdot f_{76} + f_{51}\cdot f_{65}\cdot f_{76} - f_{51}\cdot f_{68}\cdot f_{75}\cdot f_{86} + f_{51}\cdot f_{75}\right) + b_{2}\cdot f_{52}\cdot\left(f_{65}\cdot f_{76} - f_{68}\cdot f_{75}\cdot f_{86} + f_{75}\right) + b_{3}\cdot\left(f_{43}\cdot f_{64}\cdot f_{76} + f_{53}\cdot f_{65}\cdot f_{76} - f_{53}\cdot f_{68}\cdot f_{75}\cdot f_{86} + f_{53}\cdot f_{75}\right)\right)$  
  
  
  
$x_8 = -\frac{GPP}{c_{8}\cdot\left(f_{67}\cdot f_{76} + f_{68}\cdot f_{76}\cdot f_{87} + f_{68}\cdot f_{86} - 1\right)}\cdot\left(b_{1}\cdot\left(f_{41}\cdot f_{64}\cdot f_{76}\cdot f_{87} + f_{41}\cdot f_{64}\cdot f_{86} + f_{51}\cdot f_{65}\cdot f_{76}\cdot f_{87} + f_{51}\cdot f_{65}\cdot f_{86} + f_{51}\cdot f_{67}\cdot f_{75}\cdot f_{86} + f_{51}\cdot f_{75}\cdot f_{87}\right) + b_{2}\cdot f_{52}\cdot\left(f_{65}\cdot f_{76}\cdot f_{87} + f_{65}\cdot f_{86} + f_{67}\cdot f_{75}\cdot f_{86} + f_{75}\cdot f_{87}\right) + b_{3}\cdot\left(f_{43}\cdot f_{64}\cdot f_{76}\cdot f_{87} + f_{43}\cdot f_{64}\cdot f_{86} + f_{53}\cdot f_{65}\cdot f_{76}\cdot f_{87} + f_{53}\cdot f_{65}\cdot f_{86} + f_{53}\cdot f_{67}\cdot f_{75}\cdot f_{86} + f_{53}\cdot f_{75}\cdot f_{87}\right)\right)$  
  
  
  
  
  
## Steady states (potentially incomplete), according jacobian eigenvalues, damping ratio  
  
  
  
### Parameter set: Set1  
  
$x_1 = 182.868217054264$  
  
  
  
  
  
$x_2 = 14952.2184300341$  
  
  
  
  
  
$x_3 = 197.405857740586$  
  
  
  
  
  
$x_4 = 47.6128440366972$  
  
  
  
  
  
$x_5 = 1369.28421052632$  
  
  
  
  
  
$x_6 = 81.1112124108549$  
  
  
  
  
  
$x_7 = 6128.83566002952$  
  
  
  
  
  
$x_8 = 826.509774172633$  
  
  
  
  
  
$\lambda_{1}: -0.01090$  
  
  
$\lambda_{2}: -0.00095$  
  
  
$\lambda_{3}: -0.00258$  
  
  
$\lambda_{4}: -0.00239$  
  
  
$\lambda_{5}: -0.00006$  
  
  
$\lambda_{6}: -0.01051+0.00000j$  
$\rho_{6}: 1.000000$  
  
  
$\lambda_{7}: -0.00001-0.00000j$  
$\rho_{7}: 1.000000$  
  
  
$\lambda_{8}: -0.00009+0.00000j$  
$\rho_{8}: 1.000000$  
  
  
  
  
### Transit time density plot in steady state  
  

<br>
<center>
![Transit time density](Transit time density.svg)<br>**Transit time density:** * *<br>
</center>
  
  
  
  
## Mean ages  
  

<br>
<center>
![Model run 1 - mean ages](Model run 1 - mean ages.svg)<br>**Model run 1 - mean ages:** *Initial values: IV1, Parameter set: Set1, Time step: 1*<br>
</center>
  
  
  
  
## Age Density Evolution  
  
[Model run 1 - age density evolution](Model run 1 - age density evolution.html)  
  
## References  
  
