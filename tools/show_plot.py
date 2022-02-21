import json
import sys
import base64
import pickle

import matplotlib.pyplot as plt


def pickle_deserialize(serialized_obj: str):
    return pickle.loads(base64.b64decode(serialized_obj.encode("utf-8")))


if __name__ == "__main__":
    models_filepath = sys.argv[1]

    with open(models_filepath, "r", encoding="utf-8") as models_file:
        models_data = json.loads(models_file.read())

    fig = None
    try:
        fig = pickle_deserialize(models_data["model_data"]["out"]["validate_plot"])
        print("Deserialization succesful. Plotting figure.")
        plt.show()
    except:
        print(
            "Failed to deserialize plot. Make sure it has been serialized identicallt"
        )
        exit(1)
