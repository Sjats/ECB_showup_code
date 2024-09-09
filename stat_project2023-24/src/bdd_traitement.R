rm(list = ls())
library(dplyr)
# Not visible, but there was a first treatment which code I can't find where we select the variables of the database and rename them 
# Cf. pdf to find them 

dataSocial <- readRDS("dataSocial.Rds")
dataEco <- readRDS("dataEco.Rds")
summary(dataSocial)

dataEco$ArgentdePocheQ <- ifelse(dataEco$ArgentdePoche == "Non", 0, dataEco$ArgentdePocheQ)
dataEco$RemunerationSalarialeQ <- ifelse(dataEco$RemunerationSalariale == "Non", 0, dataEco$RemunerationSalarialeQ)
dataEco$ArgentOccasionnelQ <- ifelse(dataEco$ArgentOccasionnel == "Non", 0, dataEco$ArgentOccasionnelQ)
dataEco$SalaireJobQ <- ifelse(dataEco$SalaireJob == "Non", 0, dataEco$SalaireJobQ)

dataQ <- data.frame(dataEco$ArgentdePocheQ, dataEco$RemunerationSalarialeQ, dataEco$ArgentOccasionnelQ, dataEco$SalaireJobQ)
summary(dataQ)

max_rev <- apply(dataQ, 1, FUN = max )

summary(max_rev)
length(max_rev)

principaleSR <- ifelse(max_rev == 0, 1, NA)
principaleSR <- ifelse(max_rev == dataEco$ArgentdePocheQ & 0 < dataEco$ArgentdePocheQ  , 2, principaleSR)
principaleSR <- ifelse(max_rev == dataEco$RemunerationSalarialeQ & 0 < dataEco$RemunerationSalarialeQ, 3, principaleSR)
principaleSR <- ifelse(max_rev == dataEco$ArgentOccasionnelQ & 0 < dataEco$ArgentOccasionnelQ, 4, principaleSR)
principaleSR <- ifelse(max_rev == dataEco$SalaireJobQ & 0 < dataEco$SalaireJobQ, 5, principaleSR)

etiquettes = c("Sans Revenu", "Argent de Poche", "Remunération Stage", "Argent Occasionnel", "Salaire Travail")

principaleSR <-   factor(x = principaleSR, levels = 1:5, labels = etiquettes)
barplot(table(principaleSR))


# Partie Santé
library(readr)
data_escapad <- read_delim("data_escapad.csv",
delim = ";", escape_double = FALSE, trim_ws = TRUE)

IMC <- data_escapad$Q13B / (data_escapad$Q13A / 100)^2
pensee <- data.frame(data_escapad$Q16B)
etat_sante <- data.frame(data_escapad$Q12)
summary(pensee)
rm(data_escapad)

donnees_IMC <- data.frame(IMC = IMC, Categorie_IMC = categories_IMC)
categories_IMC <- cut(IMC, breaks = c(0, 18.5, 24.9, Inf), labels = c("Maigreur", "Poids normal", "Surpoids"))
donnees_IMC <- data.frame(IMC = IMC, Categorie_IMC = categories_IMC)
donnees_IMC <- ifelse(donnees_IMC=="Poids normla", "Pids normal", "Problème de poids")
summary(donnees_IMC)

etat_sante <- ifelse(etat_sante == 1 | etat_sante == 2, 1, 2)
eti4 <- c("Pas Satifaisant", "Satisfaisant")
etat_sante <- factor(etat_sante, levels = 1:2, labels = eti4)



pensee <- ifelse(pensee == 1 , 1, 2)
eti3 <- c("Non", "Oui")
summary(pensee)
pensee_suicidaires <- factor(pensee, levels = 1:2, labels = eti3)


bdd <- data.frame(principaleSR, dataSocial$Sit2, dataSocial$PCSPere, donnees_IMC$Categorie_IMC, pensee_suicidaires, 
                        etat_sante, dataSocial$Alcool)

colnames(bdd) <- c("Revenu", "Situation", "PCS Père", "IMC", "Pensées Suicidaires",
                        "État de Santé", "Alcool")
summary(bdd)


data <- readRDS("datafinal2.Rds")

summary(data)

# Regrupation PCS 

data$"PCS Père"  = ifelse(data$"PCS Père"  == 1 | data$"PCS Père"  == "Ouvrier", 1, data$"PCS Père" )
data$"PCS Père"  = ifelse(data$"PCS Père"  == 2 | data$"PCS Père"  == 5 | data$"PCS Père"  == 6, 2, data$"PCS Père" )
data$"PCS Père"  = ifelse(data$"PCS Père"  == 3 | data$"PCS Père"  == 4, 3, data$"PCS Père" )
data$"PCS Père"  = ifelse(data$"PCS Père"  == 8 | data$"PCS Père"  == 9, 4, data$"PCS Père" )

etiquettes = c("C. Ouvrière", "C. Moyenne", "C. Aisé", "C. Autre")
data$"PCS Père" <-   factor(x = data$"PCS Père", levels = 1:4, labels = etiquettes)

# Regrupation Situation


data$Situation  = ifelse(data$Situation  == 2 | data$Situation  == 3, 2, data$Situation )
data$Situation = ifelse(data$Situation  == 5 | data$Situation == 6 | data$Situation  == 7 | data$Situation  == 4, 3, data$Situation )

data$Situation  = ifelse(data$Situation  == 2 | data$Situation  == 3, 2, data$Situation )
etiquettes = c("Lycée", "Formation")
data$Situation<-   factor(x = data$Situation, levels = 1:2, labels = etiquettes)


# Regrupation Catègorie IMC


saveRDS(data, file="datafinalMoinsCat.Rds")
