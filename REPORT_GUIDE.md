# Report writing guide — follow the college template

Use the college's 15 section headings in the same order. Replace all placeholders with your actual names, guide, roll number, screenshots and measured results. Format as A4, Times New Roman 12 pt body, 1.5 spacing, 1-inch margins, justified text, numbered figures/tables and IEEE-style references as specified by the template.

## 1. Introduction
Phishing is a social-engineering attack in which a malicious actor tries to trick users into revealing credentials, payment details or other sensitive information. This project develops a machine-learning prototype that examines characteristics of a submitted URL and predicts whether it resembles phishing URLs in a labeled dataset. The system uses Python, feature engineering and supervised classification, then presents the result through a Streamlit web interface. It is an educational decision-support tool, not a guarantee that a website is safe.

## 2. Motivation
Users may be deceived by URLs that imitate trusted brands or use misleading words and structures. A simple automated warning can help users pause before interacting with a suspicious link. The project was selected to apply data preprocessing, feature engineering, classification, evaluation and deployment to a real cybersecurity problem.

## 3. Literature Survey
Create a table with at least five verified sources. Include author(s), year, title, dataset, method, findings and limitations. Suggested starting points:
- Mohammad, Thabtah and McCluskey, “An assessment of features related to phishing websites using an automated technique,” 2012.
- Abdelhamid, Ayesh and Thabtah, “Phishing detection based Associative Classification data mining,” 2014.
- Prasad and Chandra, “PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning,” Computers & Security, 2024.
- UCI PhiUSIIL dataset documentation.
- Official scikit-learn documentation for classification metrics.
Verify bibliographic details before final submission.

## 4. Dataset Used
Dataset: UCI PhiUSIIL Phishing URL (Website) Dataset, ID 967. UCI reports 235,795 instances and 54 features; it contains a raw URL field and label. The training script uses the raw URL and label to construct its own URL-only feature set. Label 1 in the source denotes legitimate and label 0 denotes phishing; the script converts the target so 1 denotes phishing. Report the exact record count after the script's cleaning step, not just the published dataset count.

Feature table to include: URL length, hostname length, path length, query length, counts of dots/hyphens/underscores/slashes/@/?/=/%, digit count, letter count, subdomain count, IP-host flag, HTTPS flag, suspicious-word flag, URL-shortener flag, explicit-port flag, punycode flag. Target: phishing (1) or legitimate (0) after conversion.

## 5. Flow Diagram / Block Diagram
Use this flow:
Dataset collection → URL cleaning and label conversion → URL feature extraction → Stratified train/test split (80/20) → Train Logistic Regression / Decision Tree / Random Forest → Evaluate metrics → Select best model by F1-score → Save model → Streamlit URL input → Feature extraction → Prediction and warning.

## 6. Methods Used / Technology Stack
Python; pandas for tabular data; scikit-learn for splitting, classifiers and metrics; ucimlrepo to fetch the UCI dataset; joblib to save the model; Streamlit for the interface; Git/GitHub if actually used. Mention hardware and software versions from your actual system.

## 7. Model Development
7.1 Preprocessing: select URL and target columns, remove missing rows and duplicate URLs, convert target to numeric, retain binary labels, map source labels to phishing=1.
7.2 EDA: create class-count plot, URL-length distribution and summary statistics before writing conclusions.
7.3 Feature engineering: derive the 21 URL-only features implemented in `features.py`.
7.4 Model selection: Logistic Regression (`max_iter=2000`, balanced class weights); Decision Tree (`max_depth=12`, balanced class weights); Random Forest (`n_estimators=200`, `min_samples_leaf=2`, balanced subsample weights).
7.5 Training: stratified 80/20 train-test split, random state 42. Avoid tuning on the test set; if you add cross-validation, document it and rerun the experiments.
7.6 Evaluation: report accuracy, precision, recall, F1-score, ROC-AUC and confusion matrix. Phishing recall is important because false negatives may leave malicious URLs undetected; precision also matters because false positives inconvenience users.

## 8. Version Control
If using Git, create a repository, commit code in logical steps, add a README and .gitignore, and insert screenshots of the actual repository. Do not claim pull requests or multiple contributors unless used.

## 9. Experiment Tracking
The training script saves measured metrics to `artifacts/metrics.json` and `artifacts/model_comparison.csv`. Use these actual values in the experiment table. This is basic file-based tracking, not MLflow or Weights & Biases.

## 10. AutoML / MLOps
If no AutoML or full MLOps tool is implemented, state that these were not implemented and briefly describe the limited practices actually used (repeatable training script, saved model, Git if used). Do not claim a model registry or CI/CD pipeline without implementing it.

## 11. Deployment
Local deployment: train and save model, then run `streamlit run app.py`. If you deploy to Streamlit Community Cloud, add a requirements file and upload the code to GitHub, then include the actual deployment URL and screenshots. Do not claim cloud deployment before it works.

## 12. Results and Discussions
Fill tables from the actual `model_comparison.csv`. Include confusion matrix, screenshots of at least two example predictions, and explain the trade-off between false positives and false negatives. Do not copy example metrics from another project.

## 13. Future Scope
Potential extensions: more recent and diverse data, HTML/page-level features in a safe sandbox, domain reputation and certificate signals, multilingual phishing detection, browser extension, explainable predictions, drift monitoring and periodic retraining.

## 14. Conclusion
Write this after experiments are complete. State the models actually tested, measured best model and its metrics, and what the working app can and cannot do.

## 15. References
Use IEEE style consistently. Include the dataset DOI and official documentation for tools actually used. Example dataset reference:
A. Prasad and S. Chandra, “PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning,” *Computers & Security*, 2024. [Online]. Available: https://doi.org/10.1016/j.cose.2023.103545.
