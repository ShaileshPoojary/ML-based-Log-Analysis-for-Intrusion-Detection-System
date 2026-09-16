# import streamlit as st
# import joblib
# import numpy as np
# import pandas as pd
# import altair as alt


# MODELS = {
#     "Random Forest": joblib.load("Models/random_forest.pkl"),
#     "Logistic Regression": joblib.load("Models/logistic_regression.pkl"),
#     "XGBoost": joblib.load("Models/xgboost.pkl"),
#     "Gradient Boosting": joblib.load("Models/gradient_boosting.pkl"),
#     "KNN": joblib.load("Models/knn.pkl")
# }

# vectorizer = joblib.load("vectorizer.pkl")
# call_to_int = joblib.load("call_to_int.pkl")


# # Helper: Read and encode .GHC

# def read_ghc(file):
#     """Read uploaded .GHC file and return encoded text."""
#     content = file.read().decode("utf-8", errors="ignore")
#     tokens = []
#     for line in content.splitlines():
#         tokens.extend(line.strip().split())
#     encoded = " ".join(str(call_to_int[c]) for c in tokens if c in call_to_int)
#     return encoded

# # Streamlit UI

# st.set_page_config(page_title="Intrusion Detection Dashboard", layout="wide")

# st.title("ML-Based Intrusion Detection System")
# st.write("Upload a `.GHC` file to detect if it represents a **Normal** or **Attack** trace using trained ML models.")

# uploaded_file = st.file_uploader("Upload your `.GHC` file", type=["GHC", "ghc"])

# if uploaded_file:
#     encoded_text = read_ghc(uploaded_file)
#     X_new = vectorizer.transform([encoded_text])

#     st.markdown("Model Predictions")

#     results = []
#     for model_name, model in MODELS.items():
#         try:
#             pred = model.predict(X_new)[0]
#             prob = model.predict_proba(X_new)[0] if hasattr(model, "predict_proba") else [0.5, 0.5]
#             attack_prob = prob[1]
#             normal_prob = prob[0]
#             label = "Attack" if pred == 1 else "Normal"
#             results.append({
#                 "Model": model_name,
#                 "Prediction": label,
#                 "Normal Probability": round(normal_prob * 100, 2),
#                 "Attack Probability": round(attack_prob * 100, 2)
                
#             })
#         except Exception as e:
#             st.error(f"Error with {model_name}: {e}")

#     df = pd.DataFrame(results)

#     st.dataframe(df, use_container_width=True)

    
#     # Visualization

#     st.markdown("Interactive Model Comparison")

#     chart_data = df.melt(
#         id_vars=["Model", "Prediction"],
#         value_vars=["Normal Probability","Attack Probability"],
#         var_name="Type",
#         value_name="Percentage"
#     )

#     chart = (
#         alt.Chart(chart_data)
#         .mark_bar()
#         .encode(
#             x=alt.X("Model:N", sort="-y"),
#             y=alt.Y("Percentage:Q"),
#             color="Type:N",
#             tooltip=["Model", "Type", "Percentage"]
#         )
#         .properties(width=700, height=400)
#         .interactive()
#     )

#     st.altair_chart(chart, use_container_width=True)


#     # Overall Summary
  
#     st.markdown("Summary")
#     attack_avg = df["Attack Probability"].mean()
#     normal_avg = df["Normal Probability"].mean()
#     st.info(f"Average Attack Probability: **{attack_avg:.2f}%**")
#     st.info(f"Average Normal Probability: **{normal_avg:.2f}%**")

#     if attack_avg > normal_avg:
#         st.error("Potential Attack Detected! This file shows malicious patterns.")
#     else:
#         st.success("Normal behavior detected.")

import streamlit as st
import joblib
import pandas as pd
import altair as alt
from pathlib import Path


# ============================================================
# Paths and Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "Models"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# ============================================================
# Load Models
# ============================================================

@st.cache_resource
def load_models():

    models = {
        "Random Forest": joblib.load(MODEL_DIR / "random_forest.pkl"),
        "Logistic Regression": joblib.load(
            MODEL_DIR / "logistic_regression.pkl"
        ),
        "XGBoost": joblib.load(MODEL_DIR / "xgboost.pkl"),
        "Gradient Boosting": joblib.load(
            MODEL_DIR / "gradient_boosting.pkl"
        ),
        "KNN": joblib.load(MODEL_DIR / "knn.pkl")
    }

    vectorizer = joblib.load(BASE_DIR / "vectorizer.pkl")
    call_to_int = joblib.load(BASE_DIR / "call_to_int.pkl")

    return models, vectorizer, call_to_int


MODELS, vectorizer, call_to_int = load_models()


# ============================================================
# Helper: Read and Encode .GHC
# ============================================================

def read_ghc(file):
    """Read uploaded .GHC file and return encoded text."""

    content = file.read().decode("utf-8", errors="ignore")

    tokens = []

    for line in content.splitlines():
        tokens.extend(line.strip().split())

    recognized_calls = [
        call_to_int[c]
        for c in tokens
        if c in call_to_int
    ]

    # No known system calls found
    if not recognized_calls:
        return None

    encoded = " ".join(
        str(call) for call in recognized_calls
    )

    return encoded


# ============================================================
# Helper: Get Normal / Attack Probabilities
# ============================================================

def get_probabilities(model, X_new):
    """
    Get prediction probabilities using the model's actual
    class ordering instead of assuming:
    prob[0] = Normal
    prob[1] = Attack
    """

    prediction = model.predict(X_new)[0]

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(X_new)[0]
        classes = model.classes_

        normal_index = None
        attack_index = None

        for index, class_value in enumerate(classes):

            class_value = str(class_value).strip().lower()

            if class_value in ["0", "normal", "benign"]:
                normal_index = index

            elif class_value in [
                "1",
                "attack",
                "malicious",
                "anomaly"
            ]:
                attack_index = index

        # Both classes were successfully identified
        if normal_index is not None and attack_index is not None:

            normal_prob = probabilities[normal_index]
            attack_prob = probabilities[attack_index]

        else:
            # Fallback for unexpected class labels
            normal_prob = 0.0
            attack_prob = 0.0

    else:
        # Fallback for models without predict_proba
        prediction_value = str(prediction).strip().lower()

        if prediction_value in [
            "1",
            "attack",
            "malicious",
            "anomaly"
        ]:
            attack_prob = 1.0
            normal_prob = 0.0
        else:
            attack_prob = 0.0
            normal_prob = 1.0

    return prediction, normal_prob, attack_prob


# ============================================================
# Streamlit UI
# ============================================================

st.set_page_config(
    page_title="Intrusion Detection Dashboard",
    layout="wide"
)

st.title("ML-Based Intrusion Detection System")

st.write(
    "Upload a `.GHC` file to detect if it represents a "
    "**Normal** or **Attack** trace using trained ML models."
)


# ============================================================
# File Upload
# ============================================================

uploaded_file = st.file_uploader(
    "Upload your `.GHC` file",
    type=["GHC", "ghc"]
)


if uploaded_file:

    # --------------------------------------------------------
    # File Size Check
    # --------------------------------------------------------

    if uploaded_file.size > MAX_FILE_SIZE:

        st.error(
            "File is too large. Please upload a file "
            "smaller than 10 MB."
        )

        st.stop()


    # --------------------------------------------------------
    # Read and Encode File
    # --------------------------------------------------------

    try:

        encoded_text = read_ghc(uploaded_file)

    except Exception as e:

        st.error(
            f"Error while reading the file: {e}"
        )

        st.stop()


    # --------------------------------------------------------
    # Check for Recognized Calls
    # --------------------------------------------------------

    if not encoded_text:

        st.error(
            "No recognized system calls were found "
            "in this GHC file."
        )

        st.info(
            "Please upload a GHC trace that uses the same "
            "system-call representation used during training."
        )

        st.stop()


    # --------------------------------------------------------
    # Vectorization
    # --------------------------------------------------------

    try:

        X_new = vectorizer.transform([encoded_text])

    except Exception as e:

        st.error(
            f"Error during feature extraction: {e}"
        )

        st.stop()


    # ========================================================
    # Model Predictions
    # ========================================================

    st.markdown("Model Predictions")

    results = []

    for model_name, model in MODELS.items():

        try:

            pred, normal_prob, attack_prob = get_probabilities(
                model,
                X_new
            )

            # Convert prediction to readable label
            pred_value = str(pred).strip().lower()

            if pred_value in [
                "1",
                "attack",
                "malicious",
                "anomaly"
            ]:
                label = "Attack"
            else:
                label = "Normal"


            results.append({
                "Model": model_name,
                "Prediction": label,
                "Normal Probability": round(
                    normal_prob * 100,
                    2
                ),
                "Attack Probability": round(
                    attack_prob * 100,
                    2
                )
            })

        except Exception as e:

            st.error(
                f"Error with {model_name}: {e}"
            )


    # ========================================================
    # Results Table
    # ========================================================

    if not results:

        st.error(
            "No model was able to process this file."
        )

        st.stop()


    df = pd.DataFrame(results)

    st.dataframe(
        df,
        use_container_width=True
    )


    # ========================================================
    # Visualization
    # ========================================================

    st.markdown("Interactive Model Comparison")

    chart_data = df.melt(
        id_vars=["Model", "Prediction"],
        value_vars=[
            "Normal Probability",
            "Attack Probability"
        ],
        var_name="Type",
        value_name="Percentage"
    )

    chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Model:N",
                sort="-y"
            ),
            y=alt.Y(
                "Percentage:Q"
            ),
            color="Type:N",
            tooltip=[
                "Model",
                "Prediction",
                "Type",
                "Percentage"
            ]
        )
        .properties(
            width=700,
            height=400
        )
        .interactive()
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # Overall Summary
    # ========================================================

    st.markdown("Summary")

    attack_avg = df["Attack Probability"].mean()
    normal_avg = df["Normal Probability"].mean()

    st.info(
        f"Average Attack Probability: "
        f"**{attack_avg:.2f}%**"
    )

    st.info(
        f"Average Normal Probability: "
        f"**{normal_avg:.2f}%**"
    )


    # ========================================================
    # Model Consensus
    # ========================================================

    attack_predictions = (
        df["Prediction"] == "Attack"
    ).sum()

    normal_predictions = (
        df["Prediction"] == "Normal"
    ).sum()


    if attack_predictions > normal_predictions:

        st.error(
            f"Potential Attack Detected! "
            f"{attack_predictions} of {len(df)} models "
            f"classified the trace as Attack."
        )

    elif normal_predictions > attack_predictions:

        st.success(
            f"Normal behavior detected. "
            f"{normal_predictions} of {len(df)} models "
            f"classified the trace as Normal."
        )

    else:

        st.warning(
            "Model predictions are inconclusive. "
            "The models produced an equal number of "
            "Normal and Attack predictions."
        )


    st.caption(
        "Note: Model probabilities are predictions from "
        "individual classifiers and should not be considered "
        "a guaranteed security verdict."
    )