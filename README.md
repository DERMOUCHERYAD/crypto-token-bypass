```markdown
# CocoRiCo AEAD - FCSC 2025

## Description
Ce challenge est un classique du **CTF crypto** basé sur un chiffrement AEAD maison. Il simule un système de connexion où le serveur génère des jetons chiffrés contenant des droits d'utilisateur (admin ou non). L'objectif est de se faire passer pour un administrateur pour obtenir le flag.

## Catégorie
**Crypto / AEAD abuse / OFB keystream reuse**

## Défi
Le serveur propose deux chemins lors du login :
- Si vous êtes un nouvel utilisateur (Are you new? y), vous fournissez un nom et recevez un jeton contenant `{"name": "<nom>", "admin": false}`.
- Si vous avez déjà un token (Are you new? n), vous pouvez le redonner pour être reconnecté. Si le nom est "toto" **et** `admin == true`, le flag est dévoilé.

## Vulnérabilité
- Le chiffrement utilisé est AES en mode **OFB** avec un IV constant.
- Le tag d'intégrité est un simple CRC32 (non cryptographique).
- Cela permet de **rejouer le keystream** pour modifier les données sans détection.

## Exploit
1. **Login en tant que nouvel utilisateur** (par ex. "ryad")
   - On reçoit un token chiffré `T_user` correspondant au JSON suivant :
     ```json
     {"name": "ryad", "admin": false}
     ```

2. **Extraction du keystream**  
   - On connaît le plaintext exact et le CRC32
   - On calcule :
     ```python
     keystream = T_user ⊕ (plaintext_user + crc_user)
     ```

3. **Forge d'un nouveau token admin**
   - On crée le message suivant :
     ```json
     {"name": "toto", "admin": true}
     ```
   - On le CRC32, puis on refait :
     ```python
     T_admin = keystream ⊕ (plaintext_admin + crc_admin)
     ```

4. **Login avec ce jeton forgé** (Are you new? n)
   - Le serveur nous considère comme admin et renvoie le flag.

## Script d'exploitation
Un script `get_flag.py` est fourni pour automatiser la connexion au serveur avec un jeton admin préfabriqué.

## Ce qu'on apprend
- Ne **jamais** réutiliser le keystream dans un chiffrement par flot (stream cipher) !
- Ne **jamais** utiliser CRC32 comme tag d'intégrité !
- Le mode OFB, comme CTR ou CFB, n'assure aucune authentification.

## Catégories CTF
- Crypto
- Keystream Reuse
- AEAD Bypass
- Token Forgery

## Tags
`OFB`, `stream cipher`, `CRC32`, `keystream`, `token forgery`, `AEAD`, `FCSC 2025`

```

