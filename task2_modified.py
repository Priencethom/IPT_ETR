import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================================================
# LOAD DATASET
# =========================================================
try:
    df = pd.read_csv("cleaned_teen_mental_dataset.csv")
    print("✅ Dataset loaded successfully!\n")
except FileNotFoundError:
    print("❌ Dataset file not found. Please make sure the CSV is in the same folder.")
    exit()

# Isaayos ang order ng social interaction level
if 'social_interaction_level' in df.columns:
    df['social_interaction_level'] = pd.Categorical(
        df['social_interaction_level'], 
        categories=['low', 'medium', 'high'], 
        ordered=True
    )

class MentalHealthVisualization:

    def __init__(self, df):
        self.df = df

    # 1. Scatter Plot: Social Media Hours vs Physical Activity
    def analyze_social_vs_physical(self):
        plt.figure(figsize=(8, 6))
        x = self.df["daily_social_media_hours"]
        y = self.df["physical_activity"]
        
        # LABEL & LEGEND: Nilagyan ng 'label' ang scatter at trendline
        plt.scatter(x, y, alpha=0.5, color="purple", label="Individual Teen")
        
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*x + b, color="orange", linewidth=2.5, label="Overall Trend")
        
        # Ipakita ang Legend
        plt.legend(title="Legend", loc="upper right", fontsize=10)
        
        plt.title("1. Social Media Hours vs Physical Activity")
        plt.xlabel("Daily Social Media (Hours)")
        plt.ylabel("Physical Activity (Hours)")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig("1_scatter_plot.png")
        plt.close()

    # 2. Pie Chart: Social Media Hours at Social Interactions
    def analyze_social_vs_interaction(self):
        # Nilakihan ng konti ang width para magkasya ang legend sa labas ng pie
        plt.figure(figsize=(9, 6)) 
        pie_data = self.df.groupby('social_interaction_level', observed=False)['daily_social_media_hours'].sum()
        
        labels = pie_data.index.str.title()
        colors = ['#ff9999','#66b3ff','#99ff99']
        
        wedges, texts, autotexts = plt.pie(
            pie_data, labels=labels, autopct='%1.1f%%', 
            startangle=140, colors=colors,
            textprops={'fontsize': 11, 'weight': 'bold'}
        )
        
        # LABEL & LEGEND: Inilagay sa gilid para hindi matakpan ang chart
        plt.legend(wedges, labels, title="Interaction Levels", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.title("2. Share of Social Media Hours per Social Interaction Level")
        plt.tight_layout()
        plt.savefig("2_pie_chart.png")
        plt.close()

    # 3. Line Graph: Stress Level at Age
    def analyze_stress_vs_age(self):
        plt.figure(figsize=(8, 6))
        line_data = self.df.groupby('age')['stress_level'].mean().reset_index()
        
        plt.plot(line_data['age'], line_data['stress_level'], marker='o', color='red', linewidth=2.5, label="Avg Stress Score")
        
        # LABELS: Eksaktong numero sa bawat tuldok
        for i, val in enumerate(line_data['stress_level']):
            plt.text(line_data['age'].iloc[i], val + 0.1, f'{val:.1f}', 
                     ha='center', fontsize=10, fontweight='bold', color='darkred')
        
        # LEGEND
        plt.legend(title="Data Metric", loc="upper left")
        
        plt.title("3. Average Stress Level per Age")
        plt.xlabel("Age (Years Old)")
        plt.ylabel("Average Stress Level (Scale 1-10)")
        plt.xticks(line_data['age'].unique())
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig("3_line_graph.png")
        plt.close()

    # 4. Histogram (2D): Sleep hours at Screentime before sleep (MADE EASIER TO UNDERSTAND)
    def analyze_sleep_vs_screentime(self):
        plt.figure(figsize=(8, 6))
        
        # IMPROVEMENT: Binawasan ang "bins" para maging malalaki ang boxes.
        # Idinagdag ang edgecolor para magmukhang malinis na grid/heatmap.
        h = plt.hist2d(self.df["screen_time_before_sleep"], self.df["sleep_hours"], 
                       bins=6, cmap="Blues", edgecolor='white', linewidth=0.5)
        
        # LEGEND (Colorbar): Ginawang mas malinaw ang label
        cbar = plt.colorbar(h[3])
        cbar.set_label('Total Number of Teens in this Range', fontweight='bold', fontsize=11)
        
        counts, xedges, yedges, image = h
        max_count = counts.max()
        
        # LABELS: Ilagay ang numero sa loob ng box, pero sa mga may laman lang
        for i in range(len(xedges)-1):
            for j in range(len(yedges)-1):
                if counts[i, j] > 0: 
                    x_center = (xedges[i] + xedges[i+1]) / 2
                    y_center = (yedges[j] + yedges[j+1]) / 2
                    # White text kung dark blue ang background, black kung light blue
                    text_color = "white" if counts[i, j] > (max_count / 2) else "black"
                    
                    # Para mas malinis, wag na i-print ang '1' o masyadong maliliit na bilang kung siksikan
                    plt.text(x_center, y_center, int(counts[i, j]), 
                             ha="center", va="center", color=text_color, fontsize=10, fontweight='bold')

        plt.title("4. Screen Time Before Sleep vs Sleep Hours (Density Grid)")
        plt.xlabel("Screen Time Before Sleep (Hours)")
        plt.ylabel("Hours of Sleep")
        plt.tight_layout()
        plt.savefig("4_histogram.png")
        plt.close()

    # 5. Bar Graph: Physical activity at Depression level
    def analyze_physical_vs_depression(self):
        plt.figure(figsize=(8, 6))
        bar_data = self.df.groupby('depression_label')['physical_activity'].mean().reset_index()
        bar_data['depression_label'] = bar_data['depression_label'].map({0: 'Normal', 1: 'Depressed'})
        
        colors = ['#66c2a5', '#fc8d62']
        bars = plt.bar(bar_data['depression_label'], bar_data['physical_activity'], color=colors)
        
        # LABELS: Numero sa tuktok ng bars
        plt.bar_label(bars, fmt='%.2f hrs', padding=3, fontsize=12, fontweight='bold')
        
        # LEGEND: Paggawa ng custom legend para sa colors ng bar
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#66c2a5', label='Normal (No Depression)'),
            Patch(facecolor='#fc8d62', label='Depressed Label')
        ]
        plt.legend(handles=legend_elements, title="Category Guide", loc="upper right")
        
        plt.title("5. Average Physical Activity by Depression Level")
        plt.xlabel("Clinical Assessment (Depression Level)")
        plt.ylabel("Average Physical Activity (Hours)")
        plt.ylim(0, bar_data['physical_activity'].max() * 1.3) # Extra space para sa legend at text
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig("5_bar_graph.png")
        plt.close()

    def generate_all_visualizations(self):
        self.analyze_social_vs_physical()
        self.analyze_social_vs_interaction()
        self.analyze_stress_vs_age()
        self.analyze_sleep_vs_screentime()
        self.analyze_physical_vs_depression()
        print("\n✅ All 5 visualizations successfully generated with clear legends and labels!")

# =========================================================
# EXECUTE THE CLASS
# =========================================================
if __name__ == "__main__":
    viz = MentalHealthVisualization(df)
    viz.generate_all_visualizations()