import numpy as np

#====================PAM====================

class DataAnalytics:

    def __init__(self, df):
        self.df = df

    def summary_statistics(self):

        stats = {}

        cols = [
            'age',
            'daily_social_media_hours',
            'sleep_hours',
            'screen_time_before_sleep',
            'academic_performance',
            'physical_activity',
            'stress_level',
            'anxiety_level',
            'addiction_level'
        ]

        for col in cols:

            stats[col] = {
                "average": round(
                    np.mean(self.df[col]), 2
                ),
                "median": round(
                    np.median(self.df[col]), 2
                ),
                "std_dev": round(
                    np.std(self.df[col]), 2
                ),
                "min": round(
                    np.min(self.df[col]), 2
                ),
                "max": round(
                    np.max(self.df[col]), 2
                )
            }

        return stats

    def grouped_analysis(self):

        results = {}

        # Gender Analysis
        gender_data = self.df.groupby("gender")[["stress_level", "sleep_hours"]].mean()

        results["gender_analysis"] = (gender_data.round(2).to_dict())

        # Platform Analysis
        platform_data = self.df.groupby("platform_usage")[["daily_social_media_hours"]].mean()

        results["platform_analysis"] = (platform_data.round(2).to_dict())

        # Usage Level Analysis
        usage_data = self.df.groupby("Social_Media_Usage_Level")[["academic_performance"]].mean()

        results["usage_level_analysis"] = (usage_data.round(2).to_dict())

        return results

    # KPI DASHBOARD
    def get_kpis(self):

        return {
            "avg_usage": round(np.mean(self.df["daily_social_media_hours"]), 2),

            "avg_academic": round(np.mean(self.df["academic_performance"]), 2),

            "avg_stress": round(np.mean(self.df["stress_level"]), 2),

            "avg_sleep": round(np.mean(self.df["sleep_hours"]), 2),

            "avg_anxiety": round(np.mean(self.df["anxiety_level"]), 2),

            "total_students": len(self.df)
        }
    
    def get_correlation(self):

        correlation = self.df[
            "daily_social_media_hours"
        ].corr(
            self.df["academic_performance"]
        )

        return round(correlation, 2)
    
    def get_platform_data(self):

        platform_counts = self.df["platform_usage"].value_counts()
        total = platform_counts.sum()
        platform_data = []

        for platform in platform_counts.index:
            count = platform_counts[platform]
            percentage = round(
                (count / total) * 100,
                1
            )
            platform_data.append({
                "name": platform,
                "count": count,
                "pct": percentage
            })
        return platform_data

#====================PAM====================
