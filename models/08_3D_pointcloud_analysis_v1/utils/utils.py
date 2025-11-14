import os
import yaml
import json
import numpy as np


def load_config(filename: str):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    raise FileNotFoundError(f"File {filename} not found.")

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    raise FileNotFoundError(f"File {filename} not found.")

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def rotation_matrix_from_vectors(vec1, vec2):
    a = vec1 / np.linalg.norm(vec1)
    b = vec2 / np.linalg.norm(vec2)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    if s == 0:
        return np.eye(3)
    kmat = np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]])
    R = np.eye(3) + kmat + kmat @ kmat * ((1 - c) / (s**2))
    return R

