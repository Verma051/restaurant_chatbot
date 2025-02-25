from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Sample restaurant menu
menu = {
    "Pizza": 300,
    "Burger": 150,
    "Pasta": 200,
    "Coke": 50,
    "Ice Cream": 100
}

# Load orders from a file
def load_orders():
    if os.path.exists('order_data.json'):
        with open('order_data.json', 'r') as f:
            return json.load(f)
    return {}

# Save orders to a file
def save_orders(orders):
    with open('order_data.json', 'w') as f:
        json.dump(orders, f)

# Store customer orders
orders = load_orders()
order_id_counter = max(orders.keys(), default=1)

# Serve the HTML page when the user accesses the home route "/"
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global order_id_counter

    user_input = request.json['message'].lower()
    response = ""

    # Respond to user input
    if "new order" in user_input:
        response = "Welcome! Here's our menu:\n"
        for item, price in menu.items():
            response += f"{item}: ₹{price}\n"
        response += "\nWhat would you like to order? Please type: 'Pizza 2' for 2 Pizzas."

    elif any(item.lower() in user_input for item in menu):
        # Extract item and quantity from user input
        user_order = user_input.split()
        item = user_order[0].capitalize()
        quantity = int(user_order[1])

        # Calculate total bill
        total = menu[item] * quantity
        order_id = order_id_counter
        orders[order_id] = (item, quantity, total)
        save_orders(orders)
        response = f"Your order for {quantity} {item}(s) is placed. Your total is ₹{total}. Your Order ID is {order_id}."
        order_id_counter += 1

    elif "track" in user_input:
        try:
            # Extract order ID from input
            order_id = int(user_input.split()[-1])
            if order_id in orders:
                response = f"Order ID {order_id} is being prepared."
            else:
                response = "Sorry, I couldn't find your order."
        except:
            response = "Please provide a valid Order ID."

    else:
        response = "I'm sorry, I didn't understand. You can say 'new order' to start ordering."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
