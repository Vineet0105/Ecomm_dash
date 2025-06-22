import pandas as pd
from .models import *

def read_file(path):
    try:
        df = pd.read_excel(path)
    except:
        df = pd.read_csv(path)

    for i in df.index:
        data = df.iloc[i]


        cust,_ = Customer.objects.get_or_create(
        customer_id = data['customer_id'],
        customer_name = data['customer_name'],
        contact_email = data['contact_email'],
        phone_number = data['phone_number'],
         )

        product_category,_ = Category.objects.get_or_create(name=data['category'])
        plat,_ = Platform.objects.get_or_create(platform_name=data['platform'])

        prod,_ = Product.objects.get_or_create(
        product_id = data['product_id'],
        product_name = data['product_name'],
        product_category = product_category,
        )



        Order.objects.create(
        order_id = data['order_id'],
        order_product = prod,
        order_customer = cust,
        order_platform = plat,
        quantity_sold = data['quantity_sold'],
        selling_price = data['selling_price'],
        sale_date = data['sale_date'],
        total_sale_value = data['total_sale_value'],
        delviery_address = data['delviery_address'],
        delivery_status = data['delivery_status']
        )