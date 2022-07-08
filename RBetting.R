library(stats)
library(base)
library(dplyr)
library(mongolite)
library(tidyr)
library(readr)
library(ggplot2)


#Horses

#Read CSV file
horses <- read_csv("C:/Users/damia/Desktop/Betting/DVGB06/Horses/horses_2020cleaned.csv")

#Quantitative values to analyze
quantitativevalues <- list("age","saddle","positionL","dist","RPR","TR","OR","weight")



#For loop to summarize and create new variable with correct quantitative values
for (item in quantitativevalues){
  assign(paste0("Summarized_", item), (
         horses %>%
           summarise_at(vars(item),
                        list(mean=mean, median=median, Standarddeviation=sd, IQR=IQR, MAD=mad), na.rm=TRUE)))
  #ggplot(data = horses,aes(x = noquote(item))) +
  #  geom_bar()
  #ggplot(paste0(horses, item), aes(x ="item"))+
  #  geom_bar()
}
ggplot(data = horses,aes(x = age)) +
  geom_bar()


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