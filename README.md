# 📊 Sales Forecasting & Business Intelligence

An end-to-end Data Science and Business Intelligence project that analyzes historical retail sales data, forecasts future sales using Machine Learning, and presents actionable business insights through an interactive Streamlit dashboard.

## 🎯 Project Overview

The goal of this project is to understand retail sales patterns, identify business trends, and predict future sales using historical transaction data.

The project includes data cleaning, exploratory data analysis (EDA), feature engineering, machine learning, model evaluation, and an interactive dashboard.

## ✨ Key Features

* Data cleaning and preprocessing
* Exploratory Data Analysis (EDA)
* Monthly, daily, country-wise, and product-wise sales analysis
* Sales trend visualization
* Feature engineering for forecasting
* Sales prediction using Random Forest Regressor
* Model evaluation and baseline comparison
* Feature importance analysis
* Interactive Streamlit dashboard
* Actual vs. Predicted sales visualization
* Interactive date-range and country filters

## 🛠️ Technologies Used

* **Programming:** Python
* **Data Analysis:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Machine Learning:** Scikit-learn, Random Forest Regressor
* **Dashboard:** Streamlit
* **Model Saving:** Joblib
* **Environment:** Jupyter Notebook, VS Code

## 📂 Project Structure

```text
Sales-Forecasting-Business-Intelligence/
│
├── data/
│   ├── OnlineRetail.csv
│   ├── OnlineRetail_Cleaned.csv
│   ├── daily_sales.csv
│   ├── monthly_sales.csv
│   ├── forecasting_features.csv
│   └── forecast_results.csv
│
├── notebooks/
│   └── Sales_Forecasting_Analysis.ipynb
│
├── src/
│
├── models/
│   ├── sales_forecasting_model.pkl
│   └── feature_columns.pkl
│
├── dashboard/
│   └── app.py
│
├── images/
│
├── requirements.txt
└── README.md
```

## 📈 Model Performance

The Random Forest Regressor was evaluated using the following metrics:

| Metric       |    Result |
| ------------ | --------: |
| MAE          | 13,919.99 |
| RMSE         | 23,731.37 |
| R² Score     |    0.4029 |
| Baseline MAE | 24,946.26 |

The model reduced MAE by approximately **44.2%** compared with the previous-day baseline.

## 🔍 Feature Importance

The most influential forecasting features include:

1. Sales_Lag_7
2. DayOfWeek
3. Rolling_Mean_7
4. IsWeekend
5. Sales_Lag_1

Sales from seven days earlier was the most important feature in the trained model.

## 📊 Interactive Dashboard

The Streamlit dashboard provides:

* Business overview and KPI metrics
* Sales analytics and visualizations
* Country-wise and product-wise analysis
* Forecast results
* Model performance metrics
* Interactive filters

## 🚀 How to Run the Project

**1. Clone the repository**

```bash
git clone https://github.com/shabeenabano/Sales-Forecasting-Business-Intelligence.git
```

**2. Navigate to the project directory**

```bash
cd Sales-Forecasting-Business-Intelligence
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the Streamlit dashboard**

```bash
python -m streamlit run dashboard/app.py
```

## 📁 Dataset

The project uses the **Online Retail dataset** from the UCI Machine Learning Repository.

The dataset contains retail transaction records used for sales analysis and forecasting.

## 💡 Key Learnings

* Data cleaning and preprocessing
* Exploratory data analysis
* Time-based feature engineering
* Machine learning model development
* Model evaluation and comparison
* Feature importance interpretation
* Interactive dashboard development

## 👩‍💻 Author

**Shabeena Bano**

* GitHub: [@shabeenabano](https://github.com/shabeenabano)
* LinkedIn: [Shabeena Bano](https://www.linkedin.com/in/shabeena-bano-49861542b/)

---

⭐ If you find this project interesting, feel free to explore the repository!
