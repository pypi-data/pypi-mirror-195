import os
import argparse
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
        url = 'https://lilablobssc.blob.core.windows.net/liladata/wild-me/leopard.coco.tar.gz'
        archive = 'leopard.coco.tar.gz'
        utils.download_url(url, archive)

def extract(root):
    utils.print_start2(root)
    with utils.data_directory(root):
        archive = 'leopard.coco.tar.gz'
        utils.extract_archive(archive, delete=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default='data',  help="Output folder")
    parser.add_argument("--name", type=str, default='LeopardID2022',  help="Dataset name")
    args = parser.parse_args()
    get_data(os.path.join(args.output, args.name))