import io
import requests
import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv("../data/iris.csv")
    
    features = ["sepal length", "petal width"]
    response = "species"
    new_df = pd.get_dummies(df[features + [response]])

    csv_string = io.StringIO() 
    new_df.to_csv(csv_string)

    request_payload = {
        "features": features,
        "target": response,
        "epochs": 100,
        "learning_rate": 0.01,
        "hidden_size": 8,
        "activation": "tanh",
        "csv_data": csv_string.getvalue(),
    }


    response = requests.post(
        "http://127.0.0.1:3000/neural-network",
        json=request_payload,
    )

    print(response.text)
