from passlib.hash import pbkdf2_sha256

password = "password123"
h = pbkdf2_sha256.hash(password)
print(f"Password: {password}")
print(f"Hash: {h}")

res = pbkdf2_sha256.verify(password, h)
print(f"Verify result: {res}")

# Test with a known hash if possible, or just re-verify
res2 = pbkdf2_sha256.verify("wrong", h)
print(f"Verify wrong result: {res2}")
