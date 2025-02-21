from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from api.config import SECRET_KEY, ALGORITHM
from api.logging import logs  # 初始化日志

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    """校验 JWT 令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logs.info("用户访问",payload)
        return payload  # 返回解码后的 JWT 数据
    except :
        logs.exception("未授权的用户访问",token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的 Token")