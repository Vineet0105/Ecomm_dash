import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecomm_dash.settings')
django.setup()

from dashboard.models import *
 

qs = Order.objects.values(
    "order_id",
    "quantity_sold",
    "selling_price",
    "sale_date",
    "total_sale_value",
    "delviery_address",
    "delivery_status",
    "order_product__product_id",
    "order_product__product_name",
    "order_product__product_category__name",
    "order_customer__customer_id",
    "order_customer__customer_name",
    "order_customer__contact_email",
    "order_customer__phone_number",
    "order_platform__platform_name"
)
		
import pandas as pd
df = pd.DataFrame(qs)

df.rename(
    columns={
        "order_product__product_id": "product_id",
        "order_product__product_name": "product_name",
        "order_product__product_category__name": "category",
        "order_customer__customer_id": "customer_id",
        "order_customer__customer_name": "customer_name",
        "order_customer__contact_email": "contact_email",
        "order_customer__phone_number": "phone_number",
        "order_platform__platform_name": "platform",
    }, inplace=True
)
df.to_excel(r"C:\Users\Vineet\Downloads\ecommerce_sales.xlsx",index=False)
