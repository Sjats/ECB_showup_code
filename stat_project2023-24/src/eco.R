rm(list = ls())
data <- readRDS("dataEco.Rds")

# Fonction pour créer des matrices de proportion
create_prop_matrix <- function(variables, labels) {
  q <- data.frame(prop.table(table(variables[[1]])),
                  prop.table(table(variables[[2]])),
                  prop.table(table(variables[[3]])),
                  prop.table(table(variables[[4]])))
  q <- q[, c(2, 4, 6, 8)]
  
  png("Rep_var_revenu.png", height = 1100, width = 1600)
  barplot(as.matrix(q),
          ylim = c(0, 1),
          main = "Répartition des Variables Revenu",
          xlim = c(0, 7.2),
          cex.main = 3.5,
          cex.names = 2.5,
          width = 1.4,
          names.arg = labels,
          las = 1,
          col = c("tomato", "cadetblue"))
  legend("right", legend = c("Non", "Oui"), fill = c("tomato", "cadetblue"), box.col = 0, box.lwd = 0, cex = 2.45)
  dev.off()
}

# Variables pour la matrice
variables <- list(data$ArgentdePoche, data$RemunerationSalariale, data$ArgentOccasionnel, data$SalaireJob)
labels <- c("Argent de Poche", "Rémunération jobs", "Occasion particulière", "Salaire Stage")

# Appel à la fonction
create_prop_matrix(variables, labels)

# Transformation des données quantitatives
create_data_frame <- function(df) {
  l <- list()
  for (i in 1:nrow(df)) {
    l[[i]] <- as.numeric(df[i,])
  }
  as.data.frame(do.call(rbind, l))
}

# Création et affichage de la matrice de réponses
my_data_frame <- create_data_frame(na.omit(data.frame(data$ArgentdePoche, data$RemunerationSalariale, data$ArgentOccasionnel, data$SalaireJob)))

png("Reponse_aux_Questions_concernant_le_Revenu.png", height = 1100, width = 1600)
image(as.matrix(my_data_frame), 
      col = c("tomato", "cadetblue"),
      cex.main = 3.5,
      xlim = c(0, 1.105),
      axes = FALSE,
      main = "Réponse aux Questions concernant le Revenu")
axis(2, at = c(0, 0.35, 0.69, 1), 
     labels = labels, 
     cex.axis = 2)
legend("right", legend = c("Non", "Oui"), fill = c("tomato", "cadetblue"), box.col = 0, box.lwd = 0, cex = 2.45)
dev.off()

# Matrice V de Cramer
create_cramer_matrix <- function(df) {
  mat <- DescTools::PairApply(df, DescTools::CramerV)
  rownames(mat) <- labels
  colnames(mat) <- labels
  return(mat)
}

mat <- create_cramer_matrix(na.omit(data.frame(data$ArgentdePoche, data$RemunerationSalariale, data$ArgentOccasionnel, data$SalaireJob)))

# Visualisation de la matrice V de Cramer
png("matrice_Covariance_Revenu_V_cramers.png", height = 1100, width = 950)
corrplot::corrplot(mat, method = "color", addrect = 3, order = "hclust", tl.cex = 1.5, tl.col = "black")
title("Matrice des V de Cramer des Différents Types de Revenu", cex.main = 2.3)
dev.off()

# Calcul du revenu et graphiques de distribution
data <- transform(data, RevenuW = RemunerationSalarialeQ + SalaireJobQ, RevenuD = ArgentdePocheQ + ArgentOccasionnelQ)

create_vioplot <- function(revenu_var, alcool_var, plot_name) {
  png(plot_name, height = 1100, width = 1600)
  vioplot(revenu_var ~ alcool_var, outline = FALSE)
  dev.off()
}

create_vioplot(data$RevenuW, data$Alcool, "vioplot_RevenuW_Alcool.png")
create_vioplot(data$RevenuD, data$Alcool, "vioplot_RevenuD_Alcool.png")

# Matrice de covariance et heatmap
plot_covariance <- function(data, labels, file_name, main_title) {
  mat <- cor(as.matrix(na.omit(data)))
  png(file_name, height = 1100, width = 950)
  corrplot::corrplot(mat, method = "color", addrect = 3, order = "hclust", tl.cex = 1.5, tl.col = "black")
  title(main_title, cex.main = 2.3)
  dev.off()
}

# Appel à la fonction de covariance
plot_covariance(data[, c("ArgentdePocheQ", "RemunerationSalarialeQ", "ArgentOccasionnelQ", "SalaireJobQ")], labels, "matrice_Covariance_Revenu.png", "Matrice de Covariance des Différents Types de Revenu")

# Réinitialiser les objets R
rm(list = ls())
