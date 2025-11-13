from flask import Flask, request, jsonify, render_template
from supabase import create_client
import os
import datetime

app = Flask(__name__, template_folder="../templates", static_folder="../static")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/send_message")
def send_message():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # ADMIN LOGIN
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


@app.get("/admin/messages")
def admin_messages():
    res = supabase.table("messages").select("*").order("id", desc=True).execute()
    messages = res.data
    return render_template("admin_messages.html", messages=messages)


@app.post("/admin/delete/<int:msg_id>")
def delete_message(msg_id):
    supabase.table("messages").delete().eq("id", msg_id).execute()
    return jsonify({"deleted": True})


def handler(request, context):
    return app(request, context)
