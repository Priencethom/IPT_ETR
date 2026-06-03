import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# LOAD DATASET
# =========================================================
try:
    df = pd.read_csv("cleaned_teen_mental_dataset.csv")
    print("✅ Dataset loaded successfully!\n")
except FileNotFoundError:
    print("❌ Dataset file not found. Please make sure the CSV is in the same folder.")
    exit()

# Isaayos ang order ng social interaction level para tama ang sunod-sunod sa graphs
if 'social_interaction_level' in df.columns:
    df['social_interaction_level'] = pd.Categorical(
        df['social_interaction_level'], 
        categories=['low', 'medium', 'high'], 
        ordered=True
    )

class MentalHealthVisualization:

    def __init__(self, df):
        self.df = df
        sns.set_theme(style="whitegrid") # Para malinis ang background ng charts

    # 1. Scatter Plot: Social Media Hours vs Physical Activity
    def analyze_social_vs_physical(self):
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=self.df, x="daily_social_media_hours", y="physical_activity", alpha=0.5, color="purple")
        
        plt.title("1. Social Media Hours vs Physical Activity (Scatter Plot)")
        plt.xlabel("Daily Social Media (Hours)")
        plt.ylabel("Physical Activity (Hours)")
        plt.tight_layout()
        plt.savefig("1_scatter_plot.png")
        plt.close()
        
        print("===== 1. SOCIAL MEDIA VS PHYSICAL ACTIVITY =====")
        print("Interpretation: Ang scatter plot na ito ay nagpapakita kung bumababa ba ang oras sa pag-eehersisyo kapag mas matagal nakatambay sa social media ang isang bata.")

    # 2. Pie Chart: Social Media Hours at Social Interactions
    def analyze_social_vs_interaction(self):
        plt.figure(figsize=(8, 6))
        # Kunin ang total na oras sa social media per social interaction level
        pie_data = self.df.groupby('social_interaction_level', observed=False)['daily_social_media_hours'].sum()
        
        plt.pie(pie_data, labels=pie_data.index.str.title(), autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
        plt.title("2. Share of Social Media Hours per Social Interaction Level (Pie Chart)")
        plt.tight_layout()
        plt.savefig("2_pie_chart.png")
        plt.close()

        print("\n===== 2. SOCIAL MEDIA HOURS & SOCIAL INTERACTION =====")
        print("Interpretation: Ipinapakita ng pie chart kung aling grupo (Low, Medium, High social interaction) ang may pinakamalaking ambag sa kabuuang oras ng paggamit ng social media.")

    # 3. Line Graph: Stress Level at Age
    def analyze_stress_vs_age(self):
        plt.figure(figsize=(8, 6))
        # Kunin ang average stress level per age
        line_data = self.df.groupby('age')['stress_level'].mean().reset_index()
        
        sns.lineplot(data=line_data, x='age', y='stress_level', marker='o', color='red', linewidth=2.5)
        plt.title("3. Average Stress Level per Age (Line Graph)")
        plt.xlabel("Age")
        plt.ylabel("Average Stress Level (1-10)")
        plt.xticks(line_data['age'].unique())
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig("3_line_graph.png")
        plt.close()

        print("\n===== 3. STRESS LEVEL & AGE =====")
        print("Interpretation: Nakikita sa line graph kung tumataas o bumababa ba ang average stress level habang tumatanda ang mga kabataan (mula age 13 hanggang 19).")

    # 4. Histogram (2D): Sleep hours at Screentime before sleep
    def analyze_sleep_vs_screentime(self):
        plt.figure(figsize=(8, 6))
        # Ginamit natin ang 2D Histogram para ipakita ang density o dami ng tao
        sns.histplot(data=self.df, x="screen_time_before_sleep", y="sleep_hours", bins=15, cbar=True, cmap="Blues")
        
        plt.title("4. Screen Time Before Sleep vs Sleep Hours (2D Histogram)")
        plt.xlabel("Screen Time Before Sleep (Hours)")
        plt.ylabel("Sleep (Hours)")
        plt.tight_layout()
        plt.savefig("4_histogram.png")
        plt.close()

        print("\n===== 4. SLEEP HOURS & SCREENTIME BEFORE SLEEP =====")
        print("Interpretation: Ipinapakita ng histogram kung saan nagkukumpulan ang karamihan ng mga kabataan. Mas madilim ang kulay blue, mas maraming tao doon. Kadalasan, ang mataas na screen time ay may katumbas na mas maikling tulog.")

    # 5. Bar Graph: Physical activity at Depression level
    def analyze_physical_vs_depression(self):
        plt.figure(figsize=(8, 6))
        # Ihiwalay ang Normal (0) at Depressed (1)
        bar_data = self.df.groupby('depression_label')['physical_activity'].mean().reset_index()
        bar_data['depression_label'] = bar_data['depression_label'].map({0: 'Normal', 1: 'Depressed'})
        
        sns.barplot(data=bar_data, x='depression_label', y='physical_activity', palette='Set2')
        plt.title("5. Average Physical Activity by Depression Level (Bar Graph)")
        plt.xlabel("Depression Level")
        plt.ylabel("Average Physical Activity (Hours)")
        plt.tight_layout()
        plt.savefig("5_bar_graph.png")
        plt.close()

        print("\n===== 5. PHYSICAL ACTIVITY & DEPRESSION LEVEL =====")
        print("Interpretation: Kinukumpara ng bar graph na ito kung sino ang mas mataas ang average na oras ng pag-eehersisyo: ang mga normal o ang mga kabataang may depression label.")

    def generate_all_visualizations(self):
        self.analyze_social_vs_physical()
        self.analyze_social_vs_interaction()
        self.analyze_stress_vs_age()
        self.analyze_sleep_vs_screentime()
        self.analyze_physical_vs_depression()
        print("\n✅ All 5 visualizations successfully generated and saved as images!")

# =========================================================
# EXECUTE THE CLASS
# =========================================================
if __name__ == "__main__":
    viz = MentalHealthVisualization(df)
    viz.generate_all_visualizations()