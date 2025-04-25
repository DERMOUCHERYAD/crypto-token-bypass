#!/usr/bin/env python3
import socket

HOST, PORT = "chall.fcsc.fr", 2150
# Ton jeton admin brut (hex)
TOKEN_ADMIN = "c53cad582562c0c9769b3fe9eb3125de78fb179dd39cfe5c0a10eae7d1d963ed52e86b1f"

def recv_until(s, prompt=b">>> "):
    data = b""
    while not data.endswith(prompt):
        data += s.recv(1)
    return data

def get_flag(token_hex):
    # 1) Connexion
    s = socket.create_connection((HOST, PORT))
    # 2) Skip menu until first prompt
    recv_until(s)
    # 3) Choisir Login (1)
    s.sendall(b"1\n")
    recv_until(s)
    # 4) Dire « not new »
    s.sendall(b"n\n")
    recv_until(s)
    # 5) Envoyer le token admin
    s.sendall(token_hex.encode() + b"\n")
    # 6) Lire la réponse (le flag)
    resp = s.recv(4096)
    s.close()
    return resp.decode(errors="ignore")

if __name__ == "__main__":
    flag = get_flag(TOKEN_ADMIN)
    print("Réponse du serveur :\n", flag)
