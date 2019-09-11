import argparse
import json
import os
import time

from flask import Flask, render_template, request
from loguru import logger
from scipy import spatial

app = Flask(__name__)


def search_images(embeddings, image_id, hits=10):
    input_vector = embeddings[image_id]
    search_result = {}
    for image_id, vector in embeddings.items():
        cos_sim = spatial.distance.cosine(input_vector, vector)
        search_result[image_id] = cos_sim
    sorted_result = sorted(search_result.items(), key=lambda x: x[1])
    return sorted_result[:hits]


def add_metadata(search_result):
    meta_result = []
    for i, (image_id, distance) in enumerate(search_result, start=1):
        image_path = "image/{}.jpg".format(image_id)
        meta_result.append({'pos': i, 'image_id': image_id, 'image_path': image_path, 'distance': distance})
    return meta_result


def load_db(db_name):
    embeddings = {}
    with open(db_name, 'r') as f:
        for row in f:
            json_line = json.loads(row)
            embeddings[json_line['image_id']] = json_line['vector']
    return embeddings


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-path', default='db')
    return parser.parse_args()


@app.route("/")
def index():
    query_image_id = request.args.get('image_id', default=1, type=int)
    query_image_path = "image/{}.jpg".format(query_image_id)
    query = {'image_id': query_image_id, 'image_path': query_image_path}

    search_result = search_images(embeddings, image_id=query_image_id)
    meta_result = add_metadata(search_result)
    return render_template("index.html", image_ids=image_ids, query=query, result=meta_result)


if __name__ == "__main__":
    args = parse_args()

    db_timestampe_path = os.path.join(args.db_path, 'timestamp.txt')
    while not os.path.exists(db_timestampe_path):
        logger.info("index_builder hasn't finished..")
        time.sleep(10)
    os.remove(db_timestampe_path)
    logger.info("Remove {}".format(db_timestampe_path))

    embeddings = load_db(args.db_path)
    image_ids = sorted(embeddings.keys())
    app.run(debug=False, host='0.0.0.0', port=8080)
