# 代码模板
变化检测深度学习训练测试框架模板

- dataset文件夹: 读取变化检测数据集的相关代码
- mdoels文件夹：将你的模型放在这个文件夹内，本模板使用BiT作为例子
- losses.py：包含变化检测常用的loss函数
- metric_tool.py: 变化检测计算指标的函数
- params&flops.py: 计算模型参数量和计算量
- train.py: 训练模型，需要导入你自己的模型
- val.py: 验证模型，需要填写你训练好的模型文件夹名称
- utils.py: 训练验证相关的一些工具函数

数据集目录结构示意：
```数据集目录结构
Dataset_dir/
  │
  ├── A/
  │   ├── tarin_1.jpg
  │   └── test_1.jpg
  │   └── val_1.jpg
  │   └── .....
  │
  ├── B/
  │   ├── tarin_1.jpg
  │   └── test_1.jpg
  │   └── val_1.jpg
  │   └── .....
  │
  ├── label/
  │   ├── tarin_1.jpg
  │   └── test_1.jpg
  │   └── val_1.jpg
  │   └── .....
  │
  └── list/
      ├── train.txt
      └── test.txt
      └── val.txt
