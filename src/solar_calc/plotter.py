import matplotlib.pyplot as plt
from typing import Sequence, Optional

def plot_profile(
    profile: Sequence[float],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    tilt: Optional[float] = None,
    azimuth: Optional[float] = None,
    figsize: tuple = (10, 5)
) -> None:
    """
    Plot a 24-point daily average profile of solar production with a main title and subtitle.

    Args:
        profile: Sequence of 24 floats, average production per hour (0-23).
        title: Main title for the plot.
        subtitle: Subtitle displayed under the main title.
        figsize: Figure size (width, height) in inches.
    """
    # Create figure and axes
    fig, ax = plt.subplots(figsize=figsize)

    # Plot data
    hours = list(range(24))
    ax.plot(hours, profile)

    # X-axis ticks every hour
    ax.set_xticks(hours)
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Average Power (kW)")
    ax.grid(True)

    # Main title
    if title:
        fig.suptitle(title, fontsize=16, x=0.5, y=0.98, ha='center')
    # Subtitle as separate text for smaller font
    if subtitle:
        # y=0.94 positions it slightly below the main title
        fig.text(x=0.5, y=0.90, s=subtitle, fontsize=12, ha='center')
    # Optional system parameters
    info_parts = []
    if tilt is not None:
        info_parts.append(f"Tilt: {tilt}°")
    if azimuth is not None:
        info_parts.append(f"Azimuth: {azimuth}°")
    if info_parts:
        info_str = " | ".join(info_parts)
        fig.text(0.5, 0.85, info_str, fontsize=10, ha='center')

    # Adjust layout to make room for titles
    plt.tight_layout()
    # Move the subplot down to make space for the subtitle
    fig.subplots_adjust(top=0.83)

    # Display
    plt.show()