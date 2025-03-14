import sys
import os
sys.path.append(os.path.abspath('C:/Users/danie/Documents/Repos/general/web3_wallet_analytics/'))
import pandas as pd
from lib.balances import get_data
from data.local_paths import csv_data_path
def generate_csv(token_name, days=30):

    file_name = os.path.join(csv_data_path, "{}_balance_last_{}_days.csv".format(token_name, days))
    if os.path.exists(file_name):
        print("El archivo ya existe.")
        return False

    data = get_data(token_name)
    # Crear un DataFrame con los resultados
    df = pd.DataFrame(data)
    print(df)

    # Guardar en un archivo CSV (opcional)
    df.to_csv(file_name.format(token_name), index=False)

    return True