class Order:
    def __init__(self, order_id, customer_name, product_name, quantity, price):
        self.order_id = order_id
        self.customer_name = customer_name
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    def SayHello(self):
        print('Hello, there !!!')

    def total_cost(self):
        return self.quantity * self.price

    def display_order(self):
        print(f"Order ID: {self.order_id}")
        print(f"Customer Name: {self.customer_name}")
        print(f"Product Name: {self.product_name}")
        print(f"Quantity: {self.quantity}")
        print(f"Price per unit: {self.price}")
        print(f"Total Cost: {self.total_cost()}")

# Example usage
# ord = Order(1, "John", "Shoes", 2, 50.0)
# ord.SayHello()
# ord.display_order()
