import requests
import random
from bs4 import BeautifulSoup as bs


session = requests.session()

def get_sizes_in_stock():
    global session
    #input the link of the item you want to checkout on "endpoint"
    endpoint = "http://www.jimmyjazz.com/mens/footwear/jordan-air-jordan-retro-12/130690-617?color=Burgundy"
    response = session.get(endpoint)

    soup = bs(response.text, "html.parser")

    div = soup.find("div", ["class", "box_wrapper"])
    all_sizes = div.findAll('a')

    sizes_in_stock = []
    for size in all_sizes:
        if "piunavailable" not in size("class"):
            size_id = size["id"]
            sizes_in_stock.append(size_id.split("_")[1])
    return sizes_in_stock

def add_to_cart():
    global session
    sizes_in_stock = get_sizes_in_stock()
    size_chosen = random.choice(sizes_in_stock)

    endpoint = "http://www.jimmyjazz.com/cart-request/cart/add/%s/1"%(size_chosen)
    response = session.get(endpoint)

    return '"success":1' in response.text

def checkout():
    global session
    endpoint0 = "https://www.jimmyjazz.com/cart/checkout"
    response0 = session.get(endpoint0)

    soup = bs(response0.text, "html.parser")
    inputs = soup.find_all("input", {"name": "form_build_id"})

    form_build_id = inputs[1]["value"]

    #You have to manually input your checkout information
    endpoint1 = "https://www.jimmyjazz.com/cart/checkout"
    payload1 = {
        "billing_email":"yahee@yahoo.com",
        "billing_email_confirm":"yahee@yahoo.com",
        "billing_phone":"231-125-2345",
        "email_opt_in":"1",
        "shipping_first_name":"Test",
        "shipping_last_name":"Test",
        "shipping_address1":"3245 12st",
        "shipping_address2":"",
        "shipping_city":"Test Cirt",
        "shipping_state":"Test State",
        "shipping_zip":"100000",
        "shipping_method":"1",
        "billing_same_as_shipping":"1",
        "billing_first_name":"",
        "billing_last_name":"",
        "billing_country":"US",
        "billing_address1":"",
        "billing_address2":"",
        "billing_city":"",
        "billing_state":"",
        "billing_zip":"",
        "cc_type":"Visa",#(or Master, American Express, etc)
        "cc_number":"1234123412341234",
        "cc_exp_month":"12",
        "cc_exp_year":"12",
        "cc_cvv":"121",
        "gc_num":"",
        "form_build_id":form_build_id,
        "form_id":"cart_checkout_form"
    }
    response1 = session.post(endpoint1, data = payload1)

    soup = bs(response1.text, "html.parser")
    inputs = soup.find_all("input", {"name" : "form_build_id"})
    form_build_id2 = inputs[1]["value"]
    print (form_build_id2)

    endpoint2 = "https://www.jimmyjazz.com/cart/confirm"
    payload2 = {
        "form_build_id":form_build_id2,
        "form_id":"cart_confirm_form"
    }
    response2 = session.post(endpoint2, data=payload2)

add_to_cart()
checkout()
