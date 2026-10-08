from datetime import datetime
import random

CAR_PRICES = {
    "hyundai creta": 1500000,
    "hyundai venue": 1200000,
    "hyundai verna": 1300000,
    "hyundai i20": 900000,
    "hyundai alcazar": 1700000,

    "tata nexon": 1100000,
    "tata punch": 800000,
    "tata harrier": 1800000,
    "tata safari": 2000000,
    "tata altroz": 900000,

    "mahindra thar": 1800000,
    "mahindra xuv700": 2600000,
    "mahindra scorpio": 2000000,
    "mahindra scorpio n": 2200000,
    "mahindra bolero": 1000000,

    "toyota fortuner": 3500000,
    "toyota innova crysta": 2800000,
    "toyota hyryder": 1900000,

    "kia seltos": 1600000,
    "kia sonet": 1000000,
    "kia carens": 1800000,

    "maruti swift": 800000,
    "maruti baleno": 900000,
    "maruti brezza": 1100000,

    "honda city": 1500000
}

# Car name aliases
CAR_ALIASES = {
    "creta": "hyundai creta",
    "venue": "hyundai venue",
    "verna": "hyundai verna",
    "i20": "hyundai i20",
    "alcazar": "hyundai alcazar",

    "nexon": "tata nexon",
    "punch": "tata punch",
    "harrier": "tata harrier",
    "safari": "tata safari",
    "altroz": "tata altroz",

    "thar": "mahindra thar",
    "xuv700": "mahindra xuv700",
    "scorpio": "mahindra scorpio",
    "scorpio n": "mahindra scorpio n",
    "bolero": "mahindra bolero",

    "fortuner": "toyota fortuner",
    "innova crysta": "toyota innova crysta",
    "hyryder": "toyota hyryder",

    "seltos": "kia seltos",
    "sonet": "kia sonet",
    "carens": "kia carens",

    "swift": "maruti swift",
    "baleno": "maruti baleno",
    "brezza": "maruti brezza",

    "city": "honda city"
}


def get_slot_value(slots, slot_name):
    slot = slots.get(slot_name)

    if not slot:
        return ""

    value = slot.get("value")

    if not value:
        return ""

    return (
        value.get("interpretedValue")
        or value.get("originalValue")
        or ""
    )


def format_indian_currency(amount):
    """
    Converts:
    1500000 → ₹15,00,000
    """

    amount = int(amount)

    if amount < 1000:
        return f"₹{amount}"

    amount_string = str(amount)

    last_three = amount_string[-3:]
    remaining = amount_string[:-3]

    if remaining:
        parts = []

        while len(remaining) > 2:
            parts.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        if remaining:
            parts.insert(0, remaining)

        return "₹" + ",".join(parts) + "," + last_three

    return "₹" + last_three


def format_delivery_date(date_value):
    """
    Converts:
    2026-10-20 → 20 October 2026
    """

    try:
        date_object = datetime.strptime(date_value, "%Y-%m-%d")
        return date_object.strftime("%d %B %Y")
    except Exception:
        return date_value


def lambda_handler(event, context):

    print("Received Lex event:")
    print(event)

    session_state = event.get("sessionState", {})
    intent = session_state.get("intent", {})
    slots = intent.get("slots", {})

    customer_name = get_slot_value(slots, "CustomerName")
    email = get_slot_value(slots, "Email")
    contact = get_slot_value(slots, "ContactNumber")
    address = get_slot_value(slots, "Address")

    car_model = get_slot_value(slots, "CarModel")
    car_colour = get_slot_value(slots, "CarColour")
    delivery_date = get_slot_value(slots, "DeliveryDate")

    # Normalize car name
    car_key = car_model.strip().lower()

    if car_key in CAR_ALIASES:
        car_key = CAR_ALIASES[car_key]

    price = CAR_PRICES.get(car_key)

    # If car price is not found
    if price is None:

        message = (
            f"Sorry {customer_name}, I could not find the price "
            f"for {car_model}. Please contact CarKart support."
        )

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent.get(
                        "name",
                        "OrderCarIntent"
                    ),
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": message
                }
            ]
        }

    # Generate Order ID
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)

    order_id = f"CK-{date_part}-{random_part}"

    # Format price and delivery date
    formatted_price = format_indian_currency(price)
    formatted_delivery_date = format_delivery_date(
        delivery_date
    )

    # Display original/full car model
    display_car_model = car_model

    # Final confirmation message
    message = (
        "🎉 CarKart Order Confirmed!\n\n"

        f"Order ID: {order_id}\n\n"

        "Customer Details\n"
        f"Name: {customer_name}\n"
        f"Email: {email}\n"
        f"Contact Number: {contact}\n"
        f"Delivery Address: {address}\n\n"

        "Car Details\n"
        f"Car Model: {display_car_model}\n"
        f"Colour: {car_colour}\n"
        f"Car Price: {formatted_price}\n"
        f"Delivery Date: {formatted_delivery_date}\n\n"

        "Thank you for choosing CarKart! 🚗"
    )

    print("Order successfully processed:")
    print(message)

    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent.get(
                    "name",
                    "OrderCarIntent"
                ),
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }