library(ggplot2)
library(tidyr)
library(dplyr)

df = read.csv("results/table.tsv", sep = "\t", header = TRUE)
df$tool = as.factor(df$tool)
df$dataset = factor(df$dataset, levels = c("salmonella", "random"), labels = c("Salmonella", "Random"))
df$mem_bytes = as.numeric(df$mem_bytes)
df$time_seconds = as.numeric(df$time_seconds)
df$time_minutes = df$time_seconds / 60

shared_theme =   theme(
  panel.grid.major = element_line(color = "grey70", linewidth = 0.2),
  panel.grid.minor = element_line(color = "grey90", linewidth = 0.2),
  axis.text.x = element_text(angle = 45, hjust = 1),
)
shared_legend = scale_color_manual(
  values = c("bifrost" = "#ffbe0b", "ggcat" = "#fb5607", "metagraph_1gb_anno" = "#ff006e", "themisto" = "#8338ec", "themisto_to_disk" = "#3a86ff"),
  labels = c("bifrost" = "Bifrost",
             "ggcat" = "GGCAT 2",
             "metagraph_1g_anno" = "Metagraph (row-major)",
             "themisto" = "Our algorithm",
             "themisto_to_disk" = "Our algorithm to disk"),
  name = "Method"
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
  labs(
    x = "# Genomes",
    y = "Memory (bytes)",
    color = "Method",
  ) +
  shared_legend + 
  theme_minimal() + shared_theme

print(p)
ggsave("plots/mem.pdf")

p = ggplot(df) +
  geom_line(aes(x = n_genomes, y = time_minutes, color = tool)) + 
  geom_point(aes(x = n_genomes, y = time_minutes, color = tool)) + 
  facet_wrap(~dataset) +
  scale_x_log10(
    breaks = 10^(-1:5),
    minor_breaks = rep(1:9, times = 5) * 10^rep(-1:5, each = 9)
  ) +
  scale_y_log10(
    breaks = 10^(0:6),
    minor_breaks = rep(1:9, times = 3) * 10^rep(0:6, each = 9)
  ) +
  labs(
    x = "# Genomes",
    y = "Time (minutes)",
    color = "Method",
  ) +
  shared_legend + 
  theme_minimal() + shared_theme

print(p)
ggsave("plots/time.pdf")