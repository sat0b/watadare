import argparse
import json
import pathlib

import os
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from loguru import logger

mtcnn = MTCNN(keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()


def load_images(path):
    images = {}
    path_files = pathlib.Path(path).glob("*.jpg")
    for image_path in sorted(path_files):
        try:
            image_id = int(image_path.stem)
            image = Image.open(image_path)
            images[image_id] = image
        except IOError as e:
            logger.error(e)
    return images


def crop_images(images):
    cropped_images = {}
    for image_id, image in images.items():
        try:
            img_cropped = mtcnn(image)
        except (ValueError, RuntimeError) as e:
            logger.error("image_id: {}, {}".format(image_id, e))
        else:
            cropped_images[image_id] = img_cropped
    return cropped_images


def get_embeddings(cropped_images):
    embeddings = {}
    for image_id, image_cropped in cropped_images.items():
        try:
            tensor = resnet(image_cropped.unsqueeze(0))
            vector = tensor.detach().numpy()
            assert vector.shape == (1, 512)
            embeddings[image_id] = [float(val) for val in tensor.detach().numpy().flatten()]
        except RuntimeError as e:
            logger.error("image_id: {}, {}".format(image_id, e))
    return embeddings


def train(image_path):
    images = load_images(image_path)
    cropped_images = crop_images(images)
    return get_embeddings(cropped_images)


def save_db(embeddings, db_path):
    with open(db_path, 'w') as f:
        for image_id, vector in embeddings.items():
            json_line = json.dumps({"image_id": image_id, "vector": vector})
            f.write(json_line + '\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-path', default='static/image')
    parser.add_argument('--db-path', default='db')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists(args.db_path):
        os.mkdir(args.db_path)
    logger.info("Start to make {}".format(args.db_path))
    embeddings = train(args.image_path)
    save_db(embeddings, args.db_path)
    logger.info("Save {}".format(args.db_path))
