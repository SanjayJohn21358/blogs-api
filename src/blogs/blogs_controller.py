from flask import Flask, jsonify, abort, request
import json
from blogs_service import BlogsService, NotFoundError, ConflictError
import pathlib

app = Flask(__name__)
# data path string can live in a settings file or config.yml
data_path = pathlib.Path("src/data")
blogs_data_path = data_path / "blogs.csv"
service = BlogsService(blogs_data_path)

@app.route("/health")
def health_check():
    return "System is OK!"

@app.route("/blogs", methods=["GET", "POST"])
def get_blogs():
    try:
        if request.method == "GET":
            return jsonify(service.get_blogs())
        elif request.method == "POST":
            return service.create_blog(**request.json)
    except ConflictError:
        return abort(409, description="Resource already exists!")

@app.route("/blogs/<name>")
def get_blog(name):
    try:
        return jsonify(service.get_blog(name))
    except NotFoundError:
        return abort(404, description=f"Resource not found.")

if __name__ == "__main__":
    app.run(port=5123)
