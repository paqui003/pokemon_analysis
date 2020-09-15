library(ggplot2)
library(ggforce)
library(dplyr)

data <- read.csv("../csv/pokemon.csv")

data <- data[c(12, 19, 20)]

data <- data[!(data$Growthr=="â???""),]


data <- data %>% group_by(Label, Growthr, Type1) %>% tally()

data <- gather_set_data(data, 1:3)


cbp1 <- c("#999999", "#D55E00", "#CC79A7", "#56B4E9", "#009E73",
          "#F0E442", "#0072B2", "#E69F00")



plot <- ggplot(data, aes(x, id = id, split = y, value = n)) +
  geom_parallel_sets(aes(fill = Label), alpha = 0.5, axis.width = 0.2) +
  geom_parallel_sets_axes(axis.width = 0.2, fill = "grey") +
  geom_parallel_sets_labels(colour = 'black', angle = 360, size = 4) +
  theme_bw()

plot + scale_fill_manual(values = cbp1) + 
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        #axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        axis.title.x = element_blank(),
        panel.border = element_blank(),
        axis.text.x = element_text(face="bold", 
                                   size=14)
        )


