import numpy as np

#====================PAM====================

class DataAnalytics:

    def __init__(self, df):
        self.df = df

    def summary_statistics(self):

        print("\n===== SUMMARY STATISTICS =====")

        cols = [
            "daily_social_media_hours",
            "academic_performance",
            "stress_level",
            "sleep_hours"
        ]

        for col in cols:
            try:
                print(f"\n{col}")
                print("Average:", np.mean(self.df[col]))
                print("Median:", np.median(self.df[col]))
                print("Std Dev:", np.std(self.df[col]))
                print("Min:", np.min(self.df[col]))
                print("Max:", np.max(self.df[col]))

            except Exception as e:
                print(f"{col} Error:", e)

    def correlation_analysis(self):

        print("\n===== CORRELATION ANALYSIS =====")

        pairs = [
            ("daily_social_media_hours", "academic_performance"),
            ("sleep_hours", "stress_level"),
            ("addiction_level", "depression_label")
        ]

        for x, y in pairs:
            try:
                corr = np.corrcoef(self.df[x], self.df[y])[0, 1]
                print(f"{x} vs {y}: {corr}")

            except Exception as e:
                print("Error:", e)

    def grouped_analysis(self):

        print("\n===== GENDER ANALYSIS =====")

        try:
            print(
                self.df.groupby("gender")[
                    ["stress_level", "sleep_hours"]
                ].mean()
            )

        except Exception as e:
            print("Error:", e)

        print("\n===== PLATFORM ANALYSIS =====")

        try:
            print(
                self.df.groupby("platform_usage")[
                    ["daily_social_media_hours"]
                ].mean()
            )

        except Exception as e:
            print("Error:", e)

        print("\n===== USAGE LEVEL ANALYSIS =====")

        try:
            print(
                self.df.groupby("Social_Media_Usage_Level")[
                    ["academic_performance"]
                ].mean()
            )

        except Exception as e:
            print("Error:", e)

    # KPI DASHBOARD
    def dashboard_kpis(self):

        print("\n===== KPI DASHBOARD =====")

        try:
            print("Total Students:", len(self.df))
            print(
                "Average Social Media Hours:",
                round(np.mean(self.df["daily_social_media_hours"]), 2)
            )

            print(
                "Average Sleep Hours:",
                round(np.mean(self.df["sleep_hours"]), 2)
            )

            print(
                "Average Stress Level:",
                round(np.mean(self.df["stress_level"]), 2)
            )

        except Exception as e:
            print("Error:", e)

#====================PAM====================