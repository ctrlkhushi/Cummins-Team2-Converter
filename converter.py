import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from forex_python.converter import CurrencyRates
import pandas as pd
import plotly.express as px

# Dictionary mapping currency codes to country names
currency_country_mapping = {
    "DZD": "Algerian dinar",
    "AUD": "Australian dollar",
    "BHD": "Bahrain dinar",
    "VEF": "Bolivar Fuerte",
    "BWP": "Botswana pula",
    "BRL": "Brazilian real",
    "BND": "Brunei dollar",
    "CAD": "Canadian dollar",
    "CLP": "Chilean peso",
    "CNY": "Chinese yuan",
    "COP": "Colombian peso",
    "CZK": "Czech koruna",
    "DKK": "Danish krone",
    "EUR": "Euro",
    "HUF": "Hungarian forint",
    "ISK": "Icelandic krona",
    "INR": "Indian rupee",
    "IDR": "Indonesian rupiah",
    "IRR": "Iranian rial",
    "ILS": "Israeli New Shekel",
    "JPY": "Japanese yen",
    "KZT": "Kazakhstani tenge",
    "KRW": "Korean won",
    "KWD": "Kuwaiti dinar",
    "LYD": "Libyan dinar",
    "MYR": "Malaysian ringgit",
    "MUR": "Mauritian rupee",
    "MXN": "Mexican peso",
    "NPR": "Nepalese rupee",
    "NZD": "New Zealand dollar",
    "NOK": "Norwegian krone",
    "OMR": "Omani rial",
    "PKR": "Pakistani rupee",
    "PEN": "Peruvian sol",
    "PHP": "Philippine peso",
    "PLN": "Polish zloty",
    "QAR": "Qatari riyal",
    "RUB": "Russian ruble",
    "SAR": "Saudi Arabian riyal",
    "SGD": "Singapore dollar",
    "ZAR": "South African rand",
    "LKR": "Sri Lankan rupee",
    "SEK": "Swedish krona",
    "CHF": "Swiss franc",
    "THB": "Thai baht",
    "TTD": "Trinidadian dollar",
    "TND": "Tunisian dinar",
    "AED": "U.A.E. dirham",
    "GBP": "U.K. pound",
    "USD": "U.S. dollar",
    "UYU": "Uruguayan peso",
}

# List of available currencies
all_currencies = list(currency_country_mapping.keys())

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1("Currency Exchange Rate Dashboard"),
        html.Label("Select Base Currency:"),
        dcc.Dropdown(
            id="base-currency",
            options=[
                {"label": f"{currency_country_mapping[currency]} ({currency})", "value": currency}
                for currency in all_currencies
            ],
            value="USD",
        ),
        html.Label("Select Target Currency:"),
        dcc.Dropdown(
            id="target-currency",
            options=[
                {"label": f"{currency_country_mapping[currency]} ({currency})", "value": currency}
                for currency in all_currencies
            ],
            value="EUR",
        ),
        html.Div(id="exchange-rate-output"),

        dcc.Graph(id='exchange-rate-chart'),  # Adding the graph component
    ]
)

# Define callback to update exchange rate and graph on user input
@app.callback(
    [Output("exchange-rate-output", "children"),
     Output('exchange-rate-chart', 'figure')],
    [Input("base-currency", "value"), Input("target-currency", "value")],
)
def update_exchange_rate_and_graph(base_currency, target_currency):
    # Fetch exchange rate
    c = CurrencyRates()
    rate = c.get_rate(base_currency, target_currency)
    
    # Generate sample data for plotting (replace this with your logic to get actual data)
    # Here's an example using random data for illustration
    data = {
        "Date": pd.date_range(start='2023-01-01', periods=10),
        "Rate": [rate * (1 + i * 0.05) for i in range(10)]  # Example random rates
    }
    df = pd.DataFrame(data)

    # Create the line chart
    fig = px.line(df, x="Date", y="Rate", title=f"{base_currency}-{target_currency} Exchange Rate Over Time")
    
    # Display the exchange rate
    exchange_rate_info = f"Exchange Rate: 1 {base_currency} ({currency_country_mapping[base_currency]}) = {rate:.2f} {target_currency} ({currency_country_mapping[target_currency]})"
    
    return exchange_rate_info, fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
