---
title: Overview
---
  
  
Model|# Variables|# Constants|Structure|Right hand side of ODE|Source  
:-----|:-----:|:-----:|:-----:|:-----:|:-----:  
[CTEM](Arora2005GCB-1/Report.html)|$22$|$23$|$f_{v}=u+A\cdot x$|$\left[\begin{matrix}C_{L}\cdot\left(-\gamma_{N} -\gamma_{Tmax}\cdot\left(-\beta_{T} + 1\right)^{b_{T}} -\gamma_{W}\right) + G - R_{mL}\\C_{S}\cdot\left(- R_{gS} - R_{mS} -\gamma_{S}\right) +\frac{\epsilon_{S} +\omega\cdot\left(1 - e^{- LAI\cdot k_{n}}\right)}{\omega\cdot\left(- W + 2 - e^{- LAI\cdot k_{n}}\right) + 1}\\C_{R}\cdot\left(- R_{gR} - R_{mR} -\gamma_{R}\right) +\frac{-\epsilon_{L} -\epsilon_{S} +\omega\cdot\left(- W + 1\right) + 1}{\omega\cdot\left(- W + 2 - e^{- LAI\cdot k_{n}}\right) + 1}\end{matrix}\right]$|@Arora2005GlobalChangeBiology  
[DeAngelis2012TheorEcol](DeAngelis2012TheorEcol/Report.html)|$11$|$17$|$f_{v}=u\cdot b+A\cdot x$|$\left[\begin{matrix}C_{f}\cdot\left(-\frac{F_{i}}{N_{f}} -\gamma_{f}\right) +\frac{G_{0}\cdot N_{f}\cdot\eta_{f}}{C_{f}\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\\- C_{r}\cdot\gamma_{r} +\frac{G_{0}\cdot N_{f}\cdot\eta_{r}}{C_{f}\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\\- C_{w}\cdot\gamma_{w} +\frac{G_{0}\cdot N_{f}}{C_{f}\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\cdot\left(\eta_{f}\cdot s_{f} +\eta_{r}\cdot s_{r}\right)\\N_{f}\cdot\left(-\frac{F_{i}}{N_{f}} -\gamma_{f}\right) +\frac{G_{0}\cdot N_{f}}{C_{f}\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\cdot\left(\frac{C_{f}\cdot N_{pore}\cdot g_{N}\cdot\left(1 - e^{- C_{r}\cdot b_{r}\cdot k_{r}}\right)\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}{G_{0}\cdot N_{f}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\cdot\left(N_{pore} + k_{N}\right)} -\eta_{m}\cdot v_{m} -\frac{N_{w}}{C_{w}}\cdot\left(\eta_{f}\cdot s_{f} +\eta_{r}\cdot s_{r}\right) -\frac{N_{r}}{C_{r}}\cdot\eta_{r}\right)\end{matrix}\right]$|@DeAngelis2011TheoreticalEcology  
[IBIS](Castanho2013Biogeosciences/Report.html)|$5$|$3$|$f_{v}=u\cdot b+A\cdot x$|$\left[\begin{matrix}-\frac{C_{il}}{\tau_{il}} + NPP_{i}\cdot\left(- 0.0025\cdot S + 0.44\right)\\-\frac{C_{is}}{\tau_{is}} + NPP_{i}\cdot\left(- 0.0014\cdot S + 0.423\right)\\-\frac{C_{ir}}{\tau_{ir}} + NPP_{i}\cdot\left(0.0039\cdot S + 0.137\right)\end{matrix}\right]$|@Castanho2013Biogeosciences  
  Table: Summary of the models in the database of Carbon Allocation in Vegetation models  
  

<br>
<center>
![Figure 1](Figure 1.svg)<br>**Figure 1:** *Histograms,  variables*<br>
</center>

<br>
<center>
![Figure 2](Figure 2.svg)<br>**Figure 2:** *No. variables & parameters*<br>
</center>

<br>
<center>
![Figure 3](Figure 3.svg)<br>**Figure 3:** *No. variables & operations*<br>
</center>

<br>
<center>
![Figure 4](Figure 4.svg)<br>**Figure 4:** *No. variables & cascading depth of operations*<br>
</center>

<br>
<center>
![Figure 5](Figure 5.svg)<br>**Figure 5:** *No. variables & cascading depth of operations*<br>
</center>

<br>
<center>
![Figure 6](Figure 6.svg)<br>**Figure 6:** *Type of carbon partitioning scheme among pools and No.  operations*<br>
</center>

<br>
<center>
![Figure 7](Figure 7.svg)<br>**Figure 7:** *Type of carbon partitioning scheme among pools and claim to have a dynamic partitionings*<br>
</center>

<br>
<center>
![Figure 8](Figure 8.svg)<br>**Figure 8:** *Number of state variables and C cycling among compartments*<br>
</center>

<br>
<center>
![Figure 6](Figure 6.svg)<br>**Figure 6:** *Dependency plots of compartment variables*<br>
</center>
  
  
# Bibliography  
  
