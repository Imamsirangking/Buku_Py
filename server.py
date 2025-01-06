from flask import Flask, jsonify, request, abort
import mysql.connector
import os

# Konfigurasi Database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "buku_db"
}

# Inisialisasi Flask app
app = Flask(__name__)

# Koneksi Database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Routes
@app.route('/')
def home():
    server_info = {
        "message": "Welcome to the Buku API!",
        "server": "Flask",
        "host": os.getenv('HOST', 'localhost'),
        "port": os.getenv('PORT', '8000'),
        "endpoints": [
            {"method": "POST", "endpoint": "/buku", "description": "Create a new book"},
            {"method": "GET", "endpoint": "/buku", "description": "Get all books"},
            {"method": "GET", "endpoint": "/buku/<int:buku_id>", "description": "Get a book by ID"},
            {"method": "PUT", "endpoint": "/buku/<int:buku_id>", "description": "Update a book by ID"},
            {"method": "DELETE", "endpoint": "/buku/<int:buku_id>", "description": "Delete a book by ID"}
        ]
    }
    return jsonify(server_info)

@app.route("/buku", methods=["POST"])
def create_buku():
    """Tambah buku baru."""
    data = request.json
    required_fields = ["judul", "penulis", "deskripsi", "harga", "genre"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Semua kolom wajib diisi"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        INSERT INTO buku (judul, penulis, deskripsi, harga, genre)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (data["judul"], data["penulis"], data["deskripsi"], data["harga"], data["genre"]))
    connection.commit()
    buku_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return jsonify({"id": buku_id, **data}), 201

@app.route("/buku", methods=["GET"])
def read_buku():
    """Ambil semua buku."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM buku"
    cursor.execute(query)
    buku_list = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(buku_list)

@app.route("/buku/<int:buku_id>", methods=["GET"])
def read_buku_detail(buku_id):
    """Ambil detail buku berdasarkan ID."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM buku WHERE id = %s"
    cursor.execute(query, (buku_id,))
    buku = cursor.fetchone()
    cursor.close()
    connection.close()
    if not buku:
        abort(404, description="Buku tidak ditemukan")
    return jsonify(buku)

@app.route("/buku/<int:buku_id>", methods=["PUT"])
def update_buku(buku_id):
    """Perbarui buku."""
    data = request.json
    required_fields = ["judul", "penulis", "deskripsi", "harga", "genre"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Semua kolom wajib diisi"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        UPDATE buku
        SET judul = %s, penulis = %s, deskripsi = %s, harga = %s, genre = %s
        WHERE id = %s
    """
    cursor.execute(query, (data["judul"], data["penulis"], data["deskripsi"], data["harga"], data["genre"], buku_id))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        abort(404, description="Buku tidak ditemukan")
    cursor.close()
    connection.close()
    return jsonify({"id": buku_id, **data})

@app.route("/buku/<int:buku_id>", methods=["DELETE"])
def delete_buku(buku_id):
    """Hapus buku."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM buku WHERE id = %s"
    cursor.execute(query, (buku_id,))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        abort(404, description="Buku tidak ditemukan")
    cursor.close()
    connection.close()
    return jsonify({"message": "Buku berhasil dihapus"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
