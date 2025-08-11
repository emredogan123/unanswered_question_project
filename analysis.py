import pandas as pd
import matplotlib.pyplot as plt

def run_analysis(csv_path):
    """
    Analyzes a labeled conversation dataset (CSV) and prints summary stats + samples.
    Also shows optional bar chart of intent distribution.
    """

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"❌ File not found: {csv_path}")
        return
    except Exception as e:
        print(f"❌ Error while reading file: {e}")
        return

    print("📂 Loaded:", csv_path)
    print("🔢 Total number of rows:", len(df))

    print("\n📊 Answered status:")
    print(df["answered"].value_counts(), "\n")

    print("📊 Sentiment distribution:")
    print(df["sentiment"].value_counts(), "\n")

    print("📊 Category distribution:")
    print(df["category"].value_counts(), "\n")

    print("📊 Intent distribution:")
    print(df["intent"].value_counts(), "\n")

    print("📝 Random 10 sample messages:")
    print(df.sample(10)[["message", "answered", "sentiment", "category", "intent"]], "\n")

    unclear = df[(df["intent"] == "Belirsiz") | (df["category"] == "Diğer")]
    print("⚠️ Rows with unclear intent or unknown category:")
    print(unclear.sample(min(10, len(unclear)))[["message", "intent", "category"]], "\n")

    plot = input("📊 Would you like to see a graph of intent distribution? (y/n): ").lower()
    if plot == "y":
        df["intent"].value_counts().plot(kind="bar", title="Intent Distribution", ylabel="Count")
        plt.tight_layout()
        plt.show()
