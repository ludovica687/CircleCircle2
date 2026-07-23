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
                 padding: int,
                 activation=nn.ReLU,
                 dropout: float = 0.0,
                 ):
        super().__init__()

        layers = []

        # Dynamically construct convolutional layer blocks
        for layer in hidden_layers:

            if conv_type == "1d":
                current_conv = nn.Conv1d(in_channels=in_channels,
                                         out_channels=out_channels,
                                         kernel_size=kernel_size,
                                         padding=padding)
            else:
                current_conv = None

            layers.append(current_conv)


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

    """
    def __init__(self, node_features_list):
        self.logger = logger
        self.node_features_list = node_features_list

    def __len__(self):
        return len(self.node_features_list)

    def __getitem__(self, idx):
        current_data = self.node_features_list[idx]

        return current_data


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


class FeaturesToTensorExtractor:
    """
    usage:
    dataset data must be saved at cpu !!!
    self.device = "cpu"
    """
    def __init__(self):
        self.logger = logger
        self.device = "cpu"

    # only extract node features from .json, [x, y, z, n1, n2, n3]
    def node_features(self, file_path, num_points):
        if os.path.isfile(file_path):

            current_dataset = []

            with open(file_path, mode="r", encoding="utf-8", errors="ignore") as f:
                current_dict = json.load(f)

            # Combine the coordinates and normal of each part, along dim=1, [x, y, z, n1, n2, n3]
            for part_name, value in current_dict.items():
                part_coords = value["node_coords"]
                part_norms = value["node_norms"]
                part_label = value["label"]

                if len(part_coords) > 0:
                    part_coords_tensor = torch.tensor(part_coords, dtype=torch.float32, device=self.device)
                    part_norms_tensor = torch.tensor(part_norms, dtype=torch.float32, device=self.device)
                    part_labels_tensor = torch.tensor(part_label, dtype=torch.long, device=self.device)

                    part_node_features_tensor = torch.cat((part_coords_tensor, part_norms_tensor), dim=1)

                    part_node_features_tensor = self.sampled_for_node_features(features_tensor=part_node_features_tensor,
                                                                               num_points=num_points,)

                    # part_node_features_tensor_shape_0 = part_node_features_tensor.shape[0]

                    # # If the input data is greater than num_points, a random sampling method is used
                    # if part_node_features_tensor_shape_0 > num_points:
                    #     idx = torch.randperm(n=part_node_features_tensor_shape_0, device=self.device)[: num_points]
                    #
                    #     part_node_features_tensor = part_node_features_tensor[idx]
                    #
                    # # If the input data is less than num_points, a repeated sampling method is used
                    # else:
                    #     repeat_num = num_points - part_node_features_tensor_shape_0
                    #
                    #     idx = torch.randint(low=0,
                    #                         high=part_node_features_tensor_shape_0,
                    #                         size=(repeat_num, ),
                    #                         device=self.device)
                    #
                    #     extra_features = part_node_features_tensor[idx]
                    #
                    #     noise = torch.randn_like(extra_features)
                    #
                    #     extra_features = extra_features + noise * 0.01
                    #
                    #     part_node_features_tensor = torch.cat((part_node_features_tensor, extra_features), dim=0)

                    current_sample = {
                        "part_name": part_name,
                        "features": part_node_features_tensor,
                        "label": part_labels_tensor
                    }

                    current_dataset.append(current_sample)

            return current_dataset

        else:
            self.logger.warning(f"File {file_path} not found\n")

            return None

    def sampled_for_node_features(self, features_tensor, num_points):
        """
        :param features_tensor: features_tensor
        :param num_points: user define number of dim
        :return:
        """

        shape_0 = features_tensor.shape[0]

        if shape_0 == 0:
            raise ValueError("Empty point cloud")

        # If the input data is greater than num_points, a random sampling method is used
        elif shape_0 > num_points:
            idx = torch.randperm(n=shape_0, device=features_tensor.device)[: num_points]

            sampled = features_tensor[idx]

        # If the input data is less than num_points, a repeated sampling method is used
        elif shape_0 < num_points:
            repeat_num = num_points - shape_0

            idx = torch.randint(low=0,
                                high=shape_0,
                                size=(repeat_num,),
                                device=features_tensor.device)

            extra_features = features_tensor[idx]

            coords = extra_features[:, :3]
            normals = extra_features[:, 3:]

            noise = torch.randn_like(coords)

            coords = coords + noise * 0.01

            # extra_features = extra_features + noise * 0.01
            extra_features = torch.cat((coords, normals), dim=1)

            sampled = torch.cat((features_tensor, extra_features), dim=0)

        else:
            sampled = features_tensor

        return sampled


class NodeEmbedding(nn.Module):
    """
    Transform node features into a higher-dimensional space
    node features [x, y, z, n1, n2, n3]
    higher-dimensional features [x1, x2, x3, x4, x5, ,x6, ...]
    """

    def __init__(self,
                 input_dim: int,
                 output_dim: int,):
        super().__init__()

        mid_dim = int(output_dim / 2)

        self.encoder = nn.Sequential(nn.Linear(input_dim, mid_dim),
                                     nn.ReLU(),
                                     nn.Linear(mid_dim, output_dim))

    def forward(self, x):
        x = self.encoder(x)

        return x


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
    # dataset = NodeFeaturesMLPDataset(file_path=file_path)
    #
    # dataset_tester = TestDataset(data_type="mlp")
    # dataset_tester.test(dataset)

    features_to_tensor_extractor = FeaturesToTensorExtractor()
    current_dataset = features_to_tensor_extractor.node_features(file_path=file_path, num_points=1024)

    for i in current_dataset:
        features_shape = i["features"].shape
        print(i["part_name"])
        print(f"shape is {features_shape}")
        print(i["features"])


