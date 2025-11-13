from flask import Flask, request, jsonify, render_template, send_from_directory
from supabase import create_client
import os
import datetime

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Supabase environment variables from Vercel
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- CONTACT FORM API ----------------
@app.route("/api/send_message", methods=["POST"])
def send_message():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # Admin login shortcut
    if (
        name == "AdityaAdmin"
        and email == "adisinghx11@gmail.com"
        and message.lower() == "show database"
    ):
        return jsonify({"admin": True})

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    supabase.table("messages").insert({
        "name": name,
        "email": email,
        "message": message,
        "timestamp": timestamp
    }).execute()

    return jsonify({"success": True})


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/messages")
def admin_messages():
    res = supabase.table("messages").select("*").order("id", desc=True).execute()
    messages = res.data
    return render_template("admin_messages.html", messages=messages)


# ---------------- DELETE MESSAGE ----------------
@app.route("/admin/delete/<int:msg_id>", methods=["POST"])
def delete_message(msg_id):
    supabase.table("messages").delete().eq("id", msg_id).execute()
    return jsonify({"deleted": True})


# ---------------- STATIC FILES ----------------
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("../static", path)


# Vercel entry point
def handler(request, context):
    return app(request, context)
