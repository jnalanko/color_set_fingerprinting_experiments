library(ggplot2)
library(tidyr)
library(dplyr)

df = read.csv("results/table.tsv", sep = "\t", header = TRUE)
df$tool = as.factor(df$tool)
df$dataset = as.factor(df$dataset)
df$mem_bytes = as.numeric(df$mem_bytes)
df$time_seconds = as.numeric(df$time_seconds)

shared_theme =   theme(
  panel.grid.major = element_line(color = "grey70", linewidth = 0.2),
  panel.grid.minor = element_line(color = "grey90", linewidth = 0.2),
)

p = ggplot(df) +
  geom_line(aes(x = n_genomes, y = mem_bytes, color = tool)) + 
  geom_point(aes(x = n_genomes, y = mem_bytes, color = tool)) + 
  facet_wrap(~dataset) +
  scale_x_log10(
    breaks = 10^(-1:5),
    minor_breaks = rep(1:9, times = 5) * 10^rep(-1:5, each = 9)
  ) +
  scale_y_log10(
    breaks = 10^(5:12),
    minor_breaks = rep(1:9, times = 3) * 10^rep(5:12, each = 9)
  ) +
  theme_minimal() + shared_theme

print(p)
ggsave("plots/mem.pdf")

p = ggplot(df) +
  geom_line(aes(x = n_genomes, y = time_seconds, color = tool)) + 
  geom_point(aes(x = n_genomes, y = time_seconds, color = tool)) + 
  facet_wrap(~dataset) +
  scale_x_log10(
    breaks = 10^(-1:5),
    minor_breaks = rep(1:9, times = 5) * 10^rep(-1:5, each = 9)
  ) +
  scale_y_log10(
    breaks = 10^(0:6),
    minor_breaks = rep(1:9, times = 3) * 10^rep(0:6, each = 9)
  ) +
  theme_minimal() + shared_theme

print(p)
ggsave("plots/time.pdf")