import secrets

def generate_jwt_secret_key():
    """ 生成一个安全的 JWT 密钥 """
    return secrets.token_hex(32)  # 生成 32 字节（64 个十六进制字符）的密钥

# 生成密钥
jwt_secret_key = generate_jwt_secret_key()
print(f"JWT_SECRET_KEY: {jwt_secret_key}")