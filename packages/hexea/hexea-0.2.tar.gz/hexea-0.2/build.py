from pybind11.setup_helpers import Pybind11Extension, build_ext
import os

def build(setup_kwargs):
    ext_modules = [
        Pybind11Extension("hexea._board", ["hexea/board.cpp"])
    ]
    setup_kwargs.update({
        "ext_modules": ext_modules,
        "cmd_class": {"build_ext": build_ext},
        "zip_safe": False,
    })
    os.environ["CFLAGS"] = "-std=c++11"
