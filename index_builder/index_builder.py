from environs import Env
import json
import pathlib

import os

import time

import datetime
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
            logger.info("image_id: {} saved".format(image_id))
        except RuntimeError as e:
            logger.error("image_id: {}, {}".format(image_id, e))
    return embeddings


def make_index(image_path):
    images = load_images(image_path)
    cropped_images = crop_images(images)
    return get_embeddings(cropped_images)


def save_db(embeddings, db_path):
    with open(os.path.join(db_path, 'db.txt'), 'w') as f:
        for image_id, vector in embeddings.items():
            json_line = json.dumps({"image_id": image_id, "vector": vector})
            f.write(json_line + '\n')




if __name__ == "__main__":
    env = Env()
    db_path = env("DB_PATH")
    if not os.path.exists(db_path):
        os.mkdir(db_path)

    image_path = env("IMAGE_PATH")
    image_timestamp_path = env("IMAGE_TIMESTAMP_PATH")
    while not os.path.exists(image_timestamp_path):
        logger.info("image_downloader hasn't finished..")
        time.sleep(10)

    logger.info("Start to make {}".format(db_path))
    embeddings = make_index(image_path)
    save_db(embeddings, db_path)
    logger.info("Save {}".format(db_path))

    os.remove(image_timestamp_path)
    logger.info("Remove {}".format(image_timestamp_path))

    db_timestamp_path = os.path.join(db_path, 'timestamp.txt')
    with open(db_timestamp_path, 'w') as f:
        now = int(datetime.datetime.now().timestamp())
        f.write(str(now))
