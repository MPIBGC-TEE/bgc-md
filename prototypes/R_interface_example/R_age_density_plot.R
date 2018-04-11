# setwd("~/SOIL-R/Code/packageTests/bgc_md/bgc_md/R_interface_example")

# author: Holger Metzler
# date: 24/09/2016

if (!require("reshape2")) install.packages('rehsap2e')
if (!require("rgl")) install.packages('rgl')
library(plyr)

####### function definitions ############

# plot an age density
plot_age_density <- function(density, palette, alpha, age_stride = 1, time_stride = 1, add = FALSE){
  times <- unique(density$time)
  strided_times <- times[seq(1, length(times), age_stride)]
  if (strided_times[[length(strided_times)]] != times[[length(times)]]) strided_times <- append(strided_times, times[[length(times)]])
  
  ages <- unique(density$age)
  strided_ages <- ages[seq(1, length(ages), time_stride)]
  if (strided_ages[[length(strided_ages)]] != ages[[length(ages)]]) strided_ages <- append(strided_ages, ages[[length(ages)]])

  density <- density[density$time %in% strided_times & density$age %in% strided_ages,]

  ages <- unique(density$age)
  times <- unique(density$time)
  values = acast(density, formula = age ~ time)
  
  position <- outer(ages, times, function(a,b) a-b)
  nbcol <- length(times)
  jet.colors <- palette
  colors <- jet.colors(nbcol)
  
  # colors along the age-time diagonal
  poscol <- cut(position, nbcol)
  persp3d(ages, times, values, col = colors[poscol], alpha = alpha, add = add)

  density
}

find_z_value_for_age_and_time <- function(strided_density, ma, mt){
  if (is.nan(ma)) return(NaN)
  
  times <- unique(strided_density$time)
  ages <- unique(strided_density$age)
  
  lower_t <- tail(times[times<=mt], 1)
  upper_t <- head(times[times>=mt], 1)

  val_between <- function(t){
    lower_age <- tail(ages[ages<=ma], 1)
    upper_age <- head(ages[ages>=ma], 1)
    lower_value <- tail(strided_density[strided_density$time==t & strided_density$age<=ma, 'value'], 1)
    upper_value <- head(strided_density[strided_density$time==t & strided_density$age>=ma, 'value'], 1)
    
    if (is.nan(lower_value) | is.nan(upper_value)) return(NaN)
    
    if (upper_age != lower_age){
      value <- lower_value + (upper_value-lower_value)*(ma-lower_age)/(upper_age-lower_age)
    } else value <- lower_value
    value
  }
  
  lower_value <- val_between(lower_t)
  upper_value <- val_between(upper_t)
  if (is.nan(lower_value) | is.nan(upper_value)) return(NaN)
  
  if (upper_t != lower_t){
    value <- lower_value + (upper_value-lower_value)*(mt-lower_t)/(upper_t-lower_t)
  } else value <- lower_value
  
  value
}

set_aspect_ratio <- function(density){
  nr_times = length(unique(density$time))
  nr_ages = length(unique(density$age))
  total = nr_ages + nr_times
  aspect3d(nr_ages/total, nr_times/total,1)
}

plot_object <- function(title, density, mean = NULL, median = NULL, 
                        age_stride = 1, time_stride = 1, eq_surface = TRUE, alpha = 1, eq_alpha = 0.3, 
                        set_aspect = FALSE, save_html = TRUE){
  if (save_html){
    if (age_stride < 5) age_stride <- 5
    if (time_stride <5) time_stride <- 5
  }
  
  open3d(windowRect = c(20, 30, 800, 800))
  strided_density <- plot_age_density(density, palette = rainbow, alpha = alpha, 
                                      age_stride = age_stride, time_stride = time_stride)
  
  if (eq_surface){
    eq_density <- density
    times <- unique(eq_density$time)
    for (time in times) eq_density[eq_density$time==time, 'value'] <- eq_density[eq_density$time==times[[1]], 'value']
    
    plot_age_density(eq_density, palette = colorRampPalette(c("#000000FF", "#FFFFFFFF")), alpha = eq_alpha, 
                     age_stride = age_stride, time_stride = time_stride,
                     add = TRUE)
  }
  
  legend3d("topright", legend = title, inset=c(0.02))
  
  # mean lines
  if (!is.null(mean)){
    lines3d(mean$value, mean$time, 0, lwd=3, col="blue")
    lines3d(mean[mean$time==mean$time[[1]], 'value'], mean$time, 0, lwd = 3, col = 'black', alpha = 0.3)

    mean_dv <- sapply(1:nrow(mean), function(i){
      find_z_value_for_age_and_time(strided_density, mean$value[[i]], mean$time[[i]])
    })
    lines3d(mean$value, mean$time, mean_dv, lwd = 3, col = "blue")
   }
  
  # median lines
  if (!is.null(median)){
    lines3d(median$value, median$time, 0, lwd=3, col="red")
    lines3d(median[median$time==median$time[[1]], 'value'], median$time, 0, lwd = 3, col = 'black', alpha = 0.3)
    
    median_dv <- sapply(1:nrow(median), function(i){
      find_z_value_for_age_and_time(strided_density, median$value[[i]], median$time[[i]])
    })
    lines3d(median$value, median$time, median_dv, lwd=3, col="red")
  }
  
  if (set_aspect) set_aspect_ratio(density)
  
  # save html file
  if (save_html){
    if (age_stride < 5) age_stride <- 5
    if (time_stride <5) time_stride <- 5
    widget <- rglwidget()
    widget$width <- 800
    widget$height <- 800

    htmlwidgets::saveWidget(widget, paste0(gsub("\\s", "", title) , ".html"))
  }
}

########### main code ############

# plot age densities
age_density_data <- read.csv("age_dens.csv")
#age_mean_data <- read.csv("age_mean.csv")
age_median_data = read.csv("age_median.csv")

df1 = age_median_data[age_median_data$pool==-1,]
df2 = read.csv("system_age_median_ode.csv")

max(df1$value-df2$value)

pool_names <- c('Atmosphere', 'Terrestrial biosphere', 'Ocean surface layer')

for (pool in unique(age_density_data$pool)){
  age_density <- age_density_data[age_density_data$pool==pool, c('age', 'time', 'value')]

  if (pool == -1){
    title <- 'System age'
  } 
  else{
    title <- paste(pool_names[pool+1], ' age')
  }

  #age_mean <- age_mean_data[age_mean_data$pool==pool, c('time', 'value')]
  age_median <- age_median_data[age_median_data$pool==pool, c('time', 'value')]

  #plot_object(title, age_density, age_mean, age_median)
  plot_object(title, age_density, median = age_median)
}

# plot backward transit time density
btt_density <- read.csv("btt_dens.csv")
btt_mean <- read.csv("btt_mean.csv")
btt_median = read.csv("btt_median.csv")

title <- 'Backward Transit Time'
plot_object(title, btt_density, btt_mean, btt_median)

title <- 'Normalized Backward Transit Time'
#normalization needs to be done by dividing by r(t)


# plot forward transit time density
ftt_density <- read.csv("ftt_dens.csv")
ftt_median = read.csv("ftt_median.csv")

title <- 'Forward Transit Time'
# at time t0 ftt_density = NaN, remove it to be able to plot eq_density with value from time t0+1
ftt_density <- ftt_density[ftt_density$time!=ftt_density$time[[1]],]
ftt_median <- ftt_median[complete.cases(ftt_median),]
plot_object(title, ftt_density, median = ftt_median)

title <- 'Normalized Forward Transit Time'
# normalization needs to be done by dividing by u(t)
