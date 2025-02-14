import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

from tqdm import tqdm

import sys
sys.path.append("..")

import argparse
from src.utils.driver import train_single_model
from src.utils.visualization import visualize_embedding
from src.utils.crystal_metric import crystal_metric
import json

data_id_choices = ["lattice", "greater", "family_tree", "equivalence", "circle"]
model_id_choices = ["H_MLP", "standard_MLP", "H_transformer", "standard_transformer"]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Experiment')
    parser.add_argument('--seed', type=int, default=29, help='random seed')
    parser.add_argument('--data_id', type=str, required=True, choices=data_id_choices, help='Data ID')
    parser.add_argument('--model_id', type=str, required=True, choices=model_id_choices, help='Model ID')


args = parser.parse_args()
seed = args.seed
data_id = args.data_id
model_id = args.model_id

data_size = 1000
train_ratio = 0.8

param_dict = {
    'seed': seed,
    'data_id': data_id,
    'data_size': data_size,
    'train_ratio': train_ratio,
    'model_id': model_id,
    'device': torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
    'embd_dim': 16,
}


# Train the model
print(f"Training model with seed {seed}, data_id {data_id}, model_id {model_id}")
ret_dic = train_single_model(param_dict)

## Exp1: Visualize Embeddings
print(f"Experiment 1: Visualize Embeddings")
model = ret_dic['model']
dataset = ret_dic['dataset']
torch.save(model.state_dict(), f"../results/{seed}_{data_id}_{model_id}_{data_size}_{train_ratio}_d=sqrtembed_1.pt")

if hasattr(model.embedding, 'weight'):
    visualize_embedding(model.embedding.weight.cpu(), title=f"{seed}_{data_id}_{model_id}_{data_size}_{train_ratio}", save_path=f"../results/unit_tests/emb_{seed}_{data_id}_{model_id}_{data_size}_{train_ratio}_new.png", dict_level = dataset['dict_level'] if 'dict_level' in dataset else None)
else:
    visualize_embedding(model.embedding.data.cpu(), title=f"{seed}_{data_id}_{model_id}_{data_size}_{train_ratio}", save_path=f"../results/unit_tests/emb_{seed}_{data_id}_{model_id}_{data_size}_{train_ratio}_new.png", dict_level = dataset['dict_level'] if 'dict_level' in dataset else None)

with open(f"../results/unit_tests/{seed}_{data_id}_{model_id}_{data_size}_{train_ratio}_train_results_new.json", "w") as f:
    json.dump(ret_dic["results"], f, indent=4)

aux_info = {}
if data_id == "lattice":
    aux_info["lattice_size"] = 5
elif data_id == "greater":
    aux_info["p"] = 30
elif data_id == "family_tree":
    aux_info["dict_level"] = dataset['dict_level']
elif data_id == "equivalence":
    aux_info["mod"] = 5
elif data_id == "circle":
    aux_info["p"] = 17
else:
    raise ValueError(f"Unknown data_id: {data_id}")

if hasattr(model.embedding, 'weight'):
    metric_dict = crystal_metric(model.embedding.weight.cpu().detach(), data_id, aux_info)
else:
    metric_dict = crystal_metric(model.embedding.data.cpu(), data_id, aux_info)

with open(f"../results/unit_tests/{seed}_{data_id}_{model_id}_{data_size}_{train_ratio}_new.json", "w") as f:
    json.dump(metric_dict, f, indent=4)

