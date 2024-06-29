from thop import profile
import torch
from models.networks import BASE_Transformer


img = torch.randn(1, 3, 256, 256)
print("-"*20,"SCUNet","-"*20)
model = BASE_Transformer(input_nc=3, output_nc=2, token_len=4, resnet_stages_num=4,
                             with_pos='learned', enc_depth=1, dec_depth=8)
macs, params = profile(model, inputs=(img, img), verbose = False)
print('{:<30}  {:<8}'.format('Computational complexity: ', macs))
print('{:<30}  {:<8}'.format('Number of parameters: ', params))

# from sklearn.metrics import confusion_matrix
# C = confusion_matrix(labels,pre)
# C_T = C.transpose()
# for i, line in enumerate(cm):
#     TP = line[i]
#     FN = sum(line) - line[i]
#     FP = sum(C_T[i]) - line[i]
#     TN = 0


# print("-"*20,"SCUNet_Best_96","-"*20)
# model2 = SCUNet_Best(embed_dim=96)
# macs, params = profile(model2, inputs=(img, img), verbose = False)
# print('{:<30}  {:<8}'.format('Computational complexity: ', macs))
# print('{:<30}  {:<8}'.format('Number of parameters: ', params))

