library(ggplot2)
library(tidyr)
library(dplyr)

df = read.csv("results/table.tsv", sep = "\t", header = TRUE)
df$tool = as.factor(df$tool)
df$dataset = as.factor(df$dataset)
df$mem_bytes = as.numeric(df$mem_bytes)
df$time_seconds = as.numeric(df$time_seconds)

p = ggplot(df) +
  geom_line(aes(x = n_genomes, y = mem_bytes, color = tool)) + 
  geom_point(aes(x = n_genomes, y = mem_bytes, color = tool)) + 
  facet_wrap(~dataset) +
  scale_x_log10() + 
  scale_y_log10() +
  theme_minimal()

print(p)

p = ggplot(df) +
  geom_line(aes(x = n_genomes, y = time_seconds, color = tool)) + 
  geom_point(aes(x = n_genomes, y = time_seconds, color = tool)) + 
  facet_wrap(~dataset) +
  scale_x_log10() + 
  scale_y_log10() +
  theme_minimal()

print(p)