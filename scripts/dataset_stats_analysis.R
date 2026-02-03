library(ggplot2)

df = read.csv("results/dataset_stats.csv")
df$n_genomes = as.integer(gsub("\\D+", "", df$dataset))
df$dataset_type = letter <- sub("-.*", "", df$dataset)

lower_bounds = 1 / (df$mean_unitig_len - 31 + 1)

print(lower_bounds)
print(df$key_kmer_frac / lower_bounds)

new_df = data.frame(
  "lower_bound" = lower_bounds, 
  "observed" = df$key_kmer_frac,
  "n_genomes" = df$n_genomes,
  "dataset_type" = df$dataset_type
)
to_plot = pivot_longer(new_df, cols = c("lower_bound", "observed"))

p = ggplot(to_plot) + 
  geom_line(aes(x = n_genomes, y = value, color = name)) + 
  facet_wrap(
    ~dataset_type,
    labeller = labeller(
      dataset_type = c(
        S = "Salmonella",
        R = "Random"
      )
    )    
  ) +
  scale_x_log10(
    minor_breaks = rep(1:9, times = 5) * 10^rep(-1:5, each = 9)
  ) +
  labs(
    x = "Number of genomes",
    y = "Fraction of key k-mers",
    color = "Fraction",
    title = "Fraction of key k-mers"
  ) +
  scale_color_manual(
    values = c("lower_bound" = "#3a86ff", "observed" = "#ff006e"),
    labels = c("lower_bound" = "Unitig-ending k-mers",
               "observed" = "Key k-mers"),
    name = "Fraction"
  ) +
  theme_minimal() + 
  theme(
    panel.grid.major = element_line(color = "grey70", linewidth = 0.2),
    panel.grid.minor = element_line(color = "grey90", linewidth = 0.2),
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.title = element_text(hjust = 0.5)
  )

print(p)
ggsave("plots/key_kmers.pdf", width = 7, height = 4)