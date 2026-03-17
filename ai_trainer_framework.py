from abc import ABC, abstractmethod

# -----------------------------
# ModelConfig (Composition + Instance Attributes + Magic Method)
# -----------------------------
class ModelConfig:
    def __init__(self, model_name, learning_rate=0.01, epochs=10):
        # Instance Attributes
        self.model_name = model_name
        self.learning_rate = learning_rate
        self.epochs = epochs

    def __repr__(self):  # Magic Method
        return f"[Config] {self.model_name} | lr={self.learning_rate} | epochs={self.epochs}"


# -----------------------------
# BaseModel (Abstraction + Class Attribute + Composition)
# -----------------------------
class BaseModel(ABC):
    model_count = 0  # Class Attribute

    def __init__(self, config: ModelConfig):
        self.config = config  # Composition (Model HAS-A config)
        BaseModel.model_count += 1

    @abstractmethod  # Abstraction
    def train(self, data):
        pass

    @abstractmethod  # Abstraction
    def evaluate(self, data):
        pass


# -----------------------------
# LinearRegressionModel (Inheritance + Method Overriding + super())
# -----------------------------
class LinearRegressionModel(BaseModel):

    def __init__(self, learning_rate=0.01, epochs=10):
        config = ModelConfig("LinearRegression", learning_rate, epochs)
        super().__init__(config)  # super()

    def train(self, data):  # Method Overriding
        print(f"{self.config.model_name}: Training on {len(data)} samples "
              f"for {self.config.epochs} epochs (lr={self.config.learning_rate})")

    def evaluate(self, data):  # Method Overriding
        print(f"{self.config.model_name}: Evaluation MSE = 0.042")


# -----------------------------
# NeuralNetworkModel (Inheritance + Extra Attribute + Overriding)
# -----------------------------
class NeuralNetworkModel(BaseModel):

    def __init__(self, learning_rate=0.001, epochs=20, layers=None):
        config = ModelConfig("NeuralNetwork", learning_rate, epochs)
        super().__init__(config)
        self.layers = layers if layers else [64, 32, 1]  # Instance Attribute

    def train(self, data):  # Method Overriding
        print(f"{self.config.model_name} {self.layers}: Training on {len(data)} samples "
              f"for {self.config.epochs} epochs (lr={self.config.learning_rate})")

    def evaluate(self, data):  # Method Overriding
        print(f"{self.config.model_name}: Evaluation Accuracy = 91.5%")


# -----------------------------
# DataLoader (Aggregation)
# -----------------------------
class DataLoader:
    def __init__(self, data):
        self.data = data  # Instance Attribute

    def get_data(self):  # Instance Method
        return self.data


# -----------------------------
# Trainer (Aggregation + Polymorphism)
# -----------------------------
class Trainer:
    def __init__(self, model: BaseModel, dataloader: DataLoader):
        self.model = model       # Aggregation (uses model)
        self.dataloader = dataloader  # Aggregation (uses loader)

    def run(self):  # Instance Method
        data = self.dataloader.get_data()

        print(f"\n--- Training {self.model.config.model_name} ---")

        # Polymorphism (same method works for different models)
        self.model.train(data)
        self.model.evaluate(data)


# -----------------------------
# Main Program
# -----------------------------
if __name__ == "__main__":

    # Data
    data = [1, 2, 3, 4, 5]
    loader = DataLoader(data)

    # Create Models
    model1 = LinearRegressionModel()
    model2 = NeuralNetworkModel()

    # Print Configs
    print(model1.config)
    print(model2.config)

    # Class Attribute usage
    print(f"\nModels created: {BaseModel.model_count}")

    # Trainers
    trainer1 = Trainer(model1, loader)
    trainer2 = Trainer(model2, loader)

    # Run Training
    trainer1.run()
    trainer2.run()