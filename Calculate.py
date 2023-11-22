import pickle

# 从文件加载图
with open('bike_graph.pkl', 'rb') as f:
    loaded_G = pickle.load(f)