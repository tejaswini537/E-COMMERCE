{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "638e1ec6",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'pandas'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[1], line 1\u001b[0m\n\u001b[1;32m----> 1\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mpandas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mpd\u001b[39;00m\n\u001b[0;32m      2\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mnumpy\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mnp\u001b[39;00m\n\u001b[0;32m      3\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mdatetime\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m datetime, timedelta\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'pandas'"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from datetime import datetime, timedelta\n",
    "import matplotlib.pyplot as plt\n",
    "import math\n",
    "from sklearn.metrics import mean_absolute_error, mean_squared_error, confusion_matrix, ConfusionMatrixDisplay\n",
    "\n",
    "# ============================================\n",
    "# 1. DATA PREPARATION WITH ERROR HANDLING\n",
    "# ============================================\n",
    "\n",
    "def create_sales_data(months=6, products=100, customers=500):\n",
    "    np.random.seed(42)\n",
    "    start_date = datetime.now() - timedelta(days=30*months)\n",
    "    dates = pd.date_range(start_date, periods=30*months, freq='D')\n",
    "\n",
    "    categories = [\"Electronics\", \"Clothing\", \"Home\", \"Beauty\", \"Sports\"]\n",
    "    products = {\n",
    "        f\"SKU-{i:04d}\": {\n",
    "            \"price\": round(np.random.uniform(5, 200), 2),\n",
    "            \"category\": np.random.choice(categories),\n",
    "            \"weight\": np.random.uniform(0.1, 5)\n",
    "        } for i in range(1, products+1)\n",
    "    }\n",
    "\n",
    "    countries = {\n",
    "        \"US\": {\"base_demand\": 1.2, \"weekend_boost\": 1.3},\n",
    "        \"UK\": {\"base_demand\": 1.0, \"weekend_boost\": 1.4},\n",
    "        \"DE\": {\"base_demand\": 0.9, \"weekend_boost\": 1.1},\n",
    "        \"FR\": {\"base_demand\": 0.8, \"weekend_boost\": 1.2},\n",
    "        \"AU\": {\"base_demand\": 0.7, \"weekend_boost\": 1.5}\n",
    "    }\n",
    "\n",
    "    records = []\n",
    "    invoice_id = 500000\n",
    "\n",
    "    for date in dates:\n",
    "        for country, params in countries.items():\n",
    "            transactions = np.random.poisson(params[\"base_demand\"] * 15)\n",
    "            if date.weekday() >= 5:\n",
    "                transactions = int(transactions * params[\"weekend_boost\"])\n",
    "            if date.month == 11:\n",
    "                transactions = int(transactions * 1.8)\n",
    "            elif date.month == 1:\n",
    "                transactions = int(transactions * 0.7)\n",
    "\n",
    "            for _ in range(transactions):\n",
    "                sku = np.random.choice(list(products.keys()))\n",
    "                qty = max(1, int(np.random.exponential(1.5) + 0.5))\n",
    "                records.append({\n",
    "                    \"InvoiceNo\": f\"INV-{invoice_id}\",\n",
    "                    \"StockCode\": sku,\n",
    "                    \"Description\": f\"{products[sku]['category']} - {sku}\",\n",
    "                    \"Quantity\": qty,\n",
    "                    \"InvoiceDate\": date,\n",
    "                    \"UnitPrice\": products[sku][\"price\"],\n",
    "                    \"CustomerID\": np.random.randint(1000, 1000 + customers),\n",
    "                    \"Country\": country,\n",
    "                    \"Category\": products[sku][\"category\"]\n",
    "                })\n",
    "                invoice_id += 1\n",
    "\n",
    "    df = pd.DataFrame(records)\n",
    "    df[\"TotalSales\"] = df[\"Quantity\"] * df[\"UnitPrice\"]\n",
    "    return df\n",
    "\n",
    "# Load or generate data\n",
    "try:\n",
    "    df = pd.read_csv(\"data.csv\", parse_dates=[\"InvoiceDate\"])\n",
    "    print(\"✅ Using uploaded dataset\")\n",
    "    required_cols = [\"InvoiceDate\", \"Quantity\", \"UnitPrice\"]\n",
    "    missing_cols = [col for col in required_cols if col not in df.columns]\n",
    "    if missing_cols:\n",
    "        raise ValueError(f\"Missing required columns: {missing_cols}\")\n",
    "    if \"TotalSales\" not in df.columns:\n",
    "        df[\"TotalSales\"] = df[\"Quantity\"] * df[\"UnitPrice\"]\n",
    "except Exception as e:\n",
    "    print(f\"⚠️ Using synthetic data (Reason: {str(e)})\")\n",
    "    df = create_sales_data(months=6)\n",
    "\n",
    "# ============================================\n",
    "# 2. DATA CLEANING AND FEATURE ENGINEERING\n",
    "# ============================================\n",
    "\n",
    "df = df[(df[\"Quantity\"] > 0) & (df[\"UnitPrice\"] > 0)]\n",
    "df[\"DayOfWeek\"] = df[\"InvoiceDate\"].dt.dayofweek\n",
    "df[\"DayOfMonth\"] = df[\"InvoiceDate\"].dt.day\n",
    "df[\"Month\"] = df[\"InvoiceDate\"].dt.month\n",
    "df[\"WeekOfYear\"] = df[\"InvoiceDate\"].dt.isocalendar().week\n",
    "df[\"Hour\"] = df[\"InvoiceDate\"].dt.hour\n",
    "\n",
    "# ============================================\n",
    "# 3. COMPREHENSIVE VISUALIZATION\n",
    "# ============================================\n",
    "\n",
    "plt.figure(figsize=(18, 12))\n",
    "plt.subplot(2, 2, 1)\n",
    "daily_sales = df.groupby(df[\"InvoiceDate\"].dt.date)[\"TotalSales\"].sum()\n",
    "daily_sales.plot(title=\"Daily Sales Trend\", color=\"navy\")\n",
    "plt.ylabel(\"Sales ($)\")\n",
    "plt.grid(True)\n",
    "\n",
    "plt.subplot(2, 2, 2)\n",
    "if \"Category\" in df.columns:\n",
    "    category_sales = df.groupby(\"Category\")[\"TotalSales\"].sum()\n",
    "    category_sales.plot(kind=\"pie\", autopct=\"%1.1f%%\", startangle=90)\n",
    "    plt.ylabel(\"\")\n",
    "\n",
    "plt.subplot(2, 2, 3)\n",
    "if \"Country\" in df.columns:\n",
    "    country_sales = df.groupby(\"Country\")[\"TotalSales\"].sum().nlargest(10)\n",
    "    country_sales.plot(kind=\"bar\", color=\"green\")\n",
    "    plt.title(\"Sales by Country\")\n",
    "    plt.xticks(rotation=45)\n",
    "\n",
    "plt.subplot(2, 2, 4)\n",
    "hourly_sales = df.groupby(\"Hour\")[\"TotalSales\"].sum()\n",
    "hourly_sales.plot(kind=\"bar\", color=\"purple\")\n",
    "plt.title(\"Sales by Hour of Day\")\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# ============================================\n",
    "# 4. ADVANCED FORECASTING ENGINE\n",
    "# ============================================\n",
    "\n",
    "class SalesForecaster:\n",
    "    def __init__(self, df):\n",
    "        self.df = df\n",
    "        self.prepare_time_series()\n",
    "        \n",
    "    def prepare_time_series(self):\n",
    "        self.daily = self.df.set_index(\"InvoiceDate\")[\"TotalSales\"].resample(\"D\").sum().fillna(0)\n",
    "        self.features = pd.DataFrame(index=self.daily.index)\n",
    "        self.features[\"Sales\"] = self.daily\n",
    "        self.features[\"DayOfWeek\"] = self.features.index.dayofweek\n",
    "        self.features[\"Month\"] = self.features.index.month\n",
    "        self.features[\"IsWeekend\"] = self.features[\"DayOfWeek\"].isin([5,6]).astype(int)\n",
    "        for lag in [1, 7, 14, 21, 28]:\n",
    "            self.features[f\"Lag_{lag}\"] = self.features[\"Sales\"].shift(lag)\n",
    "        self.features[\"Rolling_Mean_7\"] = self.features[\"Sales\"].rolling(7).mean().shift(1)\n",
    "        self.features[\"Rolling_Std_7\"] = self.features[\"Sales\"].rolling(7).std().shift(1)\n",
    "        self.features = self.features.dropna()\n",
    "        \n",
    "    def triple_exponential_smoothing(self, days=14, alpha=0.3, beta=0.2, gamma=0.1):\n",
    "        y = self.daily.values\n",
    "        m = 7\n",
    "        level = y[0]\n",
    "        trend = np.mean(y[1:m+1] - y[0])\n",
    "        seasonals = self._init_seasonality(y, m)\n",
    "        smoothed = []\n",
    "        for i in range(len(y)):\n",
    "            if i >= m:\n",
    "                prev_level, level = level, alpha*(y[i]-seasonals[i%m]) + (1-alpha)*(level+trend)\n",
    "                trend = beta*(level-prev_level) + (1-beta)*trend\n",
    "                seasonals[i%m] = gamma*(y[i]-level) + (1-gamma)*seasonals[i%m]\n",
    "            smoothed.append(level + trend + seasonals[i%m])\n",
    "        forecast = []\n",
    "        for i in range(1, days+1):\n",
    "            idx = (len(y) - m + i) % m\n",
    "            forecast.append(level + i*trend + seasonals[idx])\n",
    "        forecast_dates = pd.date_range(start=self.daily.index[-1] + timedelta(days=1), periods=days)\n",
    "        return forecast_dates, forecast\n",
    "    \n",
    "    def _init_seasonality(self, y, m):\n",
    "        return [np.mean([y[j] - np.mean(y) for j in range(i, len(y), m)]) for i in range(m)]\n",
    "    \n",
    "    def moving_average_forecast(self, days=14):\n",
    "        weights = np.array([0.5, 0.3, 0.2])\n",
    "        last_3_weeks = [self.daily[-7:].mean(), self.daily[-14:-7].mean(), self.daily[-21:-14].mean()]\n",
    "        baseline = np.dot(weights, last_3_weeks)\n",
    "        trend = (last_3_weeks[0] - last_3_weeks[2]) / last_3_weeks[2]\n",
    "        forecast = []\n",
    "        for i in range(1, days+1):\n",
    "            day_of_week = (self.daily.index[-1].dayofweek + i) % 7\n",
    "            seasonal_factor = self.daily.groupby(self.daily.index.dayofweek).mean().iloc[day_of_week] / baseline\n",
    "            forecast.append(baseline * seasonal_factor * (1 + trend) ** (i/7))\n",
    "        forecast_dates = pd.date_range(start=self.daily.index[-1] + timedelta(days=1), periods=days)\n",
    "        return forecast_dates, forecast\n",
    "    \n",
    "    def generate_forecast(self, days=14):\n",
    "        dates_hw, forecast_hw = self.triple_exponential_smoothing(days)\n",
    "        dates_ma, forecast_ma = self.moving_average_forecast(days)\n",
    "        plt.figure(figsize=(15, 6))\n",
    "        plt.plot(self.daily[-60:], label=\"Historical Sales\", color=\"blue\")\n",
    "        plt.plot(dates_hw, forecast_hw, label=\"Holt-Winters Forecast\", color=\"red\", linestyle=\"--\")\n",
    "        plt.plot(dates_ma, forecast_ma, label=\"Moving Average Forecast\", color=\"green\", linestyle=\"--\")\n",
    "        plt.title(f\"{days}-Day Sales Forecast Comparison\")\n",
    "        plt.ylabel(\"Sales ($)\")\n",
    "        plt.legend()\n",
    "        plt.grid(True)\n",
    "        plt.show()\n",
    "        return pd.DataFrame({\n",
    "            \"Date\": dates_hw,\n",
    "            \"HoltWinters\": forecast_hw,\n",
    "            \"MovingAverage\": forecast_ma\n",
    "        }).set_index(\"Date\")\n",
    "\n",
    "# ============================================\n",
    "# 5. EXECUTE FORECASTING\n",
    "# ============================================\n",
    "\n",
    "print(\"\\n🚀 Generating sales forecasts...\")\n",
    "forecaster = SalesForecaster(df)\n",
    "forecast_results = forecaster.generate_forecast(days=14)\n",
    "\n",
    "# ============================================\n",
    "# 6. BUSINESS INSIGHTS REPORT\n",
    "# ============================================\n",
    "\n",
    "print(\"\\n📊 BUSINESS INSIGHTS REPORT\")\n",
    "print(\"=\"*40)\n",
    "daily_sales = df.groupby(df[\"InvoiceDate\"].dt.date)[\"TotalSales\"].sum()\n",
    "print(f\"\\n📈 Sales Performance:\")\n",
    "print(f\"- Total sales period: {daily_sales.index.min()} to {daily_sales.index.max()}\")\n",
    "print(f\"- Highest sales day: {daily_sales.idxmax()} (${daily_sales.max():,.2f})\")\n",
    "print(f\"- Average daily sales: ${daily_sales.mean():,.2f}\")\n",
    "\n",
    "print(f\"\\n🔮 14-Day Forecast:\")\n",
    "print(f\"- Holt-Winters projected total: ${forecast_results['HoltWinters'].sum():,.2f}\")\n",
    "print(f\"- Moving Average projected total: ${forecast_results['MovingAverage'].sum():,.2f}\")\n",
    "\n",
    "if \"Category\" in df.columns:\n",
    "    category_sales = df.groupby(\"Category\")[\"TotalSales\"].sum()\n",
    "    print(f\"\\n📦 Product Categories:\")\n",
    "    print(f\"- Top category: {category_sales.idxmax()} (${category_sales.max():,.2f})\")\n",
    "    print(\"  Category distribution:\")\n",
    "    for cat, sales in category_sales.sort_values(ascending=False).items():\n",
    "        print(f\"  - {cat}: ${sales:,.2f} ({sales/category_sales.sum():.1%})\")\n",
    "\n",
    "if \"Country\" in df.columns:\n",
    "    country_sales = df.groupby(\"Country\")[\"TotalSales\"].sum()\n",
    "    print(f\"\\n🌍 Geographic Performance:\")\n",
    "    print(f\"- Top country: {country_sales.idxmax()} (${country_sales.max():,.2f})\")\n",
    "\n",
    "# ============================================\n",
    "# 7. EVALUATION METRICS\n",
    "# ============================================\n",
    "\n",
    "print(\"\\n📐 FORECAST EVALUATION METRICS\")\n",
    "print(\"=\"*40)\n",
    "cutoff_date = df[\"InvoiceDate\"].max() - timedelta(days=14)\n",
    "train_df = df[df[\"InvoiceDate\"] <= cutoff_date]\n",
    "test_df = df[df[\"InvoiceDate\"] > cutoff_date]\n",
    "\n",
    "forecaster_eval = SalesForecaster(train_df)\n",
    "forecast_eval = forecaster_eval.generate_forecast(days=14)\n",
    "actual_sales = test_df.set_index(\"InvoiceDate\").resample(\"D\")[\"TotalSales\"].sum()\n",
    "\n",
    "forecast_eval = forecast_eval[forecast_eval.index.isin(actual_sales.index)]\n",
    "actual_sales = actual_sales[actual_sales.index.isin(forecast_eval.index)]\n",
    "\n",
    "def regression_metrics(y_true, y_pred, model_name):\n",
    "    mae = mean_absolute_error(y_true, y_pred)\n",
    "    rmse = mean_squared_error(y_true, y_pred) ** 0.5\n",
    "    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100\n",
    "    print(f\"\\n📏 {model_name} Forecast Accuracy:\")\n",
    "    print(f\"- MAE:  {mae:,.2f}\")\n",
    "    print(f\"- RMSE: {rmse:,.2f}\")\n",
    "    print(f\"- MAPE: {mape:,.2f}%\")\n",
    "\n",
    "regression_metrics(actual_sales, forecast_eval[\"HoltWinters\"], \"Holt-Winters\")\n",
    "regression_metrics(actual_sales, forecast_eval[\"MovingAverage\"], \"Moving Average\")\n",
    "\n",
    "# ============================================\n",
    "# 8. OPTIONAL CONFUSION MATRIX (Categorized)\n",
    "# ============================================\n",
    "\n",
    "def categorize(sales):\n",
    "    if sales < 500:\n",
    "        return \"Low\"\n",
    "    elif sales < 1500:\n",
    "        return \"Medium\"\n",
    "    else:\n",
    "        return \"High\"\n",
    "\n",
    "y_true_cat = actual_sales.apply(categorize)\n",
    "y_pred_cat = forecast_eval[\"HoltWinters\"].apply(categorize)\n",
    "\n",
    "cm = confusion_matrix(y_true_cat, y_pred_cat, labels=[\"Low\", \"Medium\", \"High\"])\n",
    "disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[\"Low\", \"Medium\", \"High\"])\n",
    "disp.plot(cmap=\"Blues\")\n",
    "plt.title(\"Confusion Matrix (Holt-Winters Categories)\")\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "65f32961",
   "metadata": {},
   "outputs": [
    {
     "ename": "",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31mRunning cells with 'Python 3.10.0' requires the ipykernel package.\n",
      "\u001b[1;31m<a href='command:jupyter.createPythonEnvAndSelectController'>Create a Python Environment</a> with the required packages.\n",
      "\u001b[1;31mOr install 'ipykernel' using the command: 'c:/Users/VAIBHAV/AppData/Local/Programs/Python/Python310/python.exe -m pip install ipykernel -U --user --force-reinstall'"
     ]
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "29e717bb",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
