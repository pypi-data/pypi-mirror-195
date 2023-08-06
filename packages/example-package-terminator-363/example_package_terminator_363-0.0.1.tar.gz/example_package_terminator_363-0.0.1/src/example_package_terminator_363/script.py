import requests
import pandas as pd
import argparse
import numpy as np

list_to_convert_to_df=[]
cnt=1
offset=1
while(cnt<6):
    parser=argparse.ArgumentParser()
    parser.add_argument('-t', type=str, help ='Enter access token:', required=True)
    args=parser.parse_args()
    response=requests.get(f'https://globalmart-api.onrender.com/mentorskool/v1/sales/?offset={offset}&limit=100', headers={'access_token': args.t}).json()
    list_to_convert_to_df.append(response['data'])
    cnt+=1
    offset+=100

def convert_json_to_df(list_to_convert_to_df):
    frames=[]
    for lst in list_to_convert_to_df:
        df=pd.json_normalize(lst)
        frames.append(df)    
    return pd.concat(frames)
df=convert_json_to_df(list_to_convert_to_df)
'''GlobalMart wants us to find the average purchase frequency in a particular state.'''
class PurchaseFrequency:
    def __init__(self, df, state):
        self.df=df
        self.state=state
    def avg_purchase_frequency(self):
        df['order.order_purchase_date'] = pd.to_datetime(df['order.order_purchase_date'], format='%Y-%m-%d %H:%M:%S')
        result=df.loc[df['order.customer.address.state']==self.state]
        return ((result['order.order_purchase_date'].max()-result['order.order_purchase_date'].min())/np.timedelta64(1, 'D'))/result['order.order_id'].nunique()

'''create a class called Orders that calculates the total amount of an order. create a method called calculate_total() that
takes all the transactions of a particular order, calculates the total amount of that order, and returns the final amount for
that order.'''
class Orders:
    OrderID=''
    def __init__(self, order_id, df):
        self.order_id=order_id
        self.df=df
        Orders.OrderID=order_id
    def calculate_total(self):
        result=df.loc[df['order.order_id']==self.order_id]
        return result.groupby('order.order_id')['sales_amt'].sum()
    @classmethod
    def get_OrderID(cls):
        return cls.OrderID

'''In the recent sales report of GlobalMart, the manager noticed that there were some orders that had multiple transactions. 
Now, the manager wants to know the total sales amount of the order with ID "US-2014-106992". Can you please calculate the total
amount for this order using the Orders class?'''
order=Orders('US-2014-106992', df)
order.calculate_total()

'''GlobalMart wants us to modify our code to determine the final sales amount following the deduction of the discount. Ex:- If 
the discount is 20% on an iPhone of 30,000 then the final amount for the iPhone will be 24,000. Thus, we need to make some 
changes to the code.'''
class ExtendedOrders(Orders):
    def __init__(self, order_id, df):
        Orders.__init__(self, order_id, df)
    def calculate_final_amt(self):
        df['sales_after_discount']=df.apply(lambda x: x['sales_amt']-((x['sales_amt']*(x['discount']*100))/100), axis=1)
        result=df.loc[df['order.order_id']==self.order_id]
        return result.groupby('order.order_id')['sales_after_discount'].sum()
    
'''Once again, GlobalMart wants to know the final sales amount of a particular order. This time, the order_id in question is
"CA-2017-100111". They want to determine the actual amount of revenue generated from this particular order after applying any
discounts or promotions. Can you help them calculate the final sales amount for this order?'''
eo=ExtendedOrders('CA-2017-100111', df)
eo.calculate_final_amt()

'''Ram is confused on how to access the class variables and methods? Can you help Ram by selecting the correct options?'''
order=Orders('CA-2017-100111', df)
Orders.get_OrderID()
order.get_OrderID()