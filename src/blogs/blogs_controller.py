from flask import Flask, jsonify, abort
from blogs_service import BlogsService

app = Flask(__name__)
service = BlogsService()

@app.route("/health")
def health_check():
    return "System is OK!"

@app.route("/blogs")
def get_blogs():
    return jsonify(service.get_blogs())

@app.route("/blogs/<name>")
def get_blog(name):
    return jsonify(service.get_blog(name))

if __name__ == "__main__":
    app.run()
