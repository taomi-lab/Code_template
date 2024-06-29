import argparse
import os
from pprint import pprint
import utils
from dataset.CD_dataset import CDD, CDDataset
import torch
import torch.backends.cudnn as cudnn
from tqdm import tqdm
from metric_tool import ConfuseMatrixMeter
from models.networks import BASE_Transformer
import warnings
warnings.filterwarnings("ignore")

torch.cuda.set_device(0)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', default="SCUNet_6_48_LEVIR_07-08-09-05", help='model name')
    parser.add_argument('-b', '--batch_size', default=16, type=int,
                        metavar='N', help='mini-batch size (default: 16)')
    parser.add_argument('--arch', '-a', metavar='ARCH', default='WNet')
    parser.add_argument('--output_dir', default='./vis',
                        help='dataset name')
    parser.add_argument('--input_channels', default=3, type=int,
                        help='input channels')
    parser.add_argument('--num_classes', default=2, type=int,
                        help='number of classes')
    parser.add_argument('--image_size', default=224, type=int,
                        help='image size')
    parser.add_argument('--dataset', default='LEVIR-CD',
                        help='dataset name')
    parser.add_argument('--img_dir', default='/data/lmt/Dataset/LEVIR_Dataset/LEVIR_224_overlap/',
                        help='dataset name')
    parser.add_argument('--model_name', default='best_model_91.21',
                        help='model name')
    args = parser.parse_args()

    return args


def main():
    config = vars(parse_args())
    print('-' * 20)
    for key in config.keys():
        print('%s: %s' % (key, str(config[key])))
    print('-' * 20)

    cudnn.benchmark = True
    model = BASE_Transformer(input_nc=3, output_nc=2, token_len=4, resnet_stages_num=4,
                             with_pos='learned', enc_depth=1, dec_depth=8)

    model = model.to(device)
    # model = torch.nn.DataParallel(model, device_ids=[0, 1])

    checkpoint = torch.load(f'outputs/{config["name"]}/{config["model_name"]}.pth', map_location='cpu')
    model.load_state_dict(checkpoint["model_G_state_dict"])


    model.eval()

    if config['dataset'] == "CDD":
        val_dataset = CDD(root_dir=config['img_dir'], split='test', img_size=config['image_size'],
                          is_train=False, label_transform='norm')
    else:
        val_dataset = CDDataset(root_dir=config['img_dir'], split='test', img_size=config['image_size'],
                                is_train=False, label_transform='norm')

    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=config['batch_size'],
        shuffle=False,
        drop_last=False)
    running_metric = ConfuseMatrixMeter(n_class=config['num_classes'])
    config['output_dir'] = os.path.join(config['output_dir'], config['name'], "test-img")
    os.makedirs(config['output_dir'], exist_ok=True)

    with torch.no_grad():
        val_acc_list = []
        pbar = tqdm(val_loader)
        for i_batch, sampled_batch in enumerate(pbar):
            image_batch1, image_batch2, label_batch = sampled_batch['A'], sampled_batch['B'], sampled_batch["L"]
            image_batch1, image_batch2, label_batch = image_batch1.to(device), image_batch2.to(device), label_batch.squeeze().to(device)
            outputs = model(image_batch1, image_batch2)
            running_acc = running_metric.update_cm(pr=torch.argmax(outputs, dim=1).cpu().numpy(),
                                                   gt=label_batch.cpu().numpy())
            val_acc_list.append(running_acc)
            # utils.draw(sampled_batch, outputs, config['output_dir'], i_batch, 0, 'test')

        test_scores = running_metric.get_scores()
        pbar.close()
        pprint(test_scores)
        with open(f"./outputs/{config['name']}/test_res.txt", 'w', encoding='utf-8') as fp:
            for key in config.keys():
                fp.write('%s: %s\n' % (key, str(config[key])))
            fp.write('\n' + '-' * 20 + '\n')
            for key in test_scores.keys():
                fp.write('%s: %s\n' % (key, str(test_scores[key])))


if __name__ == '__main__':
    main()
