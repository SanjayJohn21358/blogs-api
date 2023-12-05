from flask import Flask, jsonify, abort, request, Response
from blogs.blogs_service import BlogsService
from blogs.db import NotFoundError, ConflictError, DataFrameRepository
import pathlib

app = Flask(__name__)
repo = DataFrameRepository(pathlib.Path("src/data") / "blogs.csv")
service = BlogsService(repo)

@app.route("/health/status")
def health_check():
    return "System is OK!"

@app.route("/blogs", methods=["GET", "POST"])
def get_blogs():
    """Get or create blogs"""
    try:
        if request.method == "GET":
            return jsonify(service.get_blogs())
        elif request.method == "POST":
            return service.create_blog(request.json)
    except ConflictError:
        return abort(409, description="Resource already exists!")

@app.route("/blogs/<id>", methods=["GET", "DELETE", "PUT"])
def get_blog(id):
    """Get, update or delete singular blog by id"""
    try:
        if request.method == "GET":
            return jsonify(service.get_blog(id))
        elif request.method == "DELETE":
            service.delete_blog(id)
            return Response(status=204)
        elif request.method == "PUT":
            return jsonify(service.update_blog(id, request.json))
    except NotFoundError:
        return abort(404, description=f"Resource not found.")
    
def main():
    app.run(port=5123)
