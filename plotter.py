"""This whole module is TODO
functions for plotting the leaderboard and skill distributions must we written properly, those below are just ai drafts"""

def plot_skill_distributions(leaderboard_file: str) -> None:
    """Plot the leaderboard using matplotlib.
    """
    # Load and sort so x-axis matches the CSV dump ordering logic
    df = pd.read_csv(leaderboard_file)
    df = df.sort_values(["true_skill", "name"], ascending=[False, True]).reset_index(drop=True)
    # only take top 10
    df = df.head(10)

    names = df["name"].tolist()
    mus = df["mu"].astype(float).to_numpy()
    sigmas = df["sigma"].astype(float).to_numpy()
    x_positions = np.arange(len(df))

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(max(10, len(df) * 0.45), 8))

    # Draw a slim "violin" (normal pdf) around each x position, centered at mu
    width_scale = 0.35  # half-width of the violin (controls visual thickness)

    for i, (mu, sigma) in enumerate(zip(mus, sigmas)):
        sigma = max(float(sigma), 1e-9)  # avoid div-by-zero

        # y-range around mu for the curve (±4σ captures ~99.99%)
        y = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 201)
        # Normal PDF along y (centered at mu with std sigma)
        pdf = np.exp(-0.5 * ((y - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

        # Normalize to a max width and build left/right x bounds
        pdf_scaled = (pdf / pdf.max()) * width_scale
        x_left = x_positions[i] - pdf_scaled
        x_right = x_positions[i] + pdf_scaled

        # Fill the violin
        ax.fill_betweenx(y, x_left, x_right, alpha=0.30, linewidth=0)

        # A faint vertical guide spanning ±3σ (optional but helpful)
        ax.vlines(x_positions[i], mu - 3 * sigma, mu + 3 * sigma, color="k", alpha=0.25, linewidth=1)

        # Point at mu
        sns.scatterplot(x=[x_positions[i]], y=[mu], ax=ax, s=60, edgecolor="white", zorder=3)

    # Axis labels & ticks
    ax.set_xticks(x_positions)
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_xlabel("Player (sorted by TrueSkill=μ-3σ)")
    ax.set_ylabel("Mean skill estimate (μ)")
    ax.set_title("Leaderboard — μ with standard deviation (σ)")

    # Ensure the plot "extends upwards" with padding even if all μ are negative
    y_min = float(np.min(mus - 4 * sigmas))
    y_max = float(np.max(mus + 4 * sigmas))
    span = y_max - y_min if y_max > y_min else 1.0
    pad = 0.05 * span
    ax.set_ylim(y_min - pad, y_max + pad)

    ax.margins(x=0.02)
    plt.tight_layout()
    plt.show()


def plot_skill_distributions_2(leaderboard_file: str) -> None:
    """
    Plot overlapping Gaussian bell curves (one per player) with direct labels:
    - X-axis: rating (μ), Y-axis: probability density.
    - Each player's curve: PDF of N(μ, σ^2), semi-transparent line.
    - Player names are placed above each curve's peak (at x=μ), with simple
      collision avoidance (staggered vertical levels when μ's are close).
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from math import sqrt, pi
    from matplotlib import patheffects

    # Load and sort for consistent ordering (same as CSV dump: true_skill desc, name asc)
    df = pd.read_csv(leaderboard_file)
    df = df.sort_values(["true_skill", "name"], ascending=[False, True]).reset_index(drop=True)
    # take top 10
    df = df.head(10)

    names  = df["name"].tolist()
    mus    = df["mu"].astype(float).to_numpy()
    sigmas = df["sigma"].astype(float).to_numpy()

    # Build a common x-domain covering all curves (±4σ around each μ)
    x_min = float(np.min(mus - 4 * sigmas))
    x_max = float(np.max(mus + 4 * sigmas))
    if not np.isfinite(x_min) or not np.isfinite(x_max) or x_min == x_max:
        x_min, x_max = -1.0, 1.0
    x = np.linspace(x_min, x_max, 1200)
    span = x_max - x_min

    # Plot style
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 7))

    # Distinct colors; will cycle if many players
    palette = sns.color_palette("husl", n_colors=len(df))

    # Precompute peak densities for labeling (peak of normal pdf is at x=μ)
    # pdf_peak = 1 / (σ * sqrt(2π))
    pdf_peaks = 1.0 / (np.maximum(sigmas, 1e-12) * sqrt(2.0 * pi))

    # Plot curves
    for idx, (name, mu, sigma, peak) in enumerate(zip(names, mus, sigmas, pdf_peaks)):
        sigma = max(float(sigma), 1e-12)
        pdf = (1.0 / (sigma * sqrt(2.0 * pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

        sns.lineplot(
            x=x,
            y=pdf,
            ax=ax,
            linewidth=2,
            alpha=0.75,
            color=palette[idx],
        )

        # A subtle marker at the peak
        ax.plot([mu], [peak], marker="o", markersize=4, color=palette[idx], alpha=0.9)

    # --- Direct labels above the peaks with simple collision avoidance ---
    # Sort players by μ so we can stagger labels when μ's are close.
    order_by_mu = np.argsort(mus)
    # If two μ's are closer than this threshold, we bump the label up a level.
    dx_threshold = max(0.03 * span, 1e-6)  # ~3% of the domain

    current_level = 0
    last_mu = None

    # Path effects for readable text (white halo)
    halo = [patheffects.withStroke(linewidth=3, foreground="white")]

    for rank, idx in enumerate(order_by_mu):
        mu = float(mus[idx])
        peak = float(pdf_peaks[idx])
        name = names[idx]
        color = palette[idx]

        if last_mu is not None and abs(mu - last_mu) < dx_threshold:
            current_level += 1
        else:
            current_level = 0
        last_mu = mu

        # Vertical offset factor: base 10% above peak + 20% per stacked level
        y_offset = peak * (0.10 + 0.20 * current_level)
        label_y = peak + y_offset

        ax.text(
            mu,
            label_y,
            name,
            ha="center",
            va="bottom",
            fontsize=9,
            color=color,
            weight="bold",
            path_effects=halo,
            zorder=5,
        )

        # Optional: a faint guide line from peak to label
        ax.plot([mu, mu], [peak, label_y * 0.98], linestyle=":", linewidth=1, color=color, alpha=0.6)

    # Axes & title
    ax.set_xlabel("Mean rating estimate (μ)")
    ax.set_ylabel("Probability density")
    ax.set_title("Player Skill Distributions, sorted by TrueSkill (μ - 3σ)")

    # Ensure plot extends upward (density ≥ 0) with headroom for labels
    _, ymax = ax.get_ylim()
    # Estimate a safe top based on the tallest label
    tallest_label = float(np.max(pdf_peaks * (1.0 + 0.10 + 0.20 * 3))) if len(df) else 1.0
    ax.set_ylim(0.0, max(ymax, tallest_label) * 1.15)

    # Slight x-margins so edge labels aren't clipped
    ax.margins(x=0.02)

    # Remove legend (labels on curves replace it). Re-enable if you prefer.
    ax.legend_.remove() if ax.legend_ else None

    plt.tight_layout()
    plt.show()



def plot_conservative_leaderboard(leaderboard_file: str) -> None:
    """Plot the conservative leaderboard using matplotlib.
    """
    # TODO