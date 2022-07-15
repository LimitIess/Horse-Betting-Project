library(stats)
library(base)
library(tidyr)
library(readr)
library(dplyr)
library(ggplot2)
library(corrplot)
library(PerformanceAnalytics)

#Races
#Read Races csv
races <- read_csv("C:/Users/damia/Desktop/Betting/DVGB06Betting/DVGB06/Horses/Horse.csv")

#Horses
#Read CSV file
horses <- read_csv("C:/Users/damia/Desktop/Betting/DVGB06Betting/DVGB06/Races/Races.csv")
results<-merge(x=horses,y=races,by="rid",all.x=FALSE, all.y=FALSE)

#Cor_horses <- select(results, c('age', 'saddle', 'decimalPrice', 'isFav', 'position','positionL', 'dist', 'RPR', 'TR', 'OR', 'runners', 'weight', 'res_win', 'res_place','metric','class','fences','hurdles','winningTime','prize'))

#M = cor(Cor_horses, use="pairwise.complete.obs")
#corrplot(M, method = 'number', number.cex = 0.6)
#pairs(Cor_horses)

