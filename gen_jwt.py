import secrets
import jwt
from datetime import datetime, timedelta
from api.config import ALGORITHM,USER_INFO_LIST

def generate_jwt_secret_key():
    """ 生成一个安全的 JWT 密钥 """
    return secrets.token_hex(32)  # 生成 32 字节（64 个十六进制字符）的密钥

def create_access_token(data: dict,jwt_secret_key , expires_delta: timedelta = None):
    """
    生成 JWT Token
    当 expires_delta 为 None 时，token 永不过期（不会包含 exp 字段）
    :param data: 要编码到 token 中的数据
    :param expires_delta: token 有效期，传入 None 表示 token 永不过期
    :return: 加密后的 JWT token
    """
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt

if __name__ == "__main__":
    # 生成密钥
    jwt_secret_key = generate_jwt_secret_key()
    with open("user_token.txt", "w", encoding="utf-8") as file:
        file.write(f"JWT_SECRET_KEY: {jwt_secret_key}\n\n")
        # 示例：生成永不过期的 token
        for user_info in USER_INFO_LIST:
            token = create_access_token(user_info, jwt_secret_key, expires_delta=None)
            file.write("user_info: " + str(user_info) + "\nJWT_TOKEN: \t" + token + "\n\n")