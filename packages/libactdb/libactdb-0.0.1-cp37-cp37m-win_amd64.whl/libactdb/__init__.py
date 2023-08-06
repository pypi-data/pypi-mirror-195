import clibactdb as lib
import types
import sys

modules = {
    "torchutils": [
        "get_embedding_model",
        "get_layers_sorted_by_depth",
        "get_layer_names",
        "get_layer",
    ],
    "db": [
        "Table",
        "DB",
    ],
}


for mod_name, items in modules.items():
    mod = types.ModuleType(mod_name)
    for item in items:
        setattr(mod, item, getattr(lib, item))
    sys.modules[f"libactdb.{mod_name}"] = mod


__version__ = "0.0.1"
