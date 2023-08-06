import os
import argparse
import shutil
if __name__ == '__main__':
    import utils
else:
    from . import utils

def get_data(root):
    download(root)
    extract(root)
    utils.print_finish(root)

def download(root):
    utils.print_start1(root)
    with utils.data_directory(root):
        url = 'https://github.com/cvjena/chimpanzee_faces/archive/refs/heads/master.zip'
        archive = 'master.zip'
        utils.download_url(url, archive)

def extract(root):
    utils.print_start2(root)
    with utils.data_directory(root):
        archive = 'master.zip'
        utils.extract_archive(archive, delete=True)

        # Cleanup
        shutil.rmtree('chimpanzee_faces-master/datasets_cropped_chimpanzee_faces/data_CTai')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default='data',  help="Output folder")
    parser.add_argument("--name", type=str, default='CZoo',  help="Dataset name")
    args = parser.parse_args()
    get_data(os.path.join(args.output, args.name))