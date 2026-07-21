import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.data import Dataset
import json
import os
from circlecircle2.utilities.logger import logger


class GraphConv(nn.Module):

    def __init__(
        self,
        input_features,
        output_features
    ):

        super().__init__()

        self.linear = nn.Linear(
            input_features,
            output_features
        )

    def forward(
        self,
        x,
        adj
    ):

        x = self.linear(x)

        x = torch.matmul(
            adj,
            x
        )

        return x


    """
    example:
    ------------------------------------------------------------------------------------------
    model = GNN(
        input_features=6,
        output_features=6,
        hidden_layers=[64,128,256],
        dropout=0.2
    )
    -------------------------------------------------------------------------------------------
    """


class GNN(nn.Module):

    def __init__(
        self,
        input_features:int,
        output_features:int,
        hidden_layers:list[int],
        activation=nn.ReLU,
        dropout:float=0.0
    ):

        super().__init__()

        dims=[
            input_features
        ]+hidden_layers

        convs=[]

        for i in range(len(dims)-1):

            convs.append(
                GraphConv(
                    dims[i],
                    dims[i+1]
                )
            )

        self.convs = nn.ModuleList(
            convs
        )

        self.classifier = MLP(
            hidden_layers[-1],
            output_features,
            [
                hidden_layers[-1]//2
            ],
            dropout=dropout
        )

    def forward(
        self,
        x,
        adj
    ):

        # graph feature extraction

        for conv in self.convs:

            x = conv(
                x,
                adj
            )

            x = F.relu(x)

        # global pooling
        #
        # node feature
        #
        # N × feature
        #
        # ↓
        #
        # 1 × feature

        graph_feature = torch.mean(
            x,
            dim=1,
            keepdim=False
        )

        out=self.classifier(
            graph_feature
        )

        return out

    @staticmethod
    def build_knn_adjacency(
        coords,
        k=8
    ):
        N = coords.shape[0]

        dist = torch.cdist(
            coords,
            coords
        )

        _, idx = torch.topk(
            dist,
            k=k+1,
            largest=False
        )

        idx = idx[:,1:]

        adj = torch.zeros(
            N,
            N,
            device=coords.device
        )

        adj.scatter_(
            1,
            idx,
            1
        )

        degree = adj.sum(
            dim=1,
            keepdim=True
        )

        adj = adj/(degree+1e-8)

        return adj


class MLP(nn.Module):
    """
    example:
    ------------------------------------------------------------------------
    model = MLP(
        input_features=9,
        output_features=2,
        hidden_layers=[64, 16]
    )
    ------------------------------------------------------------------------

    input_features = 9
    hidden_layers = [64, 16]
    output_features = 2

    dims = [input_features] + hidden_layers + [output_features] ---->
    dims = [9] + [64, 16] + [2]
    dims = [9, 64, 16, 2]

    nn.Linear(input_features, output_features)

    ...

    """
    def __init__(self,
                 input_features: int,
                 output_features: int,
                 hidden_layers: list[int],
                 activation=nn.ReLU,
                 dropout: float = 0.0,    # randomly deactivate a portion of neurons; value is between 0.0 and 0.2
                 ):
        super().__init__()

        self.input_features = input_features
        self.output_features = output_features
        self.hidden_layers = hidden_layers
        self.activation = activation
        self.dropout = dropout
        self.feature = None

        self.initialize()

    def initialize(self):

        collector = []    # empty sequential list

        all_dims = [self.input_features] + self.hidden_layers + [self.output_features]

        for i in range(len(all_dims)-1):
            current_input_features = all_dims[i]

            current_output_features = all_dims[i+1]

            current_linear = nn.Linear(current_input_features, current_output_features)

            collector.append(current_linear)

            # Add ReLU function
            if i != len(all_dims) - 2:
                collector.append(self.activation())

                # Randomly drop out a portion of neurons.
                if self.dropout > 0:
                    current_dropout = nn.Dropout(p=self.dropout)
                    collector.append(current_dropout)

        self.feature = nn.Sequential(*collector)

    def forward(self, x):
        return self.feature(x)


class Conv(nn.Module):
    def __init__(self,
                 conv_type: str,
                 in_channels: int,
                 out_channels: int,
                 hidden_layers: list[int],
                 kernel_size: int,
                 activation=nn.ReLU,
                 dropout: float = 0.0,
                 ):
        super().__init__()

        layers = []

        # Dynamically construct convolutional layer blocks
        for layer in hidden_layers:
            if conv_type == "1d":
                current_conv = nn.Conv1d(in_channels=in_channels,
                                         out_channels=out_channels,)



class DummyMLPClassificationDataset(Dataset):
    """
    to test MLP classification task
    fake data

    if x % 2 == 0, y = true, else y = false
    """

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.x = torch.arange(1, 1001, 1, dtype=torch.float32, device=self.device)
        self.x = self.x.unsqueeze(1)

        self.y = torch.full((1000, ), 0, dtype=torch.long, device=self.device)

        index = torch.where(self.x % 2 != 0)[0]

        self.y[index] = 1

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


class DummyMLPRegressionDataset(Dataset):
    """
    to test MLP regression task
    fake data
    y = 2 * x + 1
    """

    def __init__(self):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.x = torch.arange(1, 1000, 1, dtype=torch.float32, device=self.device)
        self.x = self.x.unsqueeze(1)

        length_x = self.x.shape[0]

        noise = torch.randn(length_x, 1, dtype=torch.float32, device=self.device) * 0.1

        self.y = 2 * self.x + 1 + noise

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


class NodeFeaturesMLPDataset(Dataset):
    """
    get node coords and node norms from .json

    usage:

    file_path = r"E:\PythonProject\circlecircle2\Test_Items\material_mapping.json"

    test_dataset = NodeMLPDataset(file_path)

    """
    def __init__(self, file_path):
        self.logger = logger
        self.file_path = file_path
        self.name = file_path

        if os.path.isfile(self.file_path):
            with open(file_path, mode="r", encoding="utf-8", errors="ignore") as f:

                self.part_dict = json.load(f)

        else:
            self.part_dict = {}
            self.logger.error(f"File {self.file_path} not found. Dataset is empty\n")

        self.keys = []

        # check all part dict if there is an empty part dictionary
        for part_name, value in self.part_dict.items():
            part_coords = value["node_coords"]

            if len(part_coords) > 0:
                self.keys.append(part_name)
            else:
                self.logger.warning(f"current file:    {self.file_path},    {part_name} is empty\n")

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, idx):
        # part_dict format:
        # name: {"node_ids": [], "node_coords": [], "node_norms": [], "element_ids": [], "element_norms": [], "element_areas": [], "label": -1}
        part_name = self.keys[idx]

        part = self.part_dict[part_name]

        coords = torch.tensor(part["node_coords"], dtype=torch.float32)
        coords = F.normalize(coords, p=2, dim=1)    # p=2 to calculate Euclidean distance

        norms = torch.tensor(part["node_norms"], dtype=torch.float32)

        label = torch.tensor(part["label"], dtype=torch.long)

        x = torch.cat((coords, norms), dim=1)

        y = label

        return x, y


class Trainer:
    """
    example:
    trainer = Trainer(model=model,
                  dataloader=dataloader,
                  optimizer=optimizer,
                  loss_fn=nn.CrossEntropyLoss(),
                  epochs=50)

    trainer.train()

    nn.CrossEntropyLoss(): normally used to categorize items, like 1 is Cat, 2 is Dog
    nn.MSELoss(): normally used to predict continuous numerical values

    If it is used for a regression task, disable dropout, set dropout to 0.0
    If it is used for a classification task, set dropout to 0.1 - 0.2, normally
    """
    def __init__(self, model, dataloader, optimizer, loss_fn, epochs):
        self.model = model
        self.dataloader = dataloader
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.epochs = epochs
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger = logger
        self.logger.debug(f"device is {self.device}\n")

    def train(self):
        self.model.to(self.device)

        for epoch in range(self.epochs):
            self.model.train()

            running_loss = 0.0

            for batch_x, batch_y in self.dataloader:
                batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)

                self.optimizer.zero_grad()

                output = self.model(batch_x)

                loss = self.loss_fn(output, batch_y)

                loss.backward()

                self.optimizer.step()

                running_loss += loss.item()

            average_loss = running_loss / len(self.dataloader)

            self.logger.debug(f"Epoch: {epoch+1}, Loss: {average_loss}")


class TestDataset:
    """
    to test dataset work successfully

    usage:

    dataset_tester = TestDataset(data_type="mlp")

    dataset_tester.test(dataset)
    """
    def __init__(self, data_type):
        self.data_type = data_type
        self.logger = logger

    def test(self, dataset):
        self.logger.debug(f"Testing dataset: {dataset.name}")
        self.logger.debug(f"include part name: {dataset.keys}")

        if self.data_type == "mlp":
            length = len(dataset)
            self.logger.debug(f"include data batch: {length}\n")

            for i in range(length):
                x, y = dataset[i]
                self.logger.debug(f"part name: {dataset.keys[i]}")
                self.logger.debug(f"x shape is {x.shape}, y shape is {y.shape}\n")


if __name__ == '__main__':
    # model = MLP(
    #     input_features=1,
    #     output_features=2,
    #     hidden_layers=[16, 8],
    #     dropout=0.0
    # )
    #
    # # dataset = DummyMLPRegressionDataset()
    # dataset = DummyMLPClassificationDataset()
    #
    # dataloader = DataLoader(
    #     dataset,
    #     batch_size=50,
    #     shuffle=True
    # )
    #
    # optimizer = optim.Adam(model.parameters(), lr=0.002)
    #
    # trainer = Trainer(model=model,
    #                   dataloader=dataloader,
    #                   optimizer=optimizer,
    #                   loss_fn=nn.CrossEntropyLoss(),
    #                   epochs=100)
    #
    # trainer.train()
    #
    # model.eval()
    # with torch.no_grad():
    #
    #     test_x = torch.tensor([[10]], dtype=torch.float32, device="cuda")
    #     outputs = model(test_x)
    #
    #     print(outputs)

    file_path = r"E:\PythonProject\circlecircle2\Test_Items\test_model.json"
    dataset = NodeFeaturesMLPDataset(file_path=file_path)

    dataset_tester = TestDataset(data_type="mlp")
    dataset_tester.test(dataset)


