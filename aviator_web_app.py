
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aviator Pattern Analyzer", layout="wide")

st.title("🎯 Aviator Crash Pattern Analyzer")

uploaded_file = st.file_uploader("Upload CSV file with crash multipliers", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'Multiplier' not in df.columns:
        st.error("CSV must contain a 'Multiplier' column.")
    else:
        df['Round'] = df.index + 1
        df['MovingAvg'] = df['Multiplier'].rolling(window=5).mean()

        high_multipliers = df[df['Multiplier'] >= 10]
        low_multipliers = df[df['Multiplier'] <= 1.5]
        avg = df['Multiplier'].mean()

        st.subheader("📈 Multiplier Chart")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['Round'], df['Multiplier'], label='Crash Multiplier', marker='o')
        ax.plot(df['Round'], df['MovingAvg'], label='5-Round Avg', color='orange')
        ax.scatter(high_multipliers['Round'], high_multipliers['Multiplier'], color='green', label='High (10x+)', zorder=5)
        ax.scatter(low_multipliers['Round'], low_multipliers['Multiplier'], color='red', label='Low (≤1.5x)', zorder=5)
        ax.set_xlabel("Round")
        ax.set_ylabel("Multiplier")
        ax.set_title("Aviator Crash Multiplier Pattern")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        st.subheader("📊 Summary")
        st.write({
            "Total Rounds": len(df),
            "High Multipliers (10x+)": len(high_multipliers),
            "Low Multipliers (≤1.5x)": len(low_multipliers),
            "Average Multiplier": round(avg, 2),
            "Max Multiplier": df['Multiplier'].max()
        })
else:
    st.info("Please upload a CSV file to begin.")
