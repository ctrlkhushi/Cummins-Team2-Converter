!pip install pandas plotly dash

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from google.colab import files

# Upload CSV files manually
uploaded_files = files.upload()

# List of uploaded file names
uploaded_file_names = list(uploaded_files.keys())

# Create an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Loop through each uploaded file and append its data to the combined DataFrame
for file_name in uploaded_file_names:
    data = pd.read_csv(file_name)
    combined_data = combined_data.append(data, ignore_index=True)

# Identify the columns dynamically based on the first row of the DataFrame
date_column = combined_data.columns[0]  # Assuming the date is the first column

# Check if 'TargetCurrency' column exists in the DataFrame
if 'TargetCurrency' in combined_data.columns:
    target_currency_column = 'TargetCurrency'
else:
    # If 'TargetCurrency' column does not exist, use a default value or adjust accordingly
    target_currency_column = combined_data.columns[1]  # Change this to your default value or adjust as needed

# Convert 'Date' column to datetime
combined_data[date_column] = pd.to_datetime(combined_data[date_column])

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Currency Exchange Rate Analysis Dashboard"),
    
    dcc.Dropdown(
        id='currency-pair-dropdown',
        options=[
            {'label': pair, 'value': pair} for pair in combined_data[target_currency_column].unique()
        ],
        value=combined_data[target_currency_column].unique()[0],
        multi=False,
        style={'width': '50%'}
    ),

    dcc.RadioItems(
        id='time-interval-radio',
        options=[
            {'label': 'Weekly', 'value': 'W'},
            {'label': 'Monthly', 'value': 'M'},
            {'label': 'Quarterly', 'value': 'Q'},
            {'label': 'Yearly', 'value': 'Y'}
        ],
        value='W',
        labelStyle={'display': 'block'}
    ),

    dcc.Graph(id='exchange-rate-chart'),

    html.Div(id='peak-low-info')
])

# Define callback to update the chart based on user input
@app.callback(
    [Output('exchange-rate-chart', 'figure'),
     Output('peak-low-info', 'children')],
    [Input('currency-pair-dropdown', 'value'),
     Input('time-interval-radio', 'value')]
)
def update_chart(target_currency, time_interval):
    # Filter data based on user selection
    filtered_df = combined_data[combined_data[target_currency_column] == target_currency]

    # Resample data based on the selected time interval
    resampled_df = filtered_df.set_index(date_column).resample(time_interval).mean().reset_index()

    # Find peak and low dates
    peak_date = resampled_df.loc[resampled_df[exchange_rate_column].idxmax()][date_column]
    low_date = resampled_df.loc[resampled_df[exchange_rate_column].idxmin()][date_column]

    # Create the chart
    fig = px.line(resampled_df, x=date_column, y=exchange_rate_column,
                  title=f'{target_currency} Exchange Rate Over Time')

    # Add annotations for peak and low dates
    fig.add_annotation(x=peak_date, y=resampled_df[exchange_rate_column].max(),
                       text=f'Peak: {peak_date.strftime("%Y-%m-%d")}', showarrow=True)
    fig.add_annotation(x=low_date, y=resampled_df[exchange_rate_column].min(),
                       text=f'Low: {low_date.strftime("%Y-%m-%d")}', showarrow=True)

    return fig, f'Highest rate on {peak_date.strftime("%Y-%m-%d")}, Lowest rate on {low_date.strftime("%Y-%m-%d")}'

# Run the app
if __name__ == '__main__':
    app.run_server(mode='inline')
