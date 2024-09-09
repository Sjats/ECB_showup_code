rm(list = ls())
data <- readRDS("dataSocial.Rds")
summary(data)

# Fonction des barplots en prop
plot_bar <- function(tab, file_name, plot_names, palette_size) {
  tab <- prop.table(table(tab))
  tab <- tab[order(tab, decreasing = TRUE)]
  png(file_name, height = 800, width = 1500)
  barplot(tab, 
          col = RColorBrewer::brewer.pal(palette_size, "Set3"),
          names.arg = plot_names,
          cex.axis = 2.5, 
          cex.names = 3.2)
  dev.off()
}


plot_bar(data$Sit2, "graphsSocio/Rep variable Situation revenu.png", 
         c("Lycée", "App.", "Rech. E.", "S. Act.", "Sup.", "Travail", "Inser."), 7)

plot_bar(data$SitPere, "graphsSocio/Rep variable Situation Pere revenu.png", 
         c("Trav.", "Chô", "S. Act", "Inv.", "Ret.", "Sait Pas", "Non Conc"), 9)

plot_bar(data$SitMere, "graphsSocio/Rep variable Situation Mere revenu.png", 
         c("Trav.", "Chô", "S. Act", "Inv.", "Ret.", "Sait Pas", "Non Conc"), 9)

plot_bar(data$PCSPere, "graphsSocio/Rep variable PCS Pere revenu.png", 
         c("Ouv.", "Cadre", "Emp.", "Arti.", "Inter.", "Chef", "Non C.", "S. Pro.", "Agri"), 9)

plot_bar(data$PCSMere, "graphsSocio/Rep variable PCS Mere revenu.png", 
         c("Ouv.", "Cadre", "Emp.", "Arti.", "Inter.", "Chef", "Non C.", "S. Pro.", "Agri"), 9)

# fonc cartes de chaleur
plot_contingency <- function(tab, file_name, row_labels, col_labels) {
  png(file_name, height = 800, width = 1200)
  par(omi = c(1, 1, 1, 1) + 0.1, mar = c(6, 5, 4.5, 6.5))
  image(tab, axes = FALSE)
  
  taille <- 2.65
  # Ajout lables
  for (i in seq_along(col_labels)) {
    mtext(col_labels[i], side = 3, adj = 0.08 + 0.12 * (i - 1), outer = TRUE, cex = taille)
  }
  for (i in seq_along(row_labels)) {
    mtext(row_labels[i], side = 2, adj = 0.12 + 0.38 * (i - 1), outer = TRUE, cex = 3.5)
  }
  
  par(xpd = TRUE) 
  legend("right",
         legend = c(1, .9, .8, .7, .6, .5, .4, .3, .2, .1, 0),
         fill = hcl.colors(12, "YlOrRd", rev = FALSE),
         bty = "n", y.intersp = 0.75, inset = c(-0.12, 0),
         cex = 2, text.font = 2, xjust = 0, yjust = 0.5)
  par(xpd = FALSE)
  dev.off()
}

# Plot tableaux contingence
tab1 <- prop.table(table(data$Sit2, data$Alcool), 1)
plot_contingency(tab1, "graphsSocio/Tableau contingence PCS_Alcool.png",
                 c("Faible", "Modérée", "Élevée"),
                 c("Lycée", "Apprenti.", "Sup.", "Sans Act.", "Rech.", "Insertion", "Travail"))

tab2 <- prop.table(table(data$PCSPere, data$Alcool), 1)
plot_contingency(tab2, "graphsSocio/Tableau contingence PCS.png",
                 c("Faible", "Modérée", "Élevée"),
                 c("Agri.", "Arti.", "Chef.", "Cadre", "Inte.", "Empl.", "Ouv.", "Sans.", "Non Con."))

