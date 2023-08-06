#!/bin/bash
rm -rf build/** &&
python3 -m dirtem template build &&
tree -a -- build
