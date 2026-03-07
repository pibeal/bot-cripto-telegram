import matplotlib.pyplot as plt

def create_chart(data,crypto):

    plt.figure(figsize=(10,5))

    data["Close"].plot()

    plt.title(f"{crypto} price")

    file = f"{crypto}.png"

    plt.savefig(file)

    plt.close()

    return file
