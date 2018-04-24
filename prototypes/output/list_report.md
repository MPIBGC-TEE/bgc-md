
# Overview of the models
<script language="javascript">
        function ausklappen(id)
        {
            if (document.getElementById(id).style.display=="none")
            {
                document.getElementById(id).style.display="block";
            }
            else
            {
                document.getElementById(id).style.display="none";
            }
        }
</script>
<table>
<thead><tr class="header">
<th></th><th align="left">Model</th>
<th align="center">Variables</th>
<th align="center"># Parameters</th>
<th align="center"># Constants</th>
<th align="center">Structure</th>
<th align="center">Right hand side of ODE</th>
<th align="left">Source</th>
</tr>
</thead>
<tbody>
<tr class="even">
<td align="left"><img src="Andren1997EcologicalApplications/Thumbnail.svg"> </td><td align="left"><a href="Andren1997EcologicalApplications/Report.html" target="_blank">ICBM</a></td>
<td align="center" onclick="ausklappen('comp_table_0');ausklappen('rhs_0')">2</td>
<td align="center" onclick="ausklappen('comp_table_0');ausklappen('rhs_0')">5</td>
<td align="center" onclick="ausklappen('comp_table_0');ausklappen('rhs_0')"></td>
<td align="center" onclick="ausklappen('comp_table_0');ausklappen('rhs_0')">$f_{s}=I+\xi\cdot T\cdot N\cdot C$
<div id="comp_table_0" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}Y\\O\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}i\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$\xi$</td>
<td align="left">environmental effects multiplier</td>
<td align="center">$\xi=r$</td>
</tr>
<tr>
<td align="center">$T$</td>
<td align="left">transition operator</td>
<td align="center">$T=\left[\begin{matrix}-1 & 0\\h & -1\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$N$</td>
<td align="left">decomposition operator</td>
<td align="center">$N=\left[\begin{matrix}k_{1} & 0\\0 & k_{2}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+\xi\cdot T\cdot N\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_0');ausklappen('rhs_0')"><div id="rhs_0" style="display:none">$\left[\begin{matrix}- Y\cdot k_{1}\cdot r + i\\- O\cdot k_{2}\cdot r + Y\cdot h\cdot k_{1}\cdot r\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_0');ausklappen('rhs_0')">@Andren1997EcologicalApplications</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Potter1993GlobalBiogeochmemCy/Thumbnail.svg"> </td><td align="left"><a href="Potter1993GlobalBiogeochmemCy/Report.html" target="_blank">CASA</a></td>
<td align="center" onclick="ausklappen('comp_table_1');ausklappen('rhs_1')">10</td>
<td align="center" onclick="ausklappen('comp_table_1');ausklappen('rhs_1')">6</td>
<td align="center" onclick="ausklappen('comp_table_1');ausklappen('rhs_1')"></td>
<td align="center" onclick="ausklappen('comp_table_1');ausklappen('rhs_1')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_1" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{f}\\C_{r}\\C_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=NPP$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}\alpha_{f}\\\alpha_{r}\\\alpha_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of turnover (cycling) rates</td>
<td align="center">$A=\left[\begin{matrix}-\tau_{f} & 0 & 0\\0 & -\tau_{r} & 0\\0 & 0 & -\tau_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_1');ausklappen('rhs_1')"><div id="rhs_1" style="display:none">$\left[\begin{matrix}- C_{f}\cdot\tau_{f} + 0.5\cdot FPAR\cdot SOL\cdot\alpha_{f}\cdot\epsilon\\- C_{r}\cdot\tau_{r} + 0.5\cdot FPAR\cdot SOL\cdot\alpha_{r}\cdot\epsilon\\- C_{w}\cdot\tau_{w} + 0.5\cdot FPAR\cdot SOL\cdot\alpha_{w}\cdot\epsilon\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_1');ausklappen('rhs_1')">@Potter1993GlobalBiogeochemicalCycles</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Ceballos2016/Thumbnail.svg"> </td><td align="left"><a href="Ceballos2016/Report.html" target="_blank">CAVPFP</a></td>
<td align="center" onclick="ausklappen('comp_table_2');ausklappen('rhs_2')">6</td>
<td align="center" onclick="ausklappen('comp_table_2');ausklappen('rhs_2')">0</td>
<td align="center" onclick="ausklappen('comp_table_2');ausklappen('rhs_2')"></td>
<td align="center" onclick="ausklappen('comp_table_2');ausklappen('rhs_2')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_2" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{f}\\C_{NSC}\\C_{w}\\C_{r}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=k_{1}\cdot C_{f}$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}\eta_{f}\\0\\0\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of cycling rates</td>
<td align="center">$A=\left[\begin{matrix}-\eta_{NSC} -\gamma_{f} &\gamma_{fNSC} & 0 & 0\\\eta_{NSC} & -\eta_{r} -\eta_{w} -\gamma_{fNSC} &\gamma_{NSCw} &\gamma_{\mathscr{N}}\\0 &\eta_{w} & -\gamma_{NSCw} -\gamma_{w} & 0\\0 &\eta_{r} & 0 & -\gamma_{\mathscr{N}} -\gamma_{r}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_2');ausklappen('rhs_2')"><div id="rhs_2" style="display:none">$\left[\begin{matrix}C_{NSC}\cdot\gamma_{fNSC} + 0.1\cdot C_{f}\cdot C_{r}\cdot k_{1} + C_{f}\cdot\left(-\gamma_{f} -\frac{0.1}{C_{NSC}}\right)\\C_{NSC}\cdot\left(-\eta_{r} -\eta_{w} -\gamma_{fNSC}\right) + C_{r}\cdot\gamma_{\mathscr{N}} + C_{w}\cdot\gamma_{NSCw} +\frac{0.1}{C_{NSC}}\cdot C_{f}\\C_{NSC}\cdot\eta_{w} + C_{w}\cdot\left(-\gamma_{NSCw} -\gamma_{w}\right)\\C_{NSC}\cdot\eta_{r} + C_{r}\cdot\left(-\gamma_{\mathscr{N}} -\gamma_{r}\right)\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_2');ausklappen('rhs_2')">@Ceballos2016</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Thomas2014GeosciModelDev/Thumbnail.svg"> </td><td align="left"><a href="Thomas2014GeosciModelDev/Report.html" target="_blank">ACONITE</a></td>
<td align="center" onclick="ausklappen('comp_table_3');ausklappen('rhs_3')">20</td>
<td align="center" onclick="ausklappen('comp_table_3');ausklappen('rhs_3')">3</td>
<td align="center" onclick="ausklappen('comp_table_3');ausklappen('rhs_3')"></td>
<td align="center" onclick="ausklappen('comp_table_3');ausklappen('rhs_3')">$f_{v}=u\cdot b+A_{x}\cdot x$
<div id="comp_table_3" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states (C$_{i}$) for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{labile}\\C_{bud}\\C_{leaf}\\C_{wood}\\C_{root}\\C_{labileRa}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=GPP$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}1\\0\\0\\0\\0\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A_{x}$</td>
<td align="left">matrix of cycling rates</td>
<td align="center">$A_{x}=\left[\begin{matrix}\frac{1}{C_{labile}}\cdot\left(- Ra_{excess} - Ra_{growth} - a_{budC} - a_{labileRamain} - a_{rootC} - a_{woodC}\right) & 0 & 0 & 0 & 0 & 0\\\frac{a_{budC}}{C_{labile}} &\frac{1}{C_{bud}}\cdot\left(- a_{budC2Ramain} - a_{budC2leaf}\right) & 0 & 0 & 0 & 0\\0 &\frac{a_{budC2leaf}}{C_{bud}} & -\tau_{leaf} & 0 & 0 & 0\\\frac{a_{woodC}}{C_{labile}} & 0 & 0 & -\tau_{wood} & 0 & 0\\\frac{a_{rootC}}{C_{labile}} & 0 & 0 & 0 & -\tau_{root} & 0\\\frac{a_{labileRamain}}{C_{labile}} &\frac{a_{budC2Ramain}}{C_{bud}} & 0 & 0 & 0 & -\frac{Ra_{main}}{C_{labileRa}}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A_{x}\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_3');ausklappen('rhs_3')"><div id="rhs_3" style="display:none">$\left[\begin{matrix}GPP - Ra_{excess} - Ra_{growth} - a_{budC} - a_{labileRamain} - a_{rootC} - a_{woodC}\\a_{budC} - a_{budC2Ramain} - a_{budC2leaf}\\- C_{leaf}\cdot\tau_{leaf} + a_{budC2leaf}\\- C_{wood}\cdot\tau_{wood} + a_{woodC}\\- C_{root}\cdot\tau_{root} + a_{rootC}\\- Ra_{main} + a_{budC2Ramain} + a_{labileRamain}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_3');ausklappen('rhs_3')">@Thomas2014GeoscientificModelDevelopment</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Wang2014BG3p/Thumbnail.svg"> </td><td align="left"><a href="Wang2014BG3p/Report.html" target="_blank">Three-pool microbial</a></td>
<td align="center" onclick="ausklappen('comp_table_4');ausklappen('rhs_4')">3</td>
<td align="center" onclick="ausklappen('comp_table_4');ausklappen('rhs_4')">8</td>
<td align="center" onclick="ausklappen('comp_table_4');ausklappen('rhs_4')"></td>
<td align="center" onclick="ausklappen('comp_table_4');ausklappen('rhs_4')">$f_{s}=I+A\cdot C$
<div id="comp_table_4" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}C_{l}\\C_{s}\\C_{b}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}F_{NPP}\cdot\left(-\alpha + 1\right)\\F_{NPP}\cdot\alpha\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">decomposition operator</td>
<td align="center">$A=\left[\begin{matrix}-\lambda_{l} & 0 & 0\\0 & -\lambda_{s} &\mu_{b}\\\epsilon\cdot\lambda_{l} &\epsilon\cdot\lambda_{s} & -\mu_{b}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+A\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_4');ausklappen('rhs_4')"><div id="rhs_4" style="display:none">$\left[\begin{matrix}-\frac{C_{b}\cdot C_{l}\cdot V_{l}}{C_{l} + K_{l}} + F_{NPP}\cdot\left(-\alpha + 1\right)\\-\frac{C_{b}\cdot C_{s}\cdot V_{s}}{C_{s} + K_{s}} + C_{b}\cdot\mu_{b} + F_{NPP}\cdot\alpha\\\frac{C_{b}\cdot C_{l}\cdot V_{l}}{C_{l} + K_{l}}\cdot\epsilon +\frac{C_{b}\cdot C_{s}\cdot V_{s}}{C_{s} + K_{s}}\cdot\epsilon - C_{b}\cdot\mu_{b}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_4');ausklappen('rhs_4')">@Wang2014BG</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="DeAngelis2012TheorEcol/Thumbnail.svg"> </td><td align="left"><a href="DeAngelis2012TheorEcol/Report.html" target="_blank">DeAngelis2012TheoreticalEcology</a></td>
<td align="center" onclick="ausklappen('comp_table_5');ausklappen('rhs_5')">11</td>
<td align="center" onclick="ausklappen('comp_table_5');ausklappen('rhs_5')">17</td>
<td align="center" onclick="ausklappen('comp_table_5');ausklappen('rhs_5')"></td>
<td align="center" onclick="ausklappen('comp_table_5');ausklappen('rhs_5')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_5" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{f}\\C_{r}\\C_{w}\\N_{f}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=G$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}\eta_{f}\\\eta_{r}\\\eta_{w}\\-\eta_{m}\cdot v_{m} -\eta_{r}\cdot v_{r} -\eta_{w}\cdot v_{w} +\frac{U}{G}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of senescence (cycling) rates</td>
<td align="center">$A=\left[\begin{matrix}-\frac{F_{i}}{N_{f}} -\gamma_{f} & 0 & 0 & 0\\0 & -\gamma_{r} & 0 & 0\\0 & 0 & -\gamma_{w} & 0\\0 & 0 & 0 & -\frac{F_{i}}{N_{f}} -\gamma_{f}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_5');ausklappen('rhs_5')"><div id="rhs_5" style="display:none">$\left[\begin{matrix}C_{f}\cdot\left(-\frac{F_{i}}{N_{f}} -\gamma_{f}\right) +\frac{G_{0}\cdot N_{f}\cdot\eta_{f}}{C_{f}\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\\- C_{r}\cdot\gamma_{r} +\frac{G_{0}\cdot N_{f}\cdot\eta_{r}}{C_{f}\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\\- C_{w}\cdot\gamma_{w} +\frac{G_{0}\cdot N_{f}}{C_{f}\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\cdot\left(\eta_{f}\cdot s_{f} +\eta_{r}\cdot s_{r}\right)\\N_{f}\cdot\left(-\frac{F_{i}}{N_{f}} -\gamma_{f}\right) +\frac{G_{0}\cdot N_{f}}{C_{f}\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\cdot\left(\frac{C_{f}\cdot N_{pore}\cdot g_{N}\cdot\left(1 - e^{- C_{r}\cdot b_{r}\cdot k_{r}}\right)\cdot\left(v_{0} +\frac{N_{f}}{C_{f}}\right)}{G_{0}\cdot N_{f}\cdot\left(1 - e^{- C_{f}\cdot b_{f}\cdot k_{f}}\right)\cdot\left(N_{pore} + k_{N}\right)} -\eta_{m}\cdot v_{m} -\frac{N_{w}}{C_{w}}\cdot\left(\eta_{f}\cdot s_{f} +\eta_{r}\cdot s_{r}\right) -\frac{N_{r}}{C_{r}}\cdot\eta_{r}\right)\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_5');ausklappen('rhs_5')">@DeAngelis2012TheoreticalEcology</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Murty2000EcolModell/Thumbnail.svg"> </td><td align="left"><a href="Murty2000EcolModell/Report.html" target="_blank">Murty2000EcologicalModelling</a></td>
<td align="center" onclick="ausklappen('comp_table_6');ausklappen('rhs_6')">15</td>
<td align="center" onclick="ausklappen('comp_table_6');ausklappen('rhs_6')">12</td>
<td align="center" onclick="ausklappen('comp_table_6');ausklappen('rhs_6')"></td>
<td align="center" onclick="ausklappen('comp_table_6');ausklappen('rhs_6')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_6" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{f}\\C_{r}\\C_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=NPP$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}a_{f}\\a_{r}\\a_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of senescence (cycling) rates</td>
<td align="center">$A=\left[\begin{matrix}-\gamma_{f} & 0 & 0\\0 & -\gamma_{r} & 0\\0 & 0 & -\gamma_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_6');ausklappen('rhs_6')"><div id="rhs_6" style="display:none">$\left[\begin{matrix}- C_{f}\cdot\gamma_{f} + a_{f}\cdot\left(- 0.0097236\cdot C_{w}^{0.77}\cdot Q_{010}^{\frac{T_{a}}{10}} + I_{0}\cdot\left(1 - e^{- C_{f}\cdot k\cdot\sigma}\right)\cdot\left(\begin{cases}\epsilon_{young} &\text{for}\: t{\leq} t_{1}\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t_{1} < t\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t < t_{2}\\\epsilon_{old} &\text{for}\: t{\geq} t_{2}\end{cases} &\text{otherwise}\end{cases} &\text{otherwise}\end{cases}\right)\cdot\begin{cases}\frac{\left(n_{crit} + 0.017\right)\cdot\left(1.84\cdot n_{f} - 0.01\right)}{\left(1.84\cdot n_{crit} - 0.01\right)\cdot\left(n_{f} + 0.017\right)} &\text{for}\: n_{f} < n_{crit}\\1 &\text{for}\: n_{f} > n_{crit}\end{cases} - 0.5\cdot N_{f}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - N_{r}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - R_{c}\right)\\- C_{r}\cdot\gamma_{r} + a_{r}\cdot\left(- 0.0097236\cdot C_{w}^{0.77}\cdot Q_{010}^{\frac{T_{a}}{10}} + I_{0}\cdot\left(1 - e^{- C_{f}\cdot k\cdot\sigma}\right)\cdot\left(\begin{cases}\epsilon_{young} &\text{for}\: t{\leq} t_{1}\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t_{1} < t\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t < t_{2}\\\epsilon_{old} &\text{for}\: t{\geq} t_{2}\end{cases} &\text{otherwise}\end{cases} &\text{otherwise}\end{cases}\right)\cdot\begin{cases}\frac{\left(n_{crit} + 0.017\right)\cdot\left(1.84\cdot n_{f} - 0.01\right)}{\left(1.84\cdot n_{crit} - 0.01\right)\cdot\left(n_{f} + 0.017\right)} &\text{for}\: n_{f} < n_{crit}\\1 &\text{for}\: n_{f} > n_{crit}\end{cases} - 0.5\cdot N_{f}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - N_{r}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - R_{c}\right)\\- C_{w}\cdot\gamma_{w} +\left(- a_{f} - a_{r} + 1\right)\cdot\left(- 0.0097236\cdot C_{w}^{0.77}\cdot Q_{010}^{\frac{T_{a}}{10}} + I_{0}\cdot\left(1 - e^{- C_{f}\cdot k\cdot\sigma}\right)\cdot\left(\begin{cases}\epsilon_{young} &\text{for}\: t{\leq} t_{1}\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t_{1} < t\\\begin{cases}\epsilon_{young} -\frac{\left(-\epsilon_{old} +\epsilon_{young}\right)\cdot\left(t - t_{1}\right)}{- t_{1} + t_{2}} &\text{for}\: t < t_{2}\\\epsilon_{old} &\text{for}\: t{\geq} t_{2}\end{cases} &\text{otherwise}\end{cases} &\text{otherwise}\end{cases}\right)\cdot\begin{cases}\frac{\left(n_{crit} + 0.017\right)\cdot\left(1.84\cdot n_{f} - 0.01\right)}{\left(1.84\cdot n_{crit} - 0.01\right)\cdot\left(n_{f} + 0.017\right)} &\text{for}\: n_{f} < n_{crit}\\1 &\text{for}\: n_{f} > n_{crit}\end{cases} - 0.5\cdot N_{f}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - N_{r}\cdot Q_{10}^{\frac{T_{a}}{10}}\cdot R_{0} - R_{c}\right)\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_6');ausklappen('rhs_6')">@Murty2000EcologicalModelling</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Wang2010Biogeosciences/Thumbnail.svg"> </td><td align="left"><a href="Wang2010Biogeosciences/Report.html" target="_blank">CABLE</a></td>
<td align="center" onclick="ausklappen('comp_table_7');ausklappen('rhs_7')">10</td>
<td align="center" onclick="ausklappen('comp_table_7');ausklappen('rhs_7')">16</td>
<td align="center" onclick="ausklappen('comp_table_7');ausklappen('rhs_7')"></td>
<td align="center" onclick="ausklappen('comp_table_7');ausklappen('rhs_7')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_7" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{leaf}\\C_{root}\\C_{wood}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=F_{c}$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}a_{leaf}\\a_{root}\\a_{wood}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of turnover (cycling) rates</td>
<td align="center">$A=\left[\begin{matrix}-\mu_{leaf} & 0 & 0\\0 & -\mu_{root} & 0\\0 & 0 & -\mu_{wood}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_7');ausklappen('rhs_7')"><div id="rhs_7" style="display:none">$\left[\begin{matrix}- C_{leaf}\cdot\mu_{leaf} + F_{cmax}\cdot a_{leaf}\cdot\min\left(\frac{n_{leaf}}{k_{n} + n_{leaf}},\frac{p_{leaf}}{k_{p} + p_{leaf}}\right)\cdot\min\left(1,\frac{N_{min}}{\Delta_{t}\cdot F_{nupmin}},\frac{P_{lab}}{\Delta_{t}\cdot F_{pupmin}}\right)\\- C_{root}\cdot\mu_{root} + F_{cmax}\cdot a_{root}\cdot\min\left(\frac{n_{leaf}}{k_{n} + n_{leaf}},\frac{p_{leaf}}{k_{p} + p_{leaf}}\right)\cdot\min\left(1,\frac{N_{min}}{\Delta_{t}\cdot F_{nupmin}},\frac{P_{lab}}{\Delta_{t}\cdot F_{pupmin}}\right)\\- C_{wood}\cdot\mu_{wood} + F_{cmax}\cdot a_{wood}\cdot\min\left(\frac{n_{leaf}}{k_{n} + n_{leaf}},\frac{p_{leaf}}{k_{p} + p_{leaf}}\right)\cdot\min\left(1,\frac{N_{min}}{\Delta_{t}\cdot F_{nupmin}},\frac{P_{lab}}{\Delta_{t}\cdot F_{pupmin}}\right)\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_7');ausklappen('rhs_7')">@Wang2010Biogeosciences</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="King1993TreePhysiol/Thumbnail.svg"> </td><td align="left"><a href="King1993TreePhysiol/Report.html" target="_blank">King1993TreePhysiology</a></td>
<td align="center" onclick="ausklappen('comp_table_8');ausklappen('rhs_8')">5</td>
<td align="center" onclick="ausklappen('comp_table_8');ausklappen('rhs_8')">9</td>
<td align="center" onclick="ausklappen('comp_table_8');ausklappen('rhs_8')"></td>
<td align="center" onclick="ausklappen('comp_table_8');ausklappen('rhs_8')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_8" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}F\\R\\W\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=G$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}\eta_{f}\\\eta_{r}\\\eta_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of turnover (cycling) rates</td>
<td align="center">$A=\left[\begin{matrix}-\gamma_{f} & 0 & 0\\0 & -\gamma_{r} & 0\\0 & 0 & 0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_8');ausklappen('rhs_8')"><div id="rhs_8" style="display:none">$\left[\begin{matrix}- F\cdot\gamma_{f} +\Phi_{0}\cdot\epsilon\cdot\eta_{f}\cdot\left(1 - e^{- F\cdot k\cdot\omega}\right)\\\Phi_{0}\cdot\epsilon\cdot\eta_{r}\cdot\left(1 - e^{- F\cdot k\cdot\omega}\right) - R\cdot\gamma_{r}\\\Phi_{0}\cdot\epsilon\cdot\left(1 - e^{- F\cdot k\cdot\omega}\right)\cdot\left(-\eta_{f} -\eta_{r} + 1\right)\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_8');ausklappen('rhs_8')">@King1993TreePhysiology</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Arora2005GCB-1/Thumbnail.svg"> </td><td align="left"><a href="Arora2005GCB-1/Report.html" target="_blank">CTEM</a></td>
<td align="center" onclick="ausklappen('comp_table_9');ausklappen('rhs_9')">22</td>
<td align="center" onclick="ausklappen('comp_table_9');ausklappen('rhs_9')">23</td>
<td align="center" onclick="ausklappen('comp_table_9');ausklappen('rhs_9')"></td>
<td align="center" onclick="ausklappen('comp_table_9');ausklappen('rhs_9')">$f_{v}=u+A\cdot x$
<div id="comp_table_9" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{L}\\C_{S}\\C_{R}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">Vector of functions of photosynthetic inputs</td>
<td align="center">$u=\left[\begin{matrix}G - R_{mL}\\a_{S}\\a_{R}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of cycling rates</td>
<td align="center">$A=\left[\begin{matrix}-\gamma_{N} -\gamma_{T} -\gamma_{W} & 0 & 0\\0 & - R_{gS} - R_{mS} -\gamma_{S} & 0\\0 & 0 & - R_{gR} - R_{mR} -\gamma_{R}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_9');ausklappen('rhs_9')"><div id="rhs_9" style="display:none">$\left[\begin{matrix}C_{L}\cdot\left(-\gamma_{N} -\gamma_{Tmax}\cdot\left(-\beta_{T} + 1\right)^{b_{T}} -\gamma_{W}\right) + G - R_{mL}\\C_{S}\cdot\left(- R_{gS} - R_{mS} -\gamma_{S}\right) +\frac{\epsilon_{S} +\omega\cdot\left(1 - e^{- LAI\cdot k_{n}}\right)}{\omega\cdot\left(- W + 2 - e^{- LAI\cdot k_{n}}\right) + 1}\\C_{R}\cdot\left(- R_{gR} - R_{mR} -\gamma_{R}\right) +\frac{-\epsilon_{L} -\epsilon_{S} +\omega\cdot\left(- W + 1\right) + 1}{\omega\cdot\left(- W + 2 - e^{- LAI\cdot k_{n}}\right) + 1}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_9');ausklappen('rhs_9')">@Arora2005GlobalChangeBiology</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Fontaine2005Ecologyletters/Thumbnail.svg"> </td><td align="left"><a href="Fontaine2005Ecologyletters/Report.html" target="_blank">FB2005 (4)</a></td>
<td align="center" onclick="ausklappen('comp_table_10');ausklappen('rhs_10')">5</td>
<td align="center" onclick="ausklappen('comp_table_10');ausklappen('rhs_10')">12</td>
<td align="center" onclick="ausklappen('comp_table_10');ausklappen('rhs_10')"></td>
<td align="center" onclick="ausklappen('comp_table_10');ausklappen('rhs_10')">$f_{s}=I+A_{GM}\cdot C$
<div id="comp_table_10" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}0\\\Phi_{l}\\0\\0\\\Phi_{i} -\Phi_{o} -\Phi_{up}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}C_{s}\\C_{f}\\C_{ds}\\C_{df}\\N\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A_{GM}$</td>
<td align="left">decomposition operator</td>
<td align="center">$A_{GM}=\left[\begin{matrix}-\frac{A}{C_{s}}\cdot C_{ds} & 0 & s & s & 0\\0 & - y & 0 & -\frac{\alpha\cdot r}{\alpha -\beta} & -\frac{i}{\alpha -\beta}\\\frac{A}{C_{s}}\cdot C_{ds} & y & - r - s & 0 & 0\\0 & 0 & 0 &\frac{\alpha\cdot r}{\alpha -\beta} - r - s &\frac{i}{\alpha -\beta}\\0 & y\cdot\left(-\alpha +\beta\right) &\alpha\cdot r & 0 & - i\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+A_{GM}\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_10');ausklappen('rhs_10')"><div id="rhs_10" style="display:none">$\left[\begin{matrix}- A\cdot C_{ds} + C_{df}\cdot s + C_{ds}\cdot s\\-\frac{C_{df}\cdot\alpha\cdot r}{\alpha -\beta} - C_{f}\cdot y -\frac{N\cdot i}{\alpha -\beta} +\Phi_{l}\\A\cdot C_{ds} + C_{ds}\cdot\left(- r - s\right) + C_{f}\cdot y\\C_{df}\cdot\left(\frac{\alpha\cdot r}{\alpha -\beta} - r - s\right) +\frac{N\cdot i}{\alpha -\beta}\\C_{ds}\cdot\alpha\cdot r + C_{f}\cdot y\cdot\left(-\alpha +\beta\right) - N\cdot i +\Phi_{i} -\Phi_{o} -\Phi_{up}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_10');ausklappen('rhs_10')">@Fontaine2005Ecologyletters</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Henin1945Annalesagronomiques/Thumbnail.svg"> </td><td align="left"><a href="Henin1945Annalesagronomiques/Report.html" target="_blank">Henin's model</a></td>
<td align="center" onclick="ausklappen('comp_table_11');ausklappen('rhs_11')">2</td>
<td align="center" onclick="ausklappen('comp_table_11');ausklappen('rhs_11')">4</td>
<td align="center" onclick="ausklappen('comp_table_11');ausklappen('rhs_11')"></td>
<td align="center" onclick="ausklappen('comp_table_11');ausklappen('rhs_11')">$f_{s}=I+A_{GeM}\cdot C$
<div id="comp_table_11" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}A\\B\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}m\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A_{GeM}$</td>
<td align="left">decomposition operator</td>
<td align="center">$A_{GeM}=\left[\begin{matrix}-\alpha & 0\\K\cdot\alpha & -\beta\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+A_{GeM}\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_11');ausklappen('rhs_11')"><div id="rhs_11" style="display:none">$\left[\begin{matrix}- A\cdot\alpha + m\\A\cdot K\cdot\alpha - B\cdot\beta\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_11');ausklappen('rhs_11')">@Henin1945Annalesagronomiques</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Wang2013EcologicalApplications/Thumbnail.svg"> </td><td align="left"><a href="Wang2013EcologicalApplications/Report.html" target="_blank">MEND</a></td>
<td align="center" onclick="ausklappen('comp_table_12');ausklappen('rhs_12')">7</td>
<td align="center" onclick="ausklappen('comp_table_12');ausklappen('rhs_12')">19</td>
<td align="center" onclick="ausklappen('comp_table_12');ausklappen('rhs_12')"></td>
<td align="center" onclick="ausklappen('comp_table_12');ausklappen('rhs_12')">$f_{s}=I+T\cdot N\cdot C$
<div id="comp_table_12" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}P\\M\\Q\\B\\D\\EP\\EM\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}I_{P}\\0\\0\\0\\I_{D}\\0\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$T$</td>
<td align="left">transition operator</td>
<td align="center">$T=\left[\begin{matrix}-1 & 0 & 0 &\frac{F_{E}}{F_{E} + F_{R}}\cdot\left(- g_{D} + 1\right)\cdot\left(- p_{EM} - p_{EP} + 1\right) & 0 & 0 & 0\\- f_{D} + 1 & -1 & 0 & 0 & 0 & 0 & 0\\0 & 0 & -1 & 0 &\frac{F_{A}}{F_{A} + F_{U}} & 0 & 0\\0 & 0 & 0 & -1 &\frac{F_{U}}{F_{A} + F_{U}} & 0 & 0\\f_{D} & 1 & 1 &\frac{F_{E}\cdot g_{D}}{F_{E} + F_{R}}\cdot\left(- p_{EM} - p_{EP} + 1\right) & -1 & 1 & 1\\0 & 0 & 0 &\frac{F_{E}\cdot p_{EP}}{F_{E} + F_{R}} & 0 & -1 & 0\\0 & 0 & 0 &\frac{F_{E}\cdot p_{EM}}{F_{E} + F_{R}} & 0 & 0 & -1\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$N$</td>
<td align="left">decomposition operator</td>
<td align="center">$N=\left[\begin{matrix}\frac{EP\cdot V_{P}}{K_{P} + P} & 0 & 0 & 0 & 0 & 0 & 0\\0 &\frac{EM\cdot V_{M}}{K_{M} + M} & 0 & 0 & 0 & 0 & 0\\0 & 0 &\frac{K_{des}}{Q_{max}} & 0 & 0 & 0 & 0\\0 & 0 & 0 & F_{E} + F_{R} & 0 & 0 & 0\\0 & 0 & 0 & 0 & F_{A} + F_{U} & 0 & 0\\0 & 0 & 0 & 0 & 0 & r_{EP} & 0\\0 & 0 & 0 & 0 & 0 & 0 & r_{EM}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+T\cdot N\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_12');ausklappen('rhs_12')"><div id="rhs_12" style="display:none">$\left[\begin{matrix}B\cdot m_{R}\cdot\left(- g_{D} + 1\right)\cdot\left(- p_{EM} - p_{EP} + 1\right) -\frac{EP\cdot P\cdot V_{P}}{K_{P} + P} + I_{P}\\-\frac{EM\cdot M\cdot V_{M}}{K_{M} + M} +\frac{EP\cdot P\cdot V_{P}}{K_{P} + P}\cdot\left(- f_{D} + 1\right)\\D\cdot K_{ads}\cdot\left(-\frac{Q}{Q_{max}} + 1\right) -\frac{K_{des}}{Q_{max}}\cdot Q\\\frac{B\cdot D\cdot\left(V_{D} + m_{R}\right)}{E_{C}\cdot\left(D + K_{D}\right)} + B\cdot\left(-\frac{D}{D + K_{D}}\cdot\left(-1 +\frac{1}{E_{C}}\right)\cdot\left(V_{D} + m_{R}\right) - m_{R}\right)\\B\cdot g_{D}\cdot m_{R}\cdot\left(- p_{EM} - p_{EP} + 1\right) + D\cdot\left(-\frac{B\cdot\left(V_{D} + m_{R}\right)}{E_{C}\cdot\left(D + K_{D}\right)} - K_{ads}\cdot\left(-\frac{Q}{Q_{max}} + 1\right)\right) +\frac{EM\cdot M\cdot V_{M}}{K_{M} + M} + EM\cdot r_{EM} +\frac{EP\cdot P\cdot V_{P}}{K_{P} + P}\cdot f_{D} + EP\cdot r_{EP} + I_{D} +\frac{K_{des}}{Q_{max}}\cdot Q\\B\cdot m_{R}\cdot p_{EP} - EP\cdot r_{EP}\\B\cdot m_{R}\cdot p_{EM} - EM\cdot r_{EM}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_12');ausklappen('rhs_12')">@Wang2013EcologicalApplications</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Castanho2013Biogeosciences/Thumbnail.svg"> </td><td align="left"><a href="Castanho2013Biogeosciences/Report.html" target="_blank">IBIS</a></td>
<td align="center" onclick="ausklappen('comp_table_13');ausklappen('rhs_13')">5</td>
<td align="center" onclick="ausklappen('comp_table_13');ausklappen('rhs_13')">3</td>
<td align="center" onclick="ausklappen('comp_table_13');ausklappen('rhs_13')"></td>
<td align="center" onclick="ausklappen('comp_table_13');ausklappen('rhs_13')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_13" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{il}\\C_{is}\\C_{ir}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=NPP_{i}$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}a_{il}\\a_{is}\\a_{ir}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of turnover (cycling) rates</td>
<td align="center">$A=\left[\begin{matrix}-\frac{1}{\tau_{il}} & 0 & 0\\0 & -\frac{1}{\tau_{is}} & 0\\0 & 0 & -\frac{1}{\tau_{ir}}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_13');ausklappen('rhs_13')"><div id="rhs_13" style="display:none">$\left[\begin{matrix}-\frac{C_{il}}{\tau_{il}} + NPP_{i}\cdot\left(- 0.0025\cdot S + 0.44\right)\\-\frac{C_{is}}{\tau_{is}} + NPP_{i}\cdot\left(- 0.0014\cdot S + 0.423\right)\\-\frac{C_{ir}}{\tau_{ir}} + NPP_{i}\cdot\left(0.0039\cdot S + 0.137\right)\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_13');ausklappen('rhs_13')">@Castanho2013Biogeosciences</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Comins1993EA/Thumbnail.svg"> </td><td align="left"><a href="Comins1993EA/Report.html" target="_blank">G'DAY</a></td>
<td align="center" onclick="ausklappen('comp_table_14');ausklappen('rhs_14')">4</td>
<td align="center" onclick="ausklappen('comp_table_14');ausklappen('rhs_14')">6</td>
<td align="center" onclick="ausklappen('comp_table_14');ausklappen('rhs_14')"></td>
<td align="center" onclick="ausklappen('comp_table_14');ausklappen('rhs_14')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_14" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}F\\R\\W\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=G$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}\eta_{f}\\\eta_{r}\\\eta_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of senescence (cycling) rates</td>
<td align="center">$A=\left[\begin{matrix}-\gamma_{f} & 0 & 0\\0 & -\gamma_{r} & 0\\0 & 0 & -\gamma_{w}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_14');ausklappen('rhs_14')"><div id="rhs_14" style="display:none">$\left[\begin{matrix}- F\cdot\gamma_{f} + G\cdot\eta_{f}\\G\cdot\eta_{r} - R\cdot\gamma_{r}\\G\cdot\eta_{w} - W\cdot\gamma_{w}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_14');ausklappen('rhs_14')">@Comins1993Ecological_Applications</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Hilbert1991AnnBot/Thumbnail.svg"> </td><td align="left"><a href="Hilbert1991AnnBot/Report.html" target="_blank">Hilbert1991Annals_of_Botany</a></td>
<td align="center" onclick="ausklappen('comp_table_15');ausklappen('rhs_15')">21</td>
<td align="center" onclick="ausklappen('comp_table_15');ausklappen('rhs_15')">19</td>
<td align="center" onclick="ausklappen('comp_table_15');ausklappen('rhs_15')"></td>
<td align="center" onclick="ausklappen('comp_table_15');ausklappen('rhs_15')">$f_{v}=u\cdot b+A_{x}\cdot x$
<div id="comp_table_15" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}W_{N}\\W_{C}\\W_{p}\\W_{s}\\W_{r}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=\left[\begin{matrix}A\cdot\sigma_{c}\\W_{r}\cdot\sigma_{r}\\0\\0\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">partitioning coefficient of system inputs</td>
<td align="center">$b=1$</td>
</tr>
<tr>
<td align="center">$A_{x}$</td>
<td align="left">matrix of turnover (cycling) rates</td>
<td align="center">$A_{x}=\left[\begin{matrix}\frac{W_{N}}{W_{g}^{2}}\cdot\kappa\cdot\left(- W_{p}\cdot f_{cp}\cdot\lambda_{p} - W_{r}\cdot f_{cr}\cdot\lambda_{r} - W_{s}\cdot f_{cs}\cdot\lambda_{s}\right) & 0 & 0 & 0 & 0\\0 &\frac{W_{C}}{W_{g}^{2}}\cdot\kappa\cdot\left(- W_{p}\cdot f_{np}\cdot\lambda_{p} - W_{r}\cdot f_{nr}\cdot\lambda_{r} - W_{s}\cdot f_{ns}\cdot\lambda_{s}\right) & 0 & 0 & 0\\0 &\frac{N}{W_{g}}\cdot W_{p}\cdot\kappa\cdot\lambda_{p} & 0 & 0 & 0\\0 &\frac{N}{W_{g}}\cdot W_{s}\cdot\kappa\cdot\lambda_{s} & 0 & 0 & 0\\0 &\frac{N}{W_{g}}\cdot W_{r}\cdot\kappa\cdot\lambda_{r} & 0 & 0 & 0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A_{x}\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_15');ausklappen('rhs_15')"><div id="rhs_15" style="display:none">$\left[\begin{matrix}\frac{W_{N}^{2}\cdot\kappa}{\left(W_{p} + W_{r} + W_{s}\right)^{2}}\cdot\left(-\frac{W_{p}\cdot f_{cp}}{2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}} -\frac{W_{r}\cdot f_{cr}}{2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}} -\frac{I_{dens}\cdot W_{r}\cdot f_{cs}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot\left(2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}\right)\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}\right) +\frac{W_{s}}{I_{dens}\cdot h_{max}\cdot\rho}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)\\\frac{W_{C}^{2}\cdot\kappa}{\left(W_{p} + W_{r} + W_{s}\right)^{2}}\cdot\left(-\frac{W_{p}\cdot f_{np}}{2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}} -\frac{W_{r}\cdot f_{nr}}{2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}} -\frac{I_{dens}\cdot W_{r}\cdot f_{ns}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot\left(2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}\right)\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}\right) + W_{r}\cdot\sigma_{r}\\\frac{W_{C}\cdot W_{N}\cdot W_{p}\cdot\kappa}{\left(2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}\right)\cdot\left(W_{p} + W_{r} + W_{s}\right)^{2}}\\\frac{I_{dens}\cdot W_{C}\cdot W_{N}\cdot W_{r}\cdot h_{max}\cdot\kappa\cdot\rho\cdot\sigma_{r}}{B\cdot\left(2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}\right)\cdot\left(I_{dens} + h_{half}\right)\cdot\left(W_{p} + W_{r} + W_{s}\right)^{2}\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}\\\frac{W_{C}\cdot W_{N}\cdot W_{r}\cdot\kappa}{\left(2 +\frac{I_{dens}\cdot W_{r}\cdot h_{max}\cdot\rho\cdot\sigma_{r}}{B\cdot W_{s}\cdot\left(I_{dens} + h_{half}\right)\cdot\min\left(-\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{1}{C_{i} + 827}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{35.76\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 12.42\right) + 0.238, -\frac{0.775\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho +\frac{I_{dens}\cdot\left(C_{i} - 31\right)\cdot\left(\frac{92.55\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + 13.85\right)}{\left(4.5\cdot C_{i} + 325.5\right)\cdot\left(\frac{194.355\cdot I_{dens}\cdot W_{p}\cdot f_{np}\cdot h_{max}}{W_{s}\cdot\left(I_{dens} + h_{half}\right)}\cdot\rho + I_{dens} + 29.085\right)} + 0.238\right)}\right)\cdot\left(W_{p} + W_{r} + W_{s}\right)^{2}}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_15');ausklappen('rhs_15')">@Hilbert1991Annals_of_Botany</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Schimel2003SoilBiologyandBiochemistry/Thumbnail.svg"> </td><td align="left"><a href="Schimel2003SoilBiologyandBiochemistry/Report.html" target="_blank">Exoenzyme</a></td>
<td align="center" onclick="ausklappen('comp_table_16');ausklappen('rhs_16')">4</td>
<td align="center" onclick="ausklappen('comp_table_16');ausklappen('rhs_16')">7</td>
<td align="center" onclick="ausklappen('comp_table_16');ausklappen('rhs_16')"></td>
<td align="center" onclick="ausklappen('comp_table_16');ausklappen('rhs_16')">$f_{s}=T\cdot N\cdot C$
<div id="comp_table_16" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}S\\D\\M\\E\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$T$</td>
<td align="left">transition operator</td>
<td align="center">$T=\left[\begin{matrix}-1 & 0 & 0 & 0\\1 & -1 &\frac{K_{r}\cdot k_{t}}{SUE\cdot k_{m} + k_{t}} & 0\\0 & - K_{e} + SUE & -1 & 0\\0 & K_{e} & 0 & -1\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$N$</td>
<td align="left">decomposition operator</td>
<td align="center">$N=\left[\begin{matrix}\frac{E}{S}\cdot k_{d} & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & SUE\cdot k_{m} + k_{t} & 0\\0 & 0 & 0 & k_{l}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=T\cdot N\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_16');ausklappen('rhs_16')"><div id="rhs_16" style="display:none">$\left[\begin{matrix}- E\cdot k_{d}\\- D + E\cdot k_{d} + K_{r}\cdot M\cdot k_{t}\\D\cdot\left(- K_{e} + SUE\right) + M\cdot\left(- SUE\cdot k_{m} - k_{t}\right)\\D\cdot K_{e} - E\cdot k_{l}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_16');ausklappen('rhs_16')">@Schimel2003SoilBiologyandBiochemistry</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Allison2010NatureGeoscience/Thumbnail.svg"> </td><td align="left"><a href="Allison2010NatureGeoscience/Report.html" target="_blank">AWB</a></td>
<td align="center" onclick="ausklappen('comp_table_17');ausklappen('rhs_17')">11</td>
<td align="center" onclick="ausklappen('comp_table_17');ausklappen('rhs_17')">16</td>
<td align="center" onclick="ausklappen('comp_table_17');ausklappen('rhs_17')"></td>
<td align="center" onclick="ausklappen('comp_table_17');ausklappen('rhs_17')">$f_{s}=I+T_{M}\cdot N\cdot C$
<div id="comp_table_17" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}S\\D\\B\\E\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}I_{S}\\I_{D}\\0\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$T_{M}$</td>
<td align="left">transition operator</td>
<td align="center">$T_{M}=\left[\begin{matrix}-1 & 0 &\frac{a_{BS}\cdot r_{B}}{r_{B} + r_{E}} & 0\\1 & -1 &\frac{r_{B}\cdot\left(- a_{BS} + 1\right)}{r_{B} + r_{E}} & 1\\1 & E_{C} & -1 & 0\\0 & 0 &\frac{r_{E}}{r_{B} + r_{E}} & -1\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$N$</td>
<td align="left">decomposition operator</td>
<td align="center">$N=\left[\begin{matrix}\frac{E\cdot V}{K + S} & 0 & 0 & 0\\0 &\frac{B\cdot V_{U}}{D + K_{U}} & 0 & 0\\0 & 0 & r_{B} + r_{E} & 0\\0 & 0 & 0 & r_{L}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+T_{M}\cdot N\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_17');ausklappen('rhs_17')"><div id="rhs_17" style="display:none">$\left[\begin{matrix}B\cdot a_{BS}\cdot r_{B} -\frac{E\cdot S\cdot V_{max}\cdot e^{-\frac{E_{a}}{0.008314\cdot T + 2.269722}}}{K_{0} + K_{s}\cdot T + S} + I_{S}\\-\frac{B\cdot D\cdot V_{Umax}\cdot e^{-\frac{E_{aU}}{0.008314\cdot T + 2.269722}}}{D + K_{U0} + K_{Us}\cdot T} + B\cdot r_{B}\cdot\left(- a_{BS} + 1\right) +\frac{E\cdot S\cdot V_{max}\cdot e^{-\frac{E_{a}}{0.008314\cdot T + 2.269722}}}{K_{0} + K_{s}\cdot T + S} + E\cdot r_{L} + I_{D}\\\frac{B\cdot D\cdot V_{Umax}\cdot e^{-\frac{E_{aU}}{0.008314\cdot T + 2.269722}}}{D + K_{U0} + K_{Us}\cdot T}\cdot\left(T\cdot\epsilon_{s} +\epsilon_{0}\right) + B\cdot\left(- r_{B} - r_{E}\right) +\frac{E\cdot S\cdot V_{max}\cdot e^{-\frac{E_{a}}{0.008314\cdot T + 2.269722}}}{K_{0} + K_{s}\cdot T + S}\\B\cdot r_{E} - E\cdot r_{L}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_17');ausklappen('rhs_17')">@Allison2010NatureGeoscience</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Williams2005GCB/Thumbnail.svg"> </td><td align="left"><a href="Williams2005GCB/Report.html" target="_blank">DALEC</a></td>
<td align="center" onclick="ausklappen('comp_table_18');ausklappen('rhs_18')">9</td>
<td align="center" onclick="ausklappen('comp_table_18');ausklappen('rhs_18')">10</td>
<td align="center" onclick="ausklappen('comp_table_18');ausklappen('rhs_18')"></td>
<td align="center" onclick="ausklappen('comp_table_18');ausklappen('rhs_18')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_18" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states of vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{f}\\C_{lab}\\C_{w}\\C_{r}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=NPP$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}multtl\cdot p_{3}\\0\\- p_{4} + 1\\p_{4}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of cycling rates</td>
<td align="center">$A=\left[\begin{matrix}- T_{rate}\cdot multtf\cdot p_{16}\cdot p_{5}\cdot\left(- p_{14} + 1\right) - T_{rate}\cdot multtf\cdot p_{5}\cdot\left(- p_{14} + 1\right)\cdot\left(- p_{16} + 1\right) - multtf\cdot p_{14}\cdot p_{5} & T_{rate}\cdot multtl\cdot p_{15}\cdot\left(- p_{16} + 1\right) & 0 & 0\\T_{rate}\cdot multtf\cdot p_{5}\cdot\left(- p_{14} + 1\right)\cdot\left(- p_{16} + 1\right) & - T_{rate}\cdot multtl\cdot p_{15}\cdot p_{16} - T_{rate}\cdot multtl\cdot p_{15}\cdot\left(- p_{16} + 1\right) & 0 & 0\\0 & 0 & - p_{6} & 0\\0 & 0 & 0 & - p_{7}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_18');ausklappen('rhs_18')"><div id="rhs_18" style="display:none">$\left[\begin{matrix}C_{f}\cdot\left(- multtf\cdot p_{14}\cdot p_{5} - 0.5\cdot multtf\cdot p_{16}\cdot p_{5}\cdot\left(- p_{14} + 1\right)\cdot e^{0.5\cdot p_{10}\cdot\left(maxt + mint\right)} - 0.5\cdot multtf\cdot p_{5}\cdot\left(- p_{14} + 1\right)\cdot\left(- p_{16} + 1\right)\cdot e^{0.5\cdot p_{10}\cdot\left(maxt + mint\right)}\right) + 0.5\cdot C_{lab}\cdot multtl\cdot p_{15}\cdot\left(- p_{16} + 1\right)\cdot e^{0.5\cdot p_{10}\cdot\left(maxt + mint\right)} + NPP\cdot multtl\cdot p_{3}\\0.5\cdot C_{f}\cdot multtf\cdot p_{5}\cdot\left(- p_{14} + 1\right)\cdot\left(- p_{16} + 1\right)\cdot e^{0.5\cdot p_{10}\cdot\left(maxt + mint\right)} + C_{lab}\cdot\left(- 0.5\cdot multtl\cdot p_{15}\cdot p_{16}\cdot e^{0.5\cdot p_{10}\cdot\left(maxt + mint\right)} - 0.5\cdot multtl\cdot p_{15}\cdot\left(- p_{16} + 1\right)\cdot e^{0.5\cdot p_{10}\cdot\left(maxt + mint\right)}\right)\\- C_{w}\cdot p_{6} + NPP\cdot\left(- p_{4} + 1\right)\\- C_{r}\cdot p_{7} + NPP\cdot p_{4}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_18');ausklappen('rhs_18')">@Williams2005GlobalChangeBiology</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Jenkinson1977SoilScience/Thumbnail.svg"> </td><td align="left"><a href="Jenkinson1977SoilScience/Report.html" target="_blank">RothC-26.3</a></td>
<td align="center" onclick="ausklappen('comp_table_19');ausklappen('rhs_19')">5</td>
<td align="center" onclick="ausklappen('comp_table_19');ausklappen('rhs_19')">7</td>
<td align="center" onclick="ausklappen('comp_table_19');ausklappen('rhs_19')"></td>
<td align="center" onclick="ausklappen('comp_table_19');ausklappen('rhs_19')">$f_{s}=I+\xi\cdot A\cdot C$
<div id="comp_table_19" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}C_{1}\\C_{2}\\C_{3}\\C_{4}\\C_{5}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}J\cdot\gamma\\J\cdot\left(-\gamma + 1\right)\\0\\0\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$\xi$</td>
<td align="left">environmental effects multiplier</td>
<td align="center">$\xi=f_{T}\cdot f_{W}$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">decomposition operator</td>
<td align="center">$A=\left[\begin{matrix}- k_{1} & 0 & 0 & 0 & 0\\0 & - k_{2} & 0 & 0 & 0\\a\cdot k_{1} & a\cdot k_{2} & a\cdot k_{3} - k_{3} & a\cdot k_{4} & 0\\b\cdot k_{1} & b\cdot k_{2} & b\cdot k_{3} & b\cdot k_{4} - k_{4} & 0\\0 & 0 & 0 & 0 & 0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+\xi\cdot A\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_19');ausklappen('rhs_19')"><div id="rhs_19" style="display:none">$\left[\begin{matrix}- C_{1}\cdot f_{T}\cdot f_{W}\cdot k_{1} +\frac{DR\cdot J}{DR + 1}\\- C_{2}\cdot f_{T}\cdot f_{W}\cdot k_{2} + J\cdot\left(-\frac{DR}{DR + 1} + 1\right)\\\frac{0.46\cdot C_{1}\cdot f_{T}\cdot f_{W}\cdot k_{1}}{4.0895 + 2.672\cdot e^{- 0.0786\cdot pClay}} +\frac{0.46\cdot C_{2}\cdot f_{T}\cdot f_{W}\cdot k_{2}}{4.0895 + 2.672\cdot e^{- 0.0786\cdot pClay}} + C_{3}\cdot f_{T}\cdot f_{W}\cdot\left(- k_{3} +\frac{0.46\cdot k_{3}}{4.0895 + 2.672\cdot e^{- 0.0786\cdot pClay}}\right) +\frac{0.46\cdot C_{4}\cdot f_{T}\cdot f_{W}\cdot k_{4}}{4.0895 + 2.672\cdot e^{- 0.0786\cdot pClay}}\\\frac{0.54\cdot C_{1}\cdot f_{T}\cdot f_{W}\cdot k_{1}}{4.0895 + 2.672\cdot e^{- 0.0786\cdot pClay}} +\frac{0.54\cdot C_{2}\cdot f_{T}\cdot f_{W}\cdot k_{2}}{4.0895 + 2.672\cdot e^{- 0.0786\cdot pClay}} +\frac{0.54\cdot C_{3}\cdot f_{T}\cdot f_{W}\cdot k_{3}}{4.0895 + 2.672\cdot e^{- 0.0786\cdot pClay}} + C_{4}\cdot f_{T}\cdot f_{W}\cdot\left(- k_{4} +\frac{0.54\cdot k_{4}}{4.0895 + 2.672\cdot e^{- 0.0786\cdot pClay}}\right)\\0\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_19');ausklappen('rhs_19')">@Jenkinson1977SoilScience</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Foley1996GBC/Thumbnail.svg"> </td><td align="left"><a href="Foley1996GBC/Report.html" target="_blank">IBIS</a></td>
<td align="center" onclick="ausklappen('comp_table_20');ausklappen('rhs_20')">4</td>
<td align="center" onclick="ausklappen('comp_table_20');ausklappen('rhs_20')">6</td>
<td align="center" onclick="ausklappen('comp_table_20');ausklappen('rhs_20')"></td>
<td align="center" onclick="ausklappen('comp_table_20');ausklappen('rhs_20')">$f_{v}=u\cdot b+A\cdot x$
<div id="comp_table_20" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$x$</td>
<td align="left">vector of states for vegetation</td>
<td align="center">$x=\left[\begin{matrix}C_{il}\\C_{is}\\C_{ir}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$u$</td>
<td align="left">scalar function of photosynthetic inputs</td>
<td align="center">$u=NPP_{i}$</td>
</tr>
<tr>
<td align="center">$b$</td>
<td align="left">vector of partitioning coefficients of photosynthetically fixed carbon</td>
<td align="center">$b=\left[\begin{matrix}a_{il}\\a_{is}\\a_{ir}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">matrix of turnover (cycling) rates</td>
<td align="center">$A=\left[\begin{matrix}-\frac{1}{\tau_{il}} & 0 & 0\\0 & -\frac{1}{\tau_{is}} & 0\\0 & 0 & -\frac{1}{\tau_{ir}}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{v}$</td>
<td align="left">the righthandside of the ode</td>
<td align="center">$f_{v}=u\cdot b+A\cdot x$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_20');ausklappen('rhs_20')"><div id="rhs_20" style="display:none">$\left[\begin{matrix}-\frac{C_{il}}{\tau_{il}} + a_{il}\cdot t\cdot\left(-\eta + 1\right)\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{- T_{0} + 15}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{- T_{0} + 15}\right)} - V_{m}\cdot\gamma +\min\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)},\frac{Q_{p}\cdot\alpha_{3}}{C_{i} +\frac{O_{2}}{\tau}}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right), 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\right)\\-\frac{C_{is}}{\tau_{is}} + a_{is}\cdot t\cdot\left(-\eta + 1\right)\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{- T_{0} + 15}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{- T_{0} + 15}\right)} - V_{m}\cdot\gamma +\min\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)},\frac{Q_{p}\cdot\alpha_{3}}{C_{i} +\frac{O_{2}}{\tau}}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right), 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\right)\\-\frac{C_{ir}}{\tau_{ir}} + a_{ir}\cdot t\cdot\left(-\eta + 1\right)\cdot\left(- B_{root}\cdot C_{ir}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{soil}} +\frac{1}{- T_{0} + 15}\right)} - B_{stem}\cdot C_{is}\cdot\lambda_{sapwood}\cdot e^{E_{0}\cdot\left(-\frac{1}{- T_{0} + T_{stem}} +\frac{1}{- T_{0} + 15}\right)} - V_{m}\cdot\gamma +\min\left(\frac{V_{m}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right)}{C_{i} + K_{c}\cdot\left(1 +\frac{O_{2}}{K_{o}}\right)},\frac{Q_{p}\cdot\alpha_{3}}{C_{i} +\frac{O_{2}}{\tau}}\cdot\left(C_{i} -\frac{O_{2}}{2\cdot\tau}\right), 0.365853658536585\cdot V_{m}\cdot\left(1 -\frac{O_{2}}{2\cdot C_{i}\cdot\tau}\right) +\frac{J_{p}\cdot O_{2}}{2\cdot C_{i}\cdot\tau}\right)\right)\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_20');ausklappen('rhs_20')">@Foley1996GlobalBiogeochemicalCycles</td>
</tr>
<tbody>
<tr class="odd">
<td align="left"><img src="Zelenev2000MicrobialEcology/Thumbnail.svg"> </td><td align="left"><a href="Zelenev2000MicrobialEcology/Report.html" target="_blank">BACWAVE</a></td>
<td align="center" onclick="ausklappen('comp_table_21');ausklappen('rhs_21')">5</td>
<td align="center" onclick="ausklappen('comp_table_21');ausklappen('rhs_21')">10</td>
<td align="center" onclick="ausklappen('comp_table_21');ausklappen('rhs_21')"></td>
<td align="center" onclick="ausklappen('comp_table_21');ausklappen('rhs_21')">$f_{s}=I+T\cdot N\cdot C$
<div id="comp_table_21" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}X\\S\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}0\\BGF + Exu\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$T$</td>
<td align="left">transition operator</td>
<td align="center">$T=\left[\begin{matrix}-1 & Y\\K_{r} & -1\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$N$</td>
<td align="left">decomposition operator</td>
<td align="center">$N=\left[\begin{matrix}\frac{D_{max}\cdot K_{d}}{K_{d} +\frac{S}{\theta}} & 0\\0 &\frac{X\cdot\mu_{max}}{Y\cdot\left(K_{s}\cdot\theta + S\right)}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+T\cdot N\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_21');ausklappen('rhs_21')"><div id="rhs_21" style="display:none">$\left[\begin{matrix}-\frac{D_{max}\cdot K_{d}\cdot X}{K_{d} +\frac{S}{\theta}} +\frac{S\cdot X\cdot\mu_{max}}{K_{s}\cdot\theta + S}\\BGF +\frac{D_{max}\cdot K_{d}\cdot K_{r}}{K_{d} +\frac{S}{\theta}}\cdot X + ExuM\cdot e^{- ExuT\cdot t} -\frac{S\cdot X\cdot\mu_{max}}{Y\cdot\left(K_{s}\cdot\theta + S\right)}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_21');ausklappen('rhs_21')">@Zelenev2000MicrobialEcology</td>
</tr>
<tbody>
<tr class="even">
<td align="left"><img src="Wang2014BG2p/Thumbnail.svg"> </td><td align="left"><a href="Wang2014BG2p/Report.html" target="_blank">Two-pool microbial</a></td>
<td align="center" onclick="ausklappen('comp_table_22');ausklappen('rhs_22')">2</td>
<td align="center" onclick="ausklappen('comp_table_22');ausklappen('rhs_22')">5</td>
<td align="center" onclick="ausklappen('comp_table_22');ausklappen('rhs_22')"></td>
<td align="center" onclick="ausklappen('comp_table_22');ausklappen('rhs_22')">$f_{s}=I+A\cdot C$
<div id="comp_table_22" style="display:none">
<table>
<tr class="header">
<th align="center">Component</th>
<th align="left">Description</th>
<th align="center">Expressions</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">$C$</td>
<td align="left">carbon content</td>
<td align="center">$C=\left[\begin{matrix}C_{s}\\C_{b}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$I$</td>
<td align="left">input vector</td>
<td align="center">$I=\left[\begin{matrix}F_{NPP}\\0\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$A$</td>
<td align="left">decomposition operator</td>
<td align="center">$A=\left[\begin{matrix}-\lambda &\mu_{b}\\\epsilon\cdot\lambda & -\mu_{b}\end{matrix}\right]$</td>
</tr>
<tr>
<td align="center">$f_{s}$</td>
<td align="left">the right hand side of the ode</td>
<td align="center">$f_{s}=I+A\cdot C$</td>
</tr>
</tbody>
</table>
</td>
</div>
<td align="center" style="vertical-align:middle" onclick="ausklappen('comp_table_22');ausklappen('rhs_22')"><div id="rhs_22" style="display:none">$\left[\begin{matrix}-\frac{C_{b}\cdot C_{s}\cdot V_{s}}{C_{s} + K_{s}} + C_{b}\cdot\mu_{b} + F_{NPP}\\\frac{C_{b}\cdot C_{s}\cdot V_{s}}{C_{s} + K_{s}}\cdot\epsilon - C_{b}\cdot\mu_{b}\end{matrix}\right]$</div></td>
<td align="left" onclick="ausklappen('comp_table_22');ausklappen('rhs_22')">@Wang2014BG</td>
</tr>
</tbody>
</table>

# Figures
