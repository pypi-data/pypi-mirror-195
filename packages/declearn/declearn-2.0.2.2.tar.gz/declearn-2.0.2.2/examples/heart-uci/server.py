# coding: utf-8

# Copyright 2023 Inria (Institut National de Recherche en Informatique
# et Automatique)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to run a federated server on the heart-disease example."""

import argparse
import os

from declearn.communication import NetworkServerConfig
from declearn.main import FederatedServer
from declearn.main.config import FLOptimConfig, FLRunConfig
from declearn.model.sklearn import SklearnSGDModel

FILEDIR = os.path.dirname(os.path.abspath(__file__))


def run_server(
    nb_clients: int,
    sv_cert: str,
    sv_priv: str,
) -> None:
    """Instantiate and run the orchestrating server.

    Arguments
    ---------
    nb_clients: int
        Exact number of clients used in this example.
    sv_cert: str
        Path to the (self-signed) SSL certificate to use.
    sv_priv: str
        Path to the associated private-key to use.
    """

    # (1) Define a model

    # Here we use a scikit-learn SGD classifier and parametrize it
    # into a L2-penalized binary logistic regression.
    model = SklearnSGDModel.from_parameters(
        kind="classifier", loss="log_loss", penalty="l2", alpha=0.005
    )

    # (2) Define an optimization strategy

    # Configure the aggregator to use.
    # Here, averaging weighted by the effective number
    # of local gradient descent steps taken.
    aggregator = {
        "name": "averaging",
        "config": {"steps_weighted": True},
    }

    # Configure the client-side optimizer to use.
    # Here, RMSProp optimizer with 0.02 learning rate.
    client_opt = {
        "lrate": 0.02,
        "modules": ["rmsprop"],
    }

    # Configure the server-side optimizer to use.
    # Here, apply momentum to the updates and apply them (as lr=1.0).
    server_opt = {
        "lrate": 1.0,
        "modules": [("momentum", {"beta": 0.95})],
    }

    # Wrap this up into an OptimizationStrategy object.
    optim = FLOptimConfig.from_params(
        aggregator=aggregator,
        client_opt=client_opt,
        server_opt=server_opt,
    )

    # (3) Define network communication parameters.

    # Here, use websockets protocol on localhost:8765, with SSL encryption.
    network = NetworkServerConfig(
        protocol="websockets",
        host="localhost",
        port=8765,
        certificate=sv_cert,
        private_key=sv_priv,
    )

    # (4) Instantiate and run a FederatedServer.

    # Here, we add instructions to compute accuracy, precision, recall,
    # f1-score and roc auc (with plot-enabling fpr/tpr curves) during
    # evaluation rounds.
    server = FederatedServer(
        # fmt: off
        model, network, optim,
        metrics=["binary-classif", "binary-roc"],
        checkpoint=f"{FILEDIR}/results/server"
    )

    # Here, we set up 20 rounds of training, with 30 samples per batch
    # during training and 50 during validation; plus an early-stopping
    # criterion if the global validation loss stops decreasing for 5 rounds.
    run_cfg = FLRunConfig.from_params(
        rounds=20,
        register={"min_clients": nb_clients},
        training={"batch_size": 30, "drop_remainder": False},
        evaluate={"batch_size": 50, "drop_remainder": False},
        early_stop={"tolerance": 0.0, "patience": 5, "relative": False},
    )
    server.run(run_cfg)


# Called when the script is called directly (using `python server.py`).
if __name__ == "__main__":
    # Parse command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "nb_clients",
        type=int,
        help="number of clients",
        choices=[1, 2, 3, 4],
    )
    parser.add_argument(
        "--cert_path",
        dest="cert_path",
        type=str,
        help="path to the server-side ssl certification",
        default=os.path.join(FILEDIR, "server-cert.pem"),
    )
    parser.add_argument(
        "--key_path",
        dest="key_path",
        type=str,
        help="path to the server-side ssl private key",
        default=os.path.join(FILEDIR, "server-pkey.pem"),
    )
    args = parser.parse_args()
    # Run the server routine.
    run_server(args.nb_clients, args.cert_path, args.key_path)
