# House Price Prediction and Real Estate Dashboard

This repository contains code and data for analyzing real estate trends, predicting house prices, estimating time on the market, and building an interactive dashboard for visualization. It is structured to cater to data scientists, real estate analysts, and developers looking to understand property market dynamics.

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [House Price Prediction](#house-price-prediction)
4. [Time on Market Prediction](#time-on-market-prediction)
5. [Real Estate Dashboard](#real-estate-dashboard)
6. [Data Description](#data-description)
7. [How to Run](#how-to-run)
8. [Results and Visualizations](#results-and-visualizations)

## Introduction
Real estate is one of the most dynamic industries influenced by various factors such as location, property features, market trends, and economic conditions. This project aims to predict:
- House prices using machine learning techniques.
- Time a house will remain on the market.

Additionally, an interactive dashboard is built to visualize real estate data trends and predictions.

---

## Project Structure
- **House_price_prediction.ipynb**: Notebook for house price prediction using regression models.
- **Time_on_market_prediction.ipynb**: Notebook to estimate the time a property will stay on the market.
- **House_price_prediction_dash_app.ipynb**: Code to create a Dash app for real estate data visualization.
- **train.csv**: Training dataset containing property details and market data.
- **data_description.txt**: Detailed description of each feature in the dataset.

---

## House Price Prediction
### Overview
The notebook `House_price_prediction.ipynb` uses regression techniques to predict house prices based on various features like location, size, condition, and amenities.

### Steps
1. **Data Preprocessing**:
   - Handle missing values.
   - Encode categorical features.
   - Scale numeric features.

2. **Exploratory Data Analysis (EDA)**:
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns

   sns.scatterplot(data=df, x='GrLivArea', y='SalePrice')
   plt.title('Living Area vs Sale Price')
   plt.show()
   ```

3. **Model Building**:
   - XGBoost, LightGBM, and CatBoost regressors.
   - Combine predictions using an ensemble approach.

4. **Evaluation**:
   - RMSE and R2 scores.

### Key Results
- **XGBoost**: RMSE: 26656.93, R²: 90.74%
- **LightGBM**: RMSE: 28984.71, R²: 89.05%
- **CatBoost**: RMSE: 27045.08, R²: 90.46%

The final predictions are averaged across the three models and saved to `submission.csv`.

---

## Time on Market Prediction
### Overview
`Time_on_market_prediction.ipynb` estimates the number of days a property will stay on the market using features like price, location, and condition.

### Steps
1. **Feature Engineering**:
   - Derive features like price per square foot.
   - Create binary variables for high-demand neighborhoods.

2. **Modeling**:
   - Random Forest Regressor with 500 estimators.

3. **Evaluation**:
   - RMSE and R2 scores.

### Key Results
- **Time on Market Prediction**:
  - RMSE: 8.03
  - R²: 99.94%

The predictions are saved to `time_on_market_submission.csv`.

### Visualizations
```python
plt.hist(df['TimeOnMarket'], bins=30, color='blue')
plt.title('Distribution of Time on Market')
plt.xlabel('Days on Market')
plt.ylabel('Frequency')
plt.show()
```

---

## Real Estate Dashboard
### Overview
The `House_price_prediction_dash_app.ipynb` creates an interactive dashboard using the Dash framework.

### Features
- Interactive visualizations for:
  - Price trends by neighborhood.
  - Correlation between features and price.
  - Renovation trends and quality analysis.
- Geospatial maps for SalePrice distribution.
- Filters to explore specific property types, locations, or price ranges.

### Key Visualizations
1. **SalePrice Over Time (Year vs. Month)**
   A heatmap showing average `SalePrice` distribution by `Year` and `Month`.

2. **Living Area vs SalePrice**
   Interactive scatter plot with a dropdown filter for Neighborhood.

3. **Overall Quality vs SalePrice**
   Boxplot showing the impact of `Overall Quality` on `SalePrice` with a slider for construction year.

4. **Average SalePrice by Neighborhood**
   Horizontal bar chart ranking neighborhoods by average SalePrice.

5. **SalePrice Distribution by Garage Type and Building Type**
   Boxplots categorizing SalePrice based on `GarageType` and `BldgType`.

6. **Price Impact of Renovations**
   Visualizing SalePrice difference for renovated vs. non-renovated properties.

7. **Neighborhood Map**
   Geospatial map displaying SalePrice distribution with latitude and longitude filters.

8. **Correlation Heatmap**
   Heatmap showing feature correlations.

9. **Properties Built Per Year**
   Histogram of property counts by construction year.

10. **Yearly Renovation Trends**
    Bar chart showing the number of renovations across years.

### Code Example
The dashboard is built using Dash and Plotly. Key components include:
```python
@app.callback(
    Output("scatter_plot", "figure"),
    Input("neighborhood_filter", "value")
)
def update_scatter(neighborhoods):
    filtered_data = data if not neighborhoods else data[data['Neighborhood'].isin(neighborhoods)]
    fig = px.scatter(
        filtered_data, x="GrLivArea", y="SalePrice", color="SalePrice",
        color_continuous_scale="Spectral", title="Living Area vs. SalePrice",
        labels={"GrLivArea": "Living Area (sqft)", "SalePrice": "Sale Price"}
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig
```

### How to Run
1. Navigate to the `House_price_prediction_dash_app.ipynb` file.
2. Run the script to start the Dash server:
   ```bash
   python house_price_prediction_dash_app.py
   ```
3. Open the browser at `http://127.0.0.1:8050` to interact with the dashboard.

---

## Data Description
The dataset `train.csv` is accompanied by `data_description.txt`, which provides detailed metadata for each column. Below are some key features:

- **MSSubClass**: Identifies the type of dwelling involved in the sale.
- **MSZoning**: General zoning classification (e.g., Residential, Commercial).
- **LotFrontage**: Linear feet of street connected to the property.
- **GrLivArea**: Above grade (ground) living area square feet.
- **OverallQual**: Rates the overall material and finish of the house.
- **YearBuilt**: Original construction date of the house.
- **YearRemodAdd**: Remodel date (if no remodeling, equals YearBuilt).
- **Neighborhood**: Physical locations within Ames city limits.
- **SalePrice**: Sale price of the property (target variable).

For a complete description, refer to `data_description.txt`.

---

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/real-estate-analysis.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Jupyter notebooks for prediction:
   ```bash
   jupyter notebook
   ```
4. Launch the dashboard:
   ```bash
   python house_price_prediction_dash_app.py
   ```

---

## Results and Visualizations
### Example Plots
- **Correlation Heatmap**:
  ```python
  sns.heatmap(df.corr(), annot=True, fmt='.2f')
  plt.title('Correlation Matrix')
  plt.show()
  ```

- **Feature Importance**:
  ```python
  importances = model.feature_importances_
  plt.barh(df.columns, importances)
  plt.title('Feature Importance')
  plt.show()
  ```

### Dashboard Screenshot
Include a screenshot of the dashboard for reference.

---

## License
This project is licensed under the Apache License. See `LICENSE` for more details.

---

## Contributing
Contributions are welcome. Please create a pull request or open an issue for suggestions and improvements.

