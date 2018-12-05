
## The right hand side of the ODE
$\left[\begin{matrix}-\frac{D_{max}\cdot K_{d}\cdot X}{K_{d} +\frac{S}{\theta}} +\frac{S\cdot X\cdot\mu_{max}}{K_{s}\cdot\theta + S}\\BGF +\frac{D_{max}\cdot K_{d}\cdot K_{r}}{K_{d} +\frac{S}{\theta}}\cdot X + ExuM\cdot e^{- ExuT\cdot t} -\frac{S\cdot X\cdot\mu_{max}}{Y\cdot\left(K_{s}\cdot\theta + S\right)}\end{matrix}\right]$

## The Jacobian (derivative of the ODE w.r.t. state variables)
$\left[\begin{matrix}-\frac{D_{max}\cdot K_{d}}{K_{d} +\frac{S}{\theta}} +\frac{S\cdot\mu_{max}}{K_{s}\cdot\theta + S} &\frac{D_{max}\cdot K_{d}\cdot X}{\theta\cdot\left(K_{d} +\frac{S}{\theta}\right)^{2}} -\frac{S\cdot X\cdot\mu_{max}}{\left(K_{s}\cdot\theta + S\right)^{2}} +\frac{X\cdot\mu_{max}}{K_{s}\cdot\theta + S}\\\frac{D_{max}\cdot K_{d}\cdot K_{r}}{K_{d} +\frac{S}{\theta}} -\frac{S\cdot\mu_{max}}{Y\cdot\left(K_{s}\cdot\theta + S\right)} & -\frac{D_{max}\cdot K_{d}\cdot K_{r}\cdot X}{\theta\cdot\left(K_{d} +\frac{S}{\theta}\right)^{2}} +\frac{S\cdot X\cdot\mu_{max}}{Y\cdot\left(K_{s}\cdot\theta + S\right)^{2}} -\frac{X\cdot\mu_{max}}{Y\cdot\left(K_{s}\cdot\theta + S\right)}\end{matrix}\right]$
