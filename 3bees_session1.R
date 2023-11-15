#Tutorial taken from https://r4ds.hadley.nz/data-visualize

#install packages
install.packages("tidyverse")
install.packages("palmerpenguins")

#load libraries
library(tidyverse)
library(palmerpenguins)

#see what penguins is
penguins
summary(penguins)

#writing penguins to a tibble called pen and the summary to a table
pen <- penguins
pen_summary <- summary(pen)

#Plotting
#Initialising
ggplot(data = penguins)

#Defining x and y axes
ggplot(
  data = penguins,
  mapping = aes(x = flipper_length_mm, y = body_mass_g)
)

#Adding dots
ggplot(
  data = penguins,
  mapping = aes(x = flipper_length_mm, y = body_mass_g)
) +
  geom_point()

#colouring by species
ggplot(
  data = penguins,
  mapping = aes(x = flipper_length_mm, y = body_mass_g, color = species)
) +
  geom_point()

#Adding a line of best fit per species
ggplot(
  data = penguins,
  mapping = aes(x = flipper_length_mm, y = body_mass_g, color = species)
) +
  geom_point() +
  geom_smooth(method = "lm")

#Adding a line of best fit globally
ggplot(
  data = penguins,
  mapping = aes(x = flipper_length_mm, y = body_mass_g)
) +
  geom_point(mapping = aes(color = species)) +
  geom_smooth(method = "lm")

#Changing shape based on species
ggplot(
  data = penguins,
  mapping = aes(x = flipper_length_mm, y = body_mass_g)
) +
  geom_point(mapping = aes(color = species, shape = species)) +
  geom_smooth(method = "lm")
