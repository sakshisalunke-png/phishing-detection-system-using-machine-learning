from pathlib import Path
import json
import joblib
import streamlit as st

from features import extract_url_features, make_feature_frame

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "artifacts" / "phishing_model.joblib"
METRICS_PATH = ROOT / "artifacts" / "metrics.json"

st.set_page_config(page_title="AI Phishing Detection", page_icon="🛡️", layout="centered")
st.title("🛡️ AI-Powered Phishing Detection")
st.write("Enter a URL to estimate whether its URL characteristics resemble phishing links in the training data.")
st.warning("Educational prototype only. A prediction is not a guarantee of safety. Do not enter passwords or other private information.")

if not MODEL_PATH.exists():
    st.error("The trained model was not found. First run `python train_model.py` in the project folder.")
    st.stop()

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
best_model_name = bundle.get("best_model_name", "Selected model")

url = st.text_input("Website URL", placeholder="https://example.com/login")
if st.button("Check URL", type="primary", use_container_width=True):
    if not url.strip():
        st.error("Please enter a URL.")
    elif any(ch.isspace() for ch in url.strip()):
        st.error("Please enter a URL without spaces.")
    else:
        features = extract_url_features(url)
        frame = make_feature_frame([url])
        prediction = int(model.predict(frame)[0])
        probabilities = model.predict_proba(frame)[0] if hasattr(model, "predict_proba") else None
        phishing_probability = float(probabilities[1]) if probabilities is not None else None

        if prediction == 1:
            st.error("Prediction: Potentially Phishing")
            st.write("Treat this link cautiously. Avoid entering credentials or payment details.")
        else:
            st.success("Prediction: Likely Legitimate")
            st.write("This model did not identify strong phishing patterns in the URL. This does not prove the site is safe.")

        if phishing_probability is not None:
            st.metric("Model-estimated phishing probability", f"{phishing_probability:.1%}")
        st.caption(f"Model used: {best_model_name}")

        indicators = []
        if features["has_ip_address"]:
            indicators.append("The hostname is an IP address.")
        if features["has_suspicious_word"]:
            indicators.append("The URL contains a word often used in account or verification lures.")
        if features["has_shortener_domain"]:
            indicators.append("The URL uses a known URL-shortening domain.")
        if features["has_punycode"]:
            indicators.append("The hostname contains an internationalized-domain encoding marker.")
        if features["count_at"]:
            indicators.append("The URL contains an @ symbol.")
        if features["url_length"] > 75:
            indicators.append("The URL is relatively long.")
        if not features["has_https_scheme"]:
            indicators.append("The URL does not use HTTPS.")
        if indicators:
            st.subheader("URL characteristics to review")
            for item in indicators:
                st.write(f"- {item}")
        else:
            st.info("No indicators from this small explanatory checklist were triggered. The model may still classify the URL as suspicious.")

st.divider()
st.subheader("About this project")
st.write("The model is trained on labeled URL data and uses URL-only features. It does not open or visit the submitted website.")
if METRICS_PATH.exists():
    with open(METRICS_PATH, encoding="utf-8") as f:
        metrics = json.load(f)
    st.subheader("Model comparison")
    st.dataframe(
        [{k: round(v, 4) for k, v in row.items() if k != "tn_fp_fn_tp"} for row in metrics],
        use_container_width=True
    )
