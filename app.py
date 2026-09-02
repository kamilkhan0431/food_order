from email.mime.text import MIMEText
import smtplib
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# --- EMAIL CONFIGURATION ---
SENDER_EMAIL = "klarity0431@gmail.com"
RECEIVER_EMAIL = "klarity0431@gmail.com"
# Replace with your 16-character Google App Password (not your actual Gmail password)
APP_PASSWORD = "keio xfnf pxho ilgx"


def send_order_email(food_name, customer_name, customer_address):
  subject = f"🚨 New Food Order: {food_name}!"
  body = f"""
    You have received a new food order!

    - Food Item: {food_name}
    - Customer Name: {customer_name}
    - Delivery Address: {customer_address}

    Please prepare the order!
    """

  msg = MIMEText(body)
  msg["Subject"] = subject
  msg["From"] = SENDER_EMAIL
  msg["To"] = RECEIVER_EMAIL

  try:
    # Connect to Gmail's SMTP server securely
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(SENDER_EMAIL, APP_PASSWORD)
      server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    print("Email sent successfully!")
  except Exception as e:
    print(f"Error sending email: {e}")


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/order", methods=["POST"])
def place_order():
  data = request.json
  food_name = data.get("food")
  customer_name = data.get("name")
  customer_address = data.get("address")

  # Trigger the email dispatch function
  send_order_email(food_name, customer_name, customer_address)

  return jsonify(
      {"status": "success", "message": "Order placed and email sent!"}
  )


if __name__ == "__main__":
  app.run(debug=True)
