rm(list = ls())
library(FactoMineR)
library(factoextra)
library(ggplot2)
library(ggdendro)
library(RColorBrewer)

#Initialisation 
data <- readRDS("data/datafinalMoinsCat.Rds")
summary(data)

res.mca <- MCA(data, graph = FALSE, ncp = 25 )

fviz_mca_biplot(res.mca)

res.mca = MCA(data, graph = FALSE, ncp = 25,  quali.sup = c(3))

fviz_mca_biplot(res.mca)


png("contribution_valeurs_propres.png",  height=500, width=1200)
barplot(res.mca$eig[,3])
dev.off()


res.mca$ind$contrib[,c(1,2)][order(res.mca$ind$contrib[,c(1,2)], decreasing = TRUE)][c(1:10)]
indsup = c(order(apply(res.mca$ind$contrib, 1,FUN = sum), decreasing = TRUE)[c(1:100)])


nrow(data)
res.mca <- MCA(data, graph = FALSE, ncp = 25,quali.sup = c(4,3) )
res.mca$eig[,3]
barplot(res.mca$eig[,3])

indsup = c(order(apply(res.mca$ind$contrib, 1,FUN = sum), decreasing = TRUE)[1:20])
barplot(apply(res.mca$ind$contrib[, c(1:4)], 1,FUN = sum))
indsup

res.mca <- MCA(data, graph = FALSE, ncp = 25,quali.sup = c(3, 4, 5), ind.sup = indsup )
res.mca$eig[,2]


percentage = function(x) {
  return(x/sum(x))
}

cumulation = function(x) {
  n = length(x)
  aux = 0
  l = c()
  for (i in 1:n){
    l = append(l,x[i] + aux)
    aux = x[i] + aux
  }
  return(l)
}

val = apply(t(res.mca$var$contrib[c(23:25),]),1, FUN=sum)
valc = apply(t(res.mca$var$cos2[c(23:25),]),1, FUN=sum)
val2 = percentage(val)
valc2 = percentage(valc)
ordrec = order(as.vector(valc2), decreasing = TRUE)
ordre = order(as.vector(val2), decreasing = TRUE)
val2[ordre]

png("contribution_variables_alcool_cumulée.png", height=500, width=1200)
barplot(cumulation(val2[ordre]))

dev.off()
barplot(cumulation(valc2[ordrec]))


png("modalités_dim1_2.png",width = 1600, height = 1000)
fviz_mca_var(res.mca, axes=c(1,2),choice = c("mca.cor") ,labelsize = 8) +  theme_grey() + theme(axis.title = element_text(size = 25),  # Adjust axis title size
               axis.text = element_text(size = 20),  
               plot.title = element_text(size = 30), 
               legend.title = element_text(size = 25),
               legend.text = element_text(size = 20)
          
            ) + ggtitle("") + xlab(paste("Dimension ", as.character(2), sep = "")) + ylab(paste("Dimension ",  as.character(6), sep = ""))
dev.off()


png("modalités_dim3_4.png",width = 1600, height = 1000)
fviz_mca_var(res.mca, axes=c(3,4),choice = c("mca.cor") ,labelsize = 8) +  theme_grey() + theme(axis.title = element_text(size = 25),  # Adjust axis title size
               axis.text = element_text(size = 20),  
               plot.title = element_text(size = 30),  
               legend.title = element_text(size = 25), 
               legend.text = element_text(size = 20)
          
            ) + ggtitle("") + xlab(paste("Dimension ", as.character(13), sep = "")) + ylab(paste("Dimension ",  as.character(17), sep = ""))
dev.off()


affichage = function(mca ,d1, d2) {
  # parametre affichage plot
  color_palette_habillage = c("palegreen", "lemonchiffon", "#FF6A6A") # couleurs legende
  p <- fviz_mca_biplot(
  mca,
  axes = c(d1, d2), #axes choisies
  label = "var",
  select.var = list(contrib = 15 ), # 15 premiers qui contribuent le plus a la construction axe
  habillage = c(7), # coloriage
  col.ind = color_palette_habillage,
  col.var = "black",
  palette = color_palette_habillage,
  pointsize = 6,
  labelsize = 9,
  repel = TRUE
)

# parametres plots
  p <- p + theme_grey() + theme(axis.title = element_text(size = 25),  
               axis.text = element_text(size = 20),   
               plot.title = element_text(size = 30), 
               legend.title = element_text(size = 25), 
               legend.text = element_text(size = 20)   
            ) + ggtitle("") + xlab(paste("Dimension ", as.character(d1), sep = "")) + ylab(paste("Dimension ",  as.character(d2), sep = ""))

# renvoie le plot
return (p)
}


png("acm_2-6.png", width = 1500, height = 1000)
p = affichage(res.mca, 1, 2)

summary(data)
print(p)
dev.off()


png("acm_13-17.png", width=1500, height= 1000)
p = affichage(res.mca, 3, 4)
print(p)
dev.off()
