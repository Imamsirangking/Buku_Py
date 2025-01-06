import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def print_response(response):
    """Print response data in a formatted way."""
    if response.status_code in [200, 201]:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error {response.status_code}: {response.text}")

def create_buku():
    """Send POST request to create a new book."""
    print("Masukkan detail buku:")
    judul = input("Judul: ")
    penulis = input("Penulis: ")
    deskripsi = input("Deskripsi: ")
    harga = float(input("Harga: "))
    genre = input("Genre: ")
    payload = {
        "judul": judul,
        "penulis": penulis,
        "deskripsi": deskripsi,
        "harga": harga,
        "genre": genre
    }
    response = requests.post(f"{API_BASE_URL}/buku", json=payload)
    print_response(response)

def read_all_buku():
    """Send GET request to fetch all books."""
    response = requests.get(f"{API_BASE_URL}/buku")
    print_response(response)

def read_buku_by_id():
    """Send GET request to fetch a book by ID."""
    buku_id = input("Masukkan ID buku: ")
    response = requests.get(f"{API_BASE_URL}/buku/{buku_id}")
    print_response(response)

def update_buku():
    """Send PUT request to update a book."""
    buku_id = input("Masukkan ID buku yang ingin diupdate: ")
    print("Masukkan detail buku yang diperbarui:")
    judul = input("Judul: ")
    penulis = input("Penulis: ")
    deskripsi = input("Deskripsi: ")
    harga = float(input("Harga: "))
    genre = input("Genre: ")
    payload = {
        "judul": judul,
        "penulis": penulis,
        "deskripsi": deskripsi,
        "harga": harga,
        "genre": genre
    }
    response = requests.put(f"{API_BASE_URL}/buku/{buku_id}", json=payload)
    print_response(response)

def delete_buku():
    """Send DELETE request to delete a book."""
    buku_id = input("Masukkan ID buku yang ingin dihapus: ")
    response = requests.delete(f"{API_BASE_URL}/buku/{buku_id}")
    print_response(response)

def main():
    """Main menu for CRUD operations."""
    while True:
        print("\nMenu:")
        print("1. Tambah Buku")
        print("2. Lihat Semua Buku")
        print("3. Lihat Buku Berdasarkan ID")
        print("4. Perbarui Buku")
        print("5. Hapus Buku")
        print("6. Keluar")
        choice = input("Masukkan pilihan Anda: ")
        
        if choice == "1":
            create_buku()
        elif choice == "2":
            read_all_buku()
        elif choice == "3":
            read_buku_by_id()
        elif choice == "4":
            update_buku()
        elif choice == "5":
            delete_buku()
        elif choice == "6":
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
