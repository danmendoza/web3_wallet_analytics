import sys
import os
sys.path.append(os.path.abspath('C:/Users/danie/Documents/Repos/general/web3_wallet_analytics/'))

from PyQt5 import QtCore, QtWidgets, uic
from lib.balances import get_balances_and_prices





class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Load the main UI file (dashboard.ui)
        uic.loadUi(r"C:\Users\danie\Documents\Repos\general\web3_wallet_analytics\ui\dashboard.ui", self)
        
        # Fetch and display token balance data
        self.update_token_balance_data()

    def update_token_balance_data(self):
        # Example of token data (Replace this with your actual data-fetching logic)
        token_data = [
            {"id": 1, "token": "BTC", "usdt": "0.5"},
            {"id": 2, "token": "ETH", "usdt": "2.1"},
            {"id": 3, "token": "USDT", "usdt": "5000"}
        ]
        token_data = self.get_token_data()
        # Find the vertical layout where token items will go (VLayoutTokens)
        v_layout = self.findChild(QtWidgets.QVBoxLayout, "VLayoutTokens")

        # Loop through the token data and dynamically create widgets for each token entry
        for token in token_data:
            # Create a widget for each token item using the token UI (dashbd_item.ui)
            token_widget = self.create_token_widget(token)
            
            # Add the token widget to the vertical layout
            v_layout.addWidget(token_widget)

    def create_token_widget(self, token):
        # Load the UI for individual token items (dashbd_item.ui)
        token_widget = QtWidgets.QWidget()
        uic.loadUi(r"C:\Users\danie\Documents\Repos\general\web3_wallet_analytics\ui\dashbd_item.ui", token_widget)
        
        # Set the data for this particular token (id, token, and balance)
        label_id = token_widget.findChild(QtWidgets.QLabel, "label_id")
        label_amount = token_widget.findChild(QtWidgets.QLabel, "label_amount")
        label_balance = token_widget.findChild(QtWidgets.QLabel, "label_balance")
        label_price = token_widget.findChild(QtWidgets.QLabel, "label_price")
        
        # Set text based on token data
        label_id.setText(f"{token['id']}")
        label_amount.setText(f"{round(token['balance'], 5)}")
        label_balance.setText(f"{round(token['usdt'], 5)}$")
        label_price.setText(f"{round(token['price'], 5)}$")

        return token_widget 

    def get_token_data(self):
        balances = get_balances_and_prices()
        balances = [{"id": symbol, "balance": data.get('balance'), "usdt": data.get('value_in_usdt'), "price": data.get('price')} for symbol, data in balances.items()]
        return balances
    

# Create the application and the window
app = QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()

sys.exit(app.exec_())
