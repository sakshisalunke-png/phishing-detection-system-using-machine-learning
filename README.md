# AI-Powered Phishing Detection System

A college mini-project that trains machine-learning classifiers using URL-only characteristics and provides a Streamlit interface to estimate whether a URL may be phishing.

## Tools
- Python
- pandas
- scikit-learn
- UCI Machine Learning Repository (`ucimlrepo`)
- Streamlit
- joblib
- Git/GitHub (optional but recommended)

## Dataset
UCI PhiUSIIL Phishing URL (Website) Dataset, ID 967:
https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset

The training script uses the dataset's raw URL column and binary label, then derives a consistent set of URL-only features. In the UCI dataset, label 1 means legitimate and label 0 means phishing; the script converts this to `phishing=1`.

## Setup (Windows PowerShell)
1. Install Python 3.11 or 3.12 and Git.
2. Open this folder in VS Code.
3. In the VS Code terminal run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this for the current terminal only:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Train and evaluate
Internet access is required to fetch the UCI dataset the first time.

```powershell
python train_model.py
```

The script:
- removes missing and duplicate URL records;
- derives URL-only features;
- makes a stratified 80/20 train-test split;
- trains Logistic Regression, Decision Tree and Random Forest;
- calculates accuracy, precision, recall, F1-score and ROC-AUC;
- saves the best model by F1-score and a comparison CSV/JSON in `artifacts/`.

Record the actual output in your college report. Do not invent results.

## Run the application
```powershell
streamlit run app.py
```
The browser should open the local app. Enter a URL and select **Check URL**.

## Limitations
- URL-only analysis cannot inspect page content, redirects, certificates, domain registration records or website behavior.
- Attackers can make malicious URLs look normal, and legitimate URLs can look unusual.
- The dataset may not represent every current threat; performance on unseen URLs can differ.
- A probability is a model estimate, not a verified real-world risk score.
- Never use the prototype as the only security control.

## Suggested report note
Explain that this prototype prioritizes an accessible demonstration of URL-feature engineering and supervised classification. The deployed app does not fetch or open the entered URL.
