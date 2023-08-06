import pandas as pd

class Order:
    order_id_list = []

    def __init__(self,order_id,df):
        self.order_id = order_id
        Order.order_id_list.append(order_id)
        self.df = df

    def total_amount(self):
        # This method will calculate total sum of sales amount for given order id
        self.order_df = self.df[self.df['order.order_id'] == self.order_id][['order.order_id','sales_amt','discount','qty','profit_amt']]
        print(self.order_df)
        print("Total amount for given order id is:",self.order_df['sales_amt'].sum())

class OrderChild(Order):
    def __init__(self,order_id,df):
        super().__init__(order_id,df)

    def discounted_sales_amt(self):
        # This method will update the sales amount of each transaction by deducting the discount from it
        self.order_df['sales_amt'] = self.order_df['sales_amt'] - (self.order_df['sales_amt'] * self.order_df['discount'])
        print(self.order_df)
        print("Total amount after applying discount to the order is:",self.order_df['sales_amt'].sum())


def data_cleaning(df):
    ### Data cleaning
    # Check for missing values
    # print(df.isnull().sum())

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

df = df.sort_values('order.order_id')
order1 = OrderChild('CA-2017-100111', df)
order1 = OrderChild('US-2014-106992', df)
print("Class variable order_id_list:", Order.order_id_list)
print("\norder_id:",order1.order_id)
order1.total_amount()
order1.discounted_sales_amt()
