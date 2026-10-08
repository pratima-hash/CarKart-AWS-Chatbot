\# 🚗 CarKart - AWS Car Ordering Chatbot



CarKart is a \*\*cloud-based car ordering chatbot\*\* developed using \*\*Amazon Lex V2, AWS Lambda, Python, and Boto3\*\*.



The chatbot allows users to interact using natural language and place a car order by providing their personal details, selecting a car model and colour, choosing a delivery date, and confirming the order.



After confirmation, AWS Lambda processes the order and generates a unique order ID along with the car price and complete order summary.



\---



\## 📌 Project Overview



The main objective of this project is to build a simple conversational application using AWS serverless technologies.



The chatbot collects:



\- Customer Name

\- Email Address

\- Contact Number

\- Delivery Address

\- Car Model

\- Car Colour

\- Delivery Date



After collecting the required information, the chatbot asks the user to confirm the order.



If the user confirms the order, AWS Lambda processes the request and generates:



\- Unique Order ID

\- Customer Details

\- Selected Car Model

\- Car Colour

\- Car Price

\- Delivery Date

\- Order Confirmation Message



\---



\## ☁️ AWS Architecture



The project uses the following architecture:



```text

&#x20;                   👤 User

&#x20;                      |

&#x20;                      ↓

&#x20;               Amazon Lex V2

&#x20;                      |

&#x20;                      | OrderCarIntent

&#x20;                      ↓

&#x20;              AWS Lambda Function

&#x20;             CarKartOrderProcessor

&#x20;                      |

&#x20;            ┌─────────┴─────────┐

&#x20;            ↓                   ↓

&#x20;      Car Price Lookup     Order ID Generation

&#x20;            |                   |

&#x20;            └─────────┬─────────┘

&#x20;                      ↓

&#x20;               Order Summary

&#x20;                      |

&#x20;                      ↓

&#x20;                 👤 User

