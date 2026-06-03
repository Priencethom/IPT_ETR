import matplotlib
matplotlib.use('Agg')  # Fix: non-interactive backend, must be before pyplot import

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
import os

SAVE_DIR = os.path.join("static", "Images")  # ✅ Correct path for Flask static files

class DataVisualization:

    def __init__(self, df):
        self.df = df
        os.makedirs(SAVE_DIR, exist_ok=True)  # ✅ Create folder if it doesn't exist
        
        # Isaayos ang order ng social interaction level kung mayroon sa dataset
        if 'social_interaction_level' in self.df.columns:
            self.df['social_interaction_level'] = pd.Categorical(
                self.df['social_interaction_level'], 
                categories=['low', 'medium', 'high'], 
                ordered=True
            )

    def _save(self, filename):
        """Helper: save to static/Images/ and close the figure."""
        path = os.path.join(SAVE_DIR, filename)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        return path

    # 1. SCATTER PLOT: Social Media Hours vs Physical Activity
    def scatter_plot(self):
        try:
            plt.figure(figsize=(8, 6))
            x = self.df["daily_social_media_hours"]
            y = self.df["physical_activity"]
            
            plt.scatter(x, y, alpha=0.5, color="purple", label="Individual Teen")
            
            m, b = np.polyfit(x, y, 1)
            plt.plot(x, m*x + b, color="orange", linewidth=2.5, label="Overall Trend")
            
            plt.legend(title="Legend", loc="upper right", fontsize=10)
            
            plt.title("1. Social Media Hours vs Physical Activity")
            plt.xlabel("Daily Social Media (Hours)")
            plt.ylabel("Physical Activity (Hours)")
            plt.grid(True, linestyle='--', alpha=0.6)
            
            self._save("scatter_plot.png")
            print("Scatter plot saved successfully!")

        except Exception as e:
            print("Scatter Plot Error:", e)

    # 2. 2D HISTOGRAM: Sleep hours at Screentime before sleep
    def histogram_plot(self):
        try:
            plt.figure(figsize=(8, 6))
            
            h = plt.hist2d(self.df["screen_time_before_sleep"], self.df["sleep_hours"], 
                           bins=6, cmap="Blues", edgecolor='white', linewidth=0.5)
            
            cbar = plt.colorbar(h[3])
            cbar.set_label('Total Number of Teens in this Range', fontweight='bold', fontsize=11)
            
            counts, xedges, yedges, image = h
            max_count = counts.max()
            
            for i in range(len(xedges)-1):
                for j in range(len(yedges)-1):
                    if counts[i, j] > 0: 
                        x_center = (xedges[i] + xedges[i+1]) / 2
                        y_center = (yedges[j] + yedges[j+1]) / 2
                        text_color = "white" if counts[i, j] > (max_count / 2) else "black"
                        
                        plt.text(x_center, y_center, int(counts[i, j]), 
                                 ha="center", va="center", color=text_color, fontsize=10, fontweight='bold')

            plt.title("4. Screen Time Before Sleep vs Sleep Hours (Density Grid)")
            plt.xlabel("Screen Time Before Sleep (Hours)")
            plt.ylabel("Hours of Sleep")
            
            self._save("histogram_plot.png")
            print("2D Histogram saved successfully!")

        except Exception as e:
            print("Histogram Error:", e)

    # 3. LINE GRAPH: Stress Level at Age (Saves as boxplot_chart.png for app compatibility)
    def boxplot_chart(self):
        try:
            plt.figure(figsize=(8, 6))
            line_data = self.df.groupby('age')['stress_level'].mean().reset_index()
            
            plt.plot(line_data['age'], line_data['stress_level'], marker='o', color='red', linewidth=2.5, label="Avg Stress Score")
            
            for i, val in enumerate(line_data['stress_level']):
                plt.text(line_data['age'].iloc[i], val + 0.1, f'{val:.1f}', 
                         ha='center', fontsize=10, fontweight='bold', color='darkred')
            
            plt.legend(title="Data Metric", loc="upper left")
            
            plt.title("3. Average Stress Level per Age")
            plt.xlabel("Age (Years Old)")
            plt.ylabel("Average Stress Level (Scale 1-10)")
            plt.xticks(line_data['age'].unique())
            plt.grid(True, linestyle='--', alpha=0.6)
            
            self._save("boxplot_chart.png")
            print("Line graph (saved as boxplot) successfully!")

        except Exception as e:
            print("Line Graph Error:", e)

    # 4. BAR GRAPH: Physical activity at Depression level (Saves as grouped_bar_chart.png)
    def grouped_bar_chart(self):
        try:
            plt.figure(figsize=(8, 6))
            bar_data = self.df.groupby('depression_label')['physical_activity'].mean().reset_index()
            bar_data['depression_label'] = bar_data['depression_label'].map({0: 'Normal', 1: 'Depressed'})
            
            colors = ['#66c2a5', '#fc8d62']
            bars = plt.bar(bar_data['depression_label'], bar_data['physical_activity'], color=colors)
            
            plt.bar_label(bars, fmt='%.2f hrs', padding=3, fontsize=12, fontweight='bold')
            
            legend_elements = [
                Patch(facecolor='#66c2a5', label='Normal (No Depression)'),
                Patch(facecolor='#fc8d62', label='Depressed Label')
            ]
            plt.legend(handles=legend_elements, title="Category Guide", loc="upper right")
            
            plt.title("5. Average Physical Activity by Depression Level")
            plt.xlabel("Clinical Assessment (Depression Level)")
            plt.ylabel("Average Physical Activity (Hours)")
            plt.ylim(0, bar_data['physical_activity'].max() * 1.3)
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            
            self._save("grouped_bar_chart.png")
            print("Bar chart saved successfully!")

        except Exception as e:
            print("Grouped Bar Chart Error:", e)

    # 5. PIE CHART: Social Media Hours at Social Interactions
    def pie_chart(self):
        try:
            plt.figure(figsize=(9, 6)) 
            pie_data = self.df.groupby('social_interaction_level', observed=False)['daily_social_media_hours'].sum()
            
            labels = pie_data.index.str.title()
            colors = ['#ff9999','#66b3ff','#99ff99']
            
            wedges, texts, autotexts = plt.pie(
                pie_data, labels=labels, autopct='%1.1f%%', 
                startangle=140, colors=colors,
                textprops={'fontsize': 11, 'weight': 'bold'}
            )
            
            plt.legend(wedges, labels, title="Interaction Levels", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            plt.title("2. Share of Social Media Hours per Social Interaction Level")
            
            self._save("pie_chart.png")
            print("Pie chart saved successfully!")

        except Exception as e:
            print("Pie Chart Error:", e)

    # GENERATE ALL CHARTS
    def generate_all_charts(self):
        try:
            self.scatter_plot()
            self.histogram_plot()
            self.boxplot_chart()
            self.grouped_bar_chart()
            self.pie_chart()
            print("\n✅ All 5 updated charts generated successfully with clean legends and labels!")

        except Exception as e:
            print("Visualization Error:", e)
