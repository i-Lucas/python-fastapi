import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__));
project_dir = os.path.dirname(current_dir);
src_dir = os.path.join(project_dir, "src");
sys.path.insert(0, src_dir);