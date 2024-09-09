rm(list = ls())

library(factoextra)
library(ggplot2)
library(ggdendro)
library(RColorBrewer)
library(cluster)

affichage = function(mca ,d1, d2, var) {
  color_palette_habillage = paletteer_d("ggsci::nrc_npg", 7)
  p <- fviz_mca_ind(
  mca,
  axes = c(d1, d2), 
  label = "var",
  #select.var = list(contrib = var), 
  habillage = c(8), 
  col.ind = color_palette_habillage,
  #col.var = "black",
  palette = color_palette_habillage,
  pointsize = 6,
  #labelsize = 9,
  repel = TRUE,
  geom.ind = c("point")
 
)
  p <- p + theme_grey() + theme(axis.title = element_text(size = 25),  
               axis.text = element_text(size = 20),   
               plot.title = element_text(size = 30), 
               legend.title = element_text(size = 25), 
               legend.text = element_text(size = 20)   
            ) + ggtitle("") 
return (p)}

tableau_contingence <- function(var1, var2, labx="", laby="") {

    tab= melt(prop.table(table(var1, var2),1)*100)
    colnames(tab)=c("var1", "var2", "prop")
    ggplot(tab, aes(var1, var2)) +
    geom_tile(aes(fill = prop)) +
    geom_text(aes(label = paste(as.character(round(prop)), "%")), size = 15) +
    scale_fill_gradient(low = "white", high = "#1b98e0") +
    theme(text = element_text(size = 40)) +
    labs(x = labx, y = laby) +
    theme(axis.text.x = element_text(size = 45, angle = 45, hjust = 1)) +
    theme(axis.text.y = element_text(size = 45, hjust = 1)) +
    theme(legend.position = "none")
}
#Initialisation 

rm(list = ls())
setwd("/Users/Sunifred/Documents/projet_stat_final")
data <- readRDS("data_final.Rds")
data=na.omit(data)

res.mca = MCA(data, graph = FALSE, ncp = 25, quali.sup = c(3))# 4 en plus

points = res.mca$ind$coord[,c(1,2)]

library(mclust)

mclust_data = Mclust(points, G=3) # Si on force pas a avoir 3 categories, il en crée entre 7 et 9
summary(mclust_data)
parameters <- mclust_data$parameters

# Get the cluster assignments
clusters <- mclust_data$classification

data$Clusters = clusters


res.mca2 = MCA(data, graph = FALSE, ncp = 25, quali.sup = c(3,8))
png("mclust/ind_par_3_classes_forccees.png", ,width = 1600, height = 1000)

affichage(res.mca2, 1, 2, 8)
dev.off()

png("mclust/ind_par_3_classes_classification.png", ,width = 1600, height = 1000)
plot(mclust_data, what = "classification")
dev.off()
#Méthode Manuelle (Aprés observation Graphique)

data$Clusters = ifelse(res.mca$ind$coord[,1] < 0.5, 1,
                        ifelse(res.mca$ind$coord[,1] < 1.5, 2,3))

res.mca3 = MCA(data, graph = FALSE, ncp = 25, quali.sup = c(3,8))# 4 en plus

affichage(res.mca3, 1, 2, 8) # Graphiquement c'est bon

tableau_contingence(data$Clusters, data$Revenu)
# Cluster 3 tout le monde a un salaire, cluster 1 personne en a

tableau_contingence(data$Clusters, data$Situation)
# Classe 1  que des Lycéens, classe 3 que des gens en formation
# Classe 2, 68% formation, 32% lycee

tableau_contingence(data$Clusters, data$Alcool)
# Des ecarts entre les classes, mais semble pas être le facteur discriminant

tableau_contingence(data$Clusters, data$Secteur)
# Des ecarts entre les classes, mais semble pas être le facteur discriminant
tableau_contingence(data$Clusters, data$IMC)
# Pas d'ecart notable entre les classes
tableau_contingence(data$Clusters, data$EtatSante)
# Pas d'ecart notable entre les classes
tableau_contingence(data$Clusters, data$Suicide)
# Pas d'ecart notable entre les classes
