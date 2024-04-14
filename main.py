import pandas as pd
import requests
import os

API_KEY = os.environ.get('API_KEY_CURRENCY')
ENDPOINT = "https://api.fastforex.io/fetch-all"
HEADERS = {"accept": "application/json"}
valid_currencies = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD',
                    'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BZD',
                    'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNH', 'CNY', 'COP', 'CUP', 'CVE', 'CZK', 'DJF',
                    'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GHS',
                    'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS',
                    'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW',
                    'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL',
                    'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN',
                    'NAD', 'NGN', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN',
                    'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP',
                    'SLL', 'SOS', 'SRD', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD',
                    'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VND', 'VUV', 'WST', 'XAF', 'XCD',
                    'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW']
params = {"api_key": API_KEY, "from": ""}

def show_rates(fc, tc, tsc, data):
    # Get row_number of currency user requests
    row_number = data.index.get_loc(data[data['currency'] == tc].index[0])
    currency_rate = data.at[f'row{row_number + 1}', 'rate']
    result = f"From currency: {fc} | Conversion Rate: {currency_rate} | To Currency: {tc}"
    # Check if user chose a second currency to convert to
    if tsc is not None :
        second_row_number = data.index.get_loc(data[data['currency'] == tsc].index[0])
        second_currency_rate = data.at[f'row{second_row_number + 1}', 'rate']
        second_result = f"From currency: {fc} | Conversion rate:{second_currency_rate} | To Currency: {tsc}"
        print(f'{'*' * len(second_result)}\n{second_result}\n{'*' * len(second_result)}')
    else :
        second_currency_rate = None
    print(f"{'*' * len(result)}\n{result}\n{'*' * len(result)}")
    return currency_rate, second_currency_rate

def convert_amount(fc, tc, tsc, first_rate, second_rate):
    try:
        amount = float(input(f"What amount would you like to convert to {tc} and {tsc}?: Input amount in two decimals\n"))
        first_amount_converted = amount * first_rate
        result = f"{amount} {fc} | Conversion rate:{first_rate} | {round(first_amount_converted, 2)} {tc}"
        print(f'{'_' * len(result)}\n{result}\n{'_' * len(result)}')
        # Check if user chose a second currency to convert to
        if tsc is not None:
            second_amount_converted = amount * second_rate
            second_result = f"{amount} {fc} | Conversion rate:{second_rate} | {round(second_amount_converted, 2)} {tsc}"
            print(f'{'_' * len(second_result)}\n{second_result}\n{'_' * len(second_result)}')
        else:
            pass
    except (ValueError, TypeError):
        print('Please enter valid amount in two decimal points.')

def create_dataframe():
    from_currency = input("Which currency would you like to convert from? Type the three letter ISO code: \n")
    to_currency = input("Which currency would you like to convert to? Type the three letter ISO code: \n")
    choice = input('Would you like to add a third currency?: Type y/n \n')
    if choice == 'y':
        to_second_currency = input("Which other currency would you like to convert to? Type the three letter ISO code: \n")
    else:
        to_second_currency = None
    if from_currency in valid_currencies and to_currency in valid_currencies:
        # Check if input is valid ISO currency code
        params['from'] = from_currency
        # Get the conversion rates of all currencies
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        data = response.json()
        # Create list of each rate in loop so it gets cleared each instance
        rates = []
        for key, value in data['results'].items():
            rates.append(value)
        # Create dataframe with currency and rate as column and single currency per row
        data = pd.DataFrame({'currency': [currency for currency in valid_currencies],
                            'rate': [rate for rate in rates]},
                            index=[f'row{i + 1}' for i in range(len(valid_currencies))])
        return from_currency, to_currency, to_second_currency, data

while True:
    try:
        from_currency, to_currency, to_second_currency, data = create_dataframe()
        currency_rate, second_currency_rate = show_rates(fc=from_currency, tc=to_currency, tsc=to_second_currency, data=data)
        convert_amount(fc=from_currency,
                       tc=to_currency,
                       tsc=to_second_currency,
                       first_rate=currency_rate,
                       second_rate=second_currency_rate)
    except TypeError:
        print(f'{'!'*36}\nPlease enter valid ISO currency code\n{'!'*36}')