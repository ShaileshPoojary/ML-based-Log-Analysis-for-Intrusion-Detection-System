import streamlit as st
import joblib
import numpy as np
import pandas as pd
import altair as alt

# Load Models and Utilities
# MODEL_DIR = "C:/Users/shail/Desktop/Log_Analysis"

MODELS = {
    "Random Forest": joblib.load("C:/Users/shail/Desktop/Log_Analysis/random_forest.pkl"),
    "Logistic Regression": joblib.load("C:/Users/shail/Desktop/Log_Analysis/logistic_regression.pkl"),
    "XGBoost": joblib.load("C:/Users/shail/Desktop/Log_Analysis/xgboost.pkl"),
    "Gradient Boosting": joblib.load("C:/Users/shail/Desktop/Log_Analysis/gradient_boosting.pkl"),
    "KNN": joblib.load("C:/Users/shail/Desktop/Log_Analysis/knn.pkl")
}

vectorizer = joblib.load("C:/Users/shail/Desktop/Log_Analysis/vectorizer.pkl")
call_to_int = joblib.load("C:/Users/shail/Desktop/Log_Analysis/call_to_int.pkl")


# Helper: Read and encode .GHC

def read_ghc(file):
    """Read uploaded .GHC file and return encoded text."""
    content = file.read().decode("utf-8", errors="ignore")
    tokens = []
    for line in content.splitlines():
        tokens.extend(line.strip().split())
    encoded = " ".join(str(call_to_int[c]) for c in tokens if c in call_to_int)
    return encoded

# Streamlit UI

st.set_page_config(page_title="Intrusion Detection Dashboard", layout="wide")

st.title("ML-Based Intrusion Detection System")
st.write("Upload a `.GHC` file to detect if it represents a **Normal** or **Attack** trace using trained ML models.")

uploaded_file = st.file_uploader("Upload your `.GHC` file", type=["GHC", "ghc"])

if uploaded_file:
    encoded_text = read_ghc(uploaded_file)
    X_new = vectorizer.transform([encoded_text])

    st.markdown("Model Predictions")

    results = []
    for model_name, model in MODELS.items():
        try:
            pred = model.predict(X_new)[0]
            prob = model.predict_proba(X_new)[0] if hasattr(model, "predict_proba") else [0.5, 0.5]
            attack_prob = prob[1]
            normal_prob = prob[0]
            label = "Attack" if pred == 1 else "Normal"
            results.append({
                "Model": model_name,
                "Prediction": label,
                "Normal Probability": round(normal_prob * 100, 2),
                "Attack Probability": round(attack_prob * 100, 2)
                
            })
        except Exception as e:
            st.error(f"Error with {model_name}: {e}")

    df = pd.DataFrame(results)

    st.dataframe(df, use_container_width=True)

    
    # Visualization

    st.markdown("Interactive Model Comparison")

    chart_data = df.melt(
        id_vars=["Model", "Prediction"],
        value_vars=["Normal Probability","Attack Probability"],
        var_name="Type",
        value_name="Percentage"
    )

    chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X("Model:N", sort="-y"),
            y=alt.Y("Percentage:Q"),
            color="Type:N",
            tooltip=["Model", "Type", "Percentage"]
        )
        .properties(width=700, height=400)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)


    # Overall Summary
  
    st.markdown("Summary")
    attack_avg = df["Attack Probability"].mean()
    normal_avg = df["Normal Probability"].mean()
    st.info(f"Average Attack Probability: **{attack_avg:.2f}%**")
    st.info(f"Average Normal Probability: **{normal_avg:.2f}%**")

    if attack_avg > normal_avg:
        st.error("Potential Attack Detected! This file shows malicious patterns.")
    else:
        st.success("Normal behavior detected.")
