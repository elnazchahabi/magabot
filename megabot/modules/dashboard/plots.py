import matplotlib.pyplot as plt


def generate_stats_plot(stats: dict, output_file="stats.png"):
    labels = list(stats.keys())
    values = list(stats.values())

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values)
    plt.title("آمار سیستم")
    plt.xlabel("نوع")
    plt.ylabel("تعداد")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    return output_file