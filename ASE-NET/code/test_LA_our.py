import os
import argparse
import torch
from networks.vnet import VNet
from test_util_1 import test_all_case

parser = argparse.ArgumentParser()
parser.add_argument('--root_path', type=str,
                    default='data/2018LA_Seg_Training Set', help='Name of Experiment')
parser.add_argument('--model', type=str,
                    default='DTC_with_consis_weight_16labels_beta_0.3', help='model_name')
parser.add_argument('--gpu', type=str,  default='0', help='GPU to use')
parser.add_argument('--patch_size', nargs='+', type=int, default=[128, 128, 128], help='Patch _size')
parser.add_argument('--detail', type=int,  default=1,
                    help='print metrics for every samples?')
parser.add_argument('--nms', type=int, default=0,
                    help='apply NMS post-procssing?')


FLAGS = parser.parse_args()

os.environ['CUDA_VISIBLE_DEVICES'] = FLAGS.gpu
snapshot_path = "weight_our/{}".format(FLAGS.model)

num_classes = 2

test_save_path = os.path.join(snapshot_path, "test/")
if not os.path.exists(test_save_path):
    os.makedirs(test_save_path)
print(test_save_path)
with open(FLAGS.root_path + '/../test.list', 'r') as f:
    image_list = f.readlines()
image_list = [FLAGS.root_path + "/" + item.replace('\n', '') + "/mra_norm.h5" for item in
              image_list]


def test_calculate_metric():
    net = VNet(n_channels=1, n_classes=num_classes,
               normalization='batchnorm', has_dropout=False).cuda()
    save_mode_path = os.path.join(
        snapshot_path, 'iter_12000.pth')#3500 87 
    net.load_state_dict(torch.load(save_mode_path))
    print("init weight from {}".format(save_mode_path))
    net.eval()

    avg_metric = test_all_case(net, image_list, num_classes=num_classes,
                               patch_size=tuple(FLAGS.patch_size), stride_xy=18, stride_z=4,
                               save_result=True, test_save_path=test_save_path)

    return avg_metric


if __name__ == '__main__':
    metric = test_calculate_metric()  # 6000
    print(metric)
