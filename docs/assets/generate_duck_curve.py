from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def generate_duck_curve():
    # 24-satni vremenski opseg (korak 6 minuta)
    hours = np.linspace(0, 24, 241)

    # Bazna potrosnja grada (MW) bez znacajnog udela solarne energije
    base_load = (
        22500
        - 3000 * np.exp(-((hours - 4.0) / 2.5) ** 2)
        + 2500 * np.exp(-((hours - 11.0) / 3.5) ** 2)
        + 6000 * np.exp(-((hours - 19.5) / 3.2) ** 2)
    )

    # Krive solarne proizvodnje za razlicite nivoe penetracije obnovljivih izvora
    solar_low = 2200 * np.exp(-((hours - 12.8) / 3.0) ** 2)
    solar_mid = 6800 * np.exp(-((hours - 12.8) / 3.0) ** 2)
    solar_high = 12200 * np.exp(-((hours - 12.8) / 3.0) ** 2)

    net_baseline = base_load - solar_low
    net_moderate = base_load - solar_mid
    net_high_solar = base_load - solar_high

    # Podesavanje stila za tehnicki whitepaper (300 DPI)
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 0.8

    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8FAFC")

    # Crtanje krivih
    ax.plot(hours, net_baseline, color="#64748B", linestyle="--", linewidth=2, label="Baseline Grid (Low Solar Penetration)")
    ax.plot(hours, net_moderate, color="#0284C7", linewidth=2.3, label="Transitional Grid (Moderate Solar)")
    ax.plot(hours, net_high_solar, color="#0F172A", linewidth=3, label="High-Renewable Grid (Target Scenario)")

    # Isticanje kriticne vecernje rampe (16:00 - 20:00)
    ramp_mask = (hours >= 16.0) & (hours <= 19.5)
    ax.plot(hours[ramp_mask], net_high_solar[ramp_mask], color="#E11D48", linewidth=3.8, label="Steep Evening Ramp (Fossil Peaker Risk)")

    # Osencena zona podnevnog viska energije
    midday_mask = (hours >= 10.5) & (hours <= 15.0)
    ax.fill_between(
        hours[midday_mask],
        net_high_solar[midday_mask],
        net_baseline[midday_mask],
        color="#10B981",
        alpha=0.14,
        label="Midday Solar Surplus (Battery Charging Window)",
    )

    # Anotacije na grafikonu
    ax.annotate(
        "Midday Over-Generation\n(Risk of Solar Curtailment)",
        xy=(12.8, 12250),
        xytext=(6.2, 11200),
        fontsize=9,
        fontweight="bold",
        color="#047857",
        arrowprops=dict(arrowstyle="->", color="#047857", lw=1.3),
    )

    ax.annotate(
        "Steep Evening Ramp-Up\n(+13,000 MW in ~3.5 hrs)",
        xy=(17.3, 24800),
        xytext=(12.6, 26800),
        fontsize=9,
        fontweight="bold",
        color="#BE123C",
        arrowprops=dict(arrowstyle="->", color="#BE123C", lw=1.3),
    )

    # Ose, mreza i naslovi
    ax.set_title('The "Duck Curve": Municipal Net Load vs. Renewable Penetration', fontsize=13, fontweight="bold", color="#0F172A", pad=14)
    ax.set_xlabel("Time of Day (Hours)", fontsize=10.5, fontweight="bold", color="#334155", labelpad=8)
    ax.set_ylabel("Net Municipal Load (MW)", fontsize=10.5, fontweight="bold", color="#334155", labelpad=8)

    ax.set_xlim(0, 24)
    ax.set_ylim(9000, 31000)
    ax.set_xticks(range(0, 25, 2))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 25, 2)], fontsize=9, color="#475569")
    ax.tick_params(axis="y", labelsize=9, colors="#475569")

    ax.grid(True, linestyle=":", color="#CBD5E1", alpha=0.9)
    ax.legend(loc="lower left", frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=8.8)

    plt.tight_layout()

    output_path = Path(__file__).resolve().parent / "duck_curve.png"
    plt.savefig(output_path, dpi=300)
    print(f"Grafikon uspesno sacuvan na: {output_path}")

if __name__ == "__main__":
    generate_duck_curve()