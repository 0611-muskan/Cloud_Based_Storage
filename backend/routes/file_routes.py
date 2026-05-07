from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from aws_config import s3_client

file_bp = Blueprint("file_routes", __name__)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# Upload (USER-SPECIFIC)
@file_bp.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    email = request.form.get("email")

    if not email:
        return jsonify({"message": "Email required"}), 400

    if not file or file.filename == "":
        return jsonify({"message": "No file provided"}), 400

    try:
        # Create unique filename with email prefix
        filename = secure_filename(file.filename)
        key = f"{email}/{uuid.uuid4()}-{filename}"

        # Upload to S3
        s3_client.upload_fileobj(
            file.stream,
            BUCKET_NAME,
            key,
            ExtraArgs={"ContentType": file.content_type}
        )

        # Get the file URL
        location = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
        return jsonify({"url": location}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500


# List files (USER-SPECIFIC)
@file_bp.route("/", methods=["GET"])
def list_files():
    email = request.args.get("email")

    if not email:
        return jsonify({"message": "Email required"}), 400

    try:
        # List objects with email prefix
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=f"{email}/"
        )

        # Format response similar to AWS SDK
        contents = response.get("Contents", [])
        return jsonify(contents), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500


# Delete
@file_bp.route("/<path:key>", methods=["DELETE"])
def delete_file(key):
    try:
        s3_client.delete_object(
            Bucket=BUCKET_NAME,
            Key=key
        )
        return jsonify({"message": "Deleted"}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500


# Share (Generate signed URL)
@file_bp.route("/share/<path:key>", methods=["GET"])
def share_file(key):
    try:
        # Generate signed URL valid for 60 seconds
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=60
        )
        return jsonify({"url": url}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500
