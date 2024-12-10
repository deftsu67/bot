from cryptography.fernet import Fernet
import sqlite3
def load_key():
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data).decode()

def init_db():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts 
                 (id INTEGER PRIMARY KEY, identifier TEXT, data TEXT)''')
    conn.commit()
    conn.close()

def add_account(identifier, data):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    encrypted_data = encrypt_data(data)
    c.execute("INSERT INTO accounts (identifier, data) VALUES (?, ?)", (identifier, encrypted_data))
    conn.commit()
    conn.close()

def get_account(identifier):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("SELECT data FROM accounts WHERE identifier = ?", (identifier,))
    row = c.fetchone()
    conn.close()
    if row:
        return decrypt_data(row[0])
    return None
def main():
    init_db()
    print("Chào mừng đến với bot lưu tài khoản của Nguyễn Hùng Mạnh!")
    while True:
        print("1. Thêm tài khoản")
        print("2. Lấy tài khoản")
        print("3. Thoát")
        choice = input("Lựa chọn: ")

        if choice == "1":
            identifier = input("Tên lưu: ")
            account_data = input("Nhập tài khoản|mật khẩu: ")
            add_account(identifier, account_data)
            print("Tài khoản đã được lưu!")
        elif choice == "2":
            identifier = input("Tên đã lưu: ")
            account_data = get_account(identifier)
            if account_data:
                print(f"Thông tin tài khoản: {account_data}")
            else:
                print("Không tìm thấy tài khoản.")
        elif choice == "3":
            print("Xin chào!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")

if __name__ == "__main__":
    main()
