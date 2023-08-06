import pandas as pd

def avg_purchase_frequency_by_state(df, state):
    '''
    It will return the average purchase frequency of the particular state, which received as input.

    Params: 
    df(DataFrame) : Pandas dataframe of the data returned by GlobalMart API
    state(string) : The state for which we want average purchase freq.

    Returns:
    float : The average purchase frequncy of given state 
    '''
    df = df[df['order.customer.address.state'] == state]
    df = df[['order.customer.address.state','order.order_purchase_date']].sort_values('order.order_purchase_date')
    df['next_order_purchase_date'] = df['order.order_purchase_date'].shift(-1)
    df['Purchase_frequency'] = (df['next_order_purchase_date']- df['order.order_purchase_date']).apply(lambda x:x.days)
    # print(df)
    return  df['Purchase_frequency'].mean() 

def data_cleaning(df):
    ### Data cleaning
    # Check for missing values
    print(df.isnull().sum())

    # Check for duplicate records
    print("duplicated records are:",df.duplicated().sum())
    # Drop duplicate records
    df.drop_duplicates(inplace=True)

    # Check for datatype corrections
    df['order.order_purchase_date'] = pd.to_datetime(df['order.order_purchase_date'])
    df['order.order_delivered_carrier_date'] = pd.to_datetime(df['order.order_delivered_carrier_date'])
    df['order.order_delivered_customer_date'] = pd.to_datetime(df['order.order_delivered_customer_date'])
    df['order.order_estimated_delivery_date'] = pd.to_datetime(df['order.order_estimated_delivery_date'])

    # Removing leading or trailing space 
    df['order.customer.address.state'] = df['order.customer.address.state'].str.strip()

    return df

df = pd.read_csv(r'C:\Users\Krishna.Savaliya\Krishna_Savaliya_globalmart_processing\GlobalMartData.csv')
df = data_cleaning(df)

avg_freq = avg_purchase_frequency_by_state(df, 'new york')
# avg_freq = avg_purchase_frequency_by_state(df, 'calfornia')
print(avg_freq)


# which state do the users purchase the products most frequently
freq_all_states = [avg_purchase_frequency_by_state(df, states) for states in df['order.customer.address.state']]
max_freq_state = df.loc[freq_all_states.index(max(freq_all_states)), 'order.customer.address.state']
print("state with max product purchase frequency:",max_freq_state)