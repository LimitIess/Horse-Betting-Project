library(stats)
library(base)
library(dplyr)
library(mongolite)
library(tidyr)
library(readr)
library(ggplot2)


#Horses

#Read CSV file
horses <- read_csv("C:/Users/damia/Desktop/Betting/DVGB06Betting/DVGB06/Horses/Horse.csv")

#Quantitative values to analyze
quantitativevalueshorses <- list("age","saddle","positionL","dist","RPR","TR","OR","weight")


#For loop to summarize through methods mean, median, standarddeviation, IQR and MAD. Thereafter create a new variable.
for (item in quantitativevalueshorses){
  assign(paste0("Summarized_", item), (
         horses %>%
           summarise_at(vars(item),
                        list(mean=mean, median=median, Standarddeviation=sd, IQR=IQR, MAD=mad), na.rm=TRUE)))
}
#Plot for age
ggplot(data = horses,aes(age)) +
  geom_histogram(bins = 15, binwidth = 1)

#Plot for Saddle
ggplot(data = horses,aes(x = saddle)) +
  geom_histogram(bins = 15)

#Plot for  positionL, Limitation from 0 to 10, and smaller bin width to focus on the most frequent 
ggplot(data = horses,aes(x = positionL)) +
  geom_histogram(binwidth = 0.1) +
  xlim(NA,10)

#Plot for dist
ggplot(data = horses,aes(x = dist)) +
  geom_histogram(binwidth = 0.5)+
  xlim(NA, 50)

#Plot for RPR
ggplot(data = horses,aes(x = RPR)) +
  geom_histogram()

#Plot for TR
ggplot(data = horses,aes(x = TR)) +
  geom_histogram()

#Plot for OR
ggplot(data = horses,aes(x = OR)) +
  geom_histogram()

#Plot for weight
ggplot(data = horses,aes(x = weight)) +
  geom_histogram()+
  xlim(NA, 80)

ggplot(data = horses,aes(x = margin)) +
  geom_histogram()+
  xlim(NA,1.5)


#Races
#Import Races csv
races <- read_csv("C:/Users/damia/Desktop/Betting/DVGB06Betting/DVGB06/Races/Races.csv")

#List of columns to analyze
quantitativevaluesraces <- list("winningTime","prize","metric","hurdles","fences")

#For loop to summarize through methods mean, median, standarddeviation, IQR and MAD. Thereafter create a new variable.
for (item in quantitativevaluesraces){
  assign(paste0("Summarized_", item), (
    races %>%
      summarise_at(vars(item),
                   list(mean=mean, median=median, Standarddeviation=sd, IQR=IQR, MAD=mad), na.rm=TRUE)))
}


#Plot for rlcass
ggplot(data = races,aes(x = rclass)) +
  geom_histogram(stat = "count")


#Plot for ages
ggplot(data = races,aes(x = ages)) +
  geom_histogram(stat = "count")

#Plot for hurdles
ggplot(data = races,aes(x = hurdles)) +
  geom_bar()

#Plot for winningTime
ggplot(data = races,aes(x = winningTime)) +
  geom_histogram()+
  xlim(NA, 500)

#Plot for prize
ggplot(data = races,aes(x = prize)) +
  geom_histogram(bins = 20)

#Plot for metric
ggplot(data = races,aes(x = metric)) +
  geom_histogram(bins = 20)

#Plot for countryCode
ggplot(data = races,aes(x = countryCode)) +
  geom_histogram(stat = "count")

#Plot for fences
ggplot(data = races,aes(x = fences)) +
  geom_bar()


#Plot for month
ggplot(data = races,aes(x = Month)) +
  geom_histogram(stat = "count")



















#Work in progress
#for (item in quantitativevalues){
#  ggplot(data = horses[item], aes(x = item))+
#    geom_bar()
#}
#Read mongodb and set it to variable horses
#horses <- mongo(db = "HorsesDB",collection ="Horses", url = "mongodb://localhost")


#ggplot(gather(horses), aes(value)) + 
#  geom_bar() + 
#  facet_wrap(~key, scales = 'free_x')

#horses_summary <- horses %>%
#  summarise_at(vars("age","saddle","positionL","dist","RPR","TR","OR","weight"),
#               list(mean=mean, median=median, Standarddeviation=sd, IQR=IQR, MAD=mad), na.rm=TRUE)