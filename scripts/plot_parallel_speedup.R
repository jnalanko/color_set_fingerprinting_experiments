library(ggplot2)
library(tidyr)
library(dplyr)

df = read.csv("results/parallel_speedup.tsv", sep = "\t", header = TRUE)
df$dataset = as.factor(df$dataset)
df$n_threads = as.numeric(df$n_threads)
df$mem_bytes = as.numeric(df$mem_bytes)
df$time_seconds = as.numeric(df$time_seconds)

df = df %>%
  group_by(dataset) %>%
  mutate(t1 = time_seconds[n_threads == 1][1]) %>%
  ungroup() %>%
  mutate(speedup = t1 / time_seconds)

shared_theme =   theme(
  panel.grid.major = element_line(color = "grey70", linewidth = 0.2),
  panel.grid.minor = element_line(color = "grey90", linewidth = 0.2),
)

p = ggplot(df) +
  geom_line(aes(x = n_threads, y = speedup, color = dataset)) + 
  geom_point(aes(x = n_threads, y = speedup, color = dataset)) + 
  geom_line(
    aes(x = n_threads, y = n_threads),
    linetype = "dotted",
    color = "black"
  ) +
  theme_minimal() + shared_theme

print(p)
ggsave("plots/speedup.pdf", p)