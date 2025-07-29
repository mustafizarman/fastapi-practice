from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from src.db.connection import get_session
from src.schemas import token_schema, user_schema
from src.api.controllers import auth_controller
from src.core.logger import logger
from fastapi_sso.sso.google import GoogleSSO
# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()

router = APIRouter()

# OAuth2 Login
@router.post("/login", response_model=token_schema.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    """
    OAuth2 Login to get a JWT token.
    Username field expects email.
    """
    logger.info(f"Login request: {form_data.username}")
    return auth_controller.authenticate_and_create_token(db, form_data.username, form_data.password)

# Register
@router.post("/register", response_model=user_schema.UserPublic)
def register_user(
    user_in: user_schema.UserCreate, db: Session = Depends(get_session)
):
    logger.info(f"Registering user: {user_in.email}")
    return auth_controller.register_new_user(db, user_in)

# --- Google SSO ---

CLIENT_ID = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
CLIENT_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

REDIRECT_URI = "http://localhost:8000/api/auth/google/callback"
FRONTEND_URL = "http://localhost:3000"

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in .env")



@router.get("/google/login")
async def google_login():
    async with GoogleSSO(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    ) as google:
        login_url = await google.get_login_redirect()   # ✅ This is a string URL
        print("Redirecting to Google:", login_url)       # ✅ Will print https://accounts.google.com/...
        return login_url

# Google Callback
@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_session)):
    async with GoogleSSO(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    ) as google:
        user = await google.verify_and_process(request)
         
        print("Googlelogin", user)
        if not user:
            return RedirectResponse(url=f"{FRONTEND_URL}/login-failed")

        # Use your DB-aware login or register logic
        db_user = auth_controller.google_register_or_login(
            db,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            picture = user.picture
        )

        # Create token (replace with your real JWT logic)
        token = auth_controller.create_access_token({"sub": db_user.email, "id": db_user.id})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth-callback?token={token}")


# @router.get("/google/login")
# async def google_login():
#     async with GoogleSSO(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#     ) as google:
#         redirect_url = await google.get_login_redirect()
#         return RedirectResponse(redirect_url)

# @router.get("/google/callback")
# async def google_callback(request: Request):
#     async with GoogleSSO(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#     ) as google:
#         user = await google.verify_and_process(request)

#         if not user:
#             return RedirectResponse(url=f"{FRONTEND_URL}/login-failed")

#         # You can now register/login the user to your DB
#         # Here we just create a dummy token
#         token = f"dummy-token-for-{user.email}"

#         return RedirectResponse(url=f"{FRONTEND_URL}/authcallback?token={token}")

# @router.get("/google/callback")
# async def google_callback(request: Request, db: Session = Depends(get_session)):
#      async with GoogleSSO(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#     ) as google_sso:
#         user = await google_sso.verify_and_process(request)

#         if not user:
#             return RedirectResponse(url=f"{FRONTEND_URL}/login-failed")

#         # Register or fetch user from DB
#         from src.api.controllers import auth_controller
#         db_user = auth_controller.google_register_or_login(
#             db, email=user.email, first_name=user.first_name, last_name=user.last_name
#         )

#         token = auth_controller.create_access_token({"sub": db_user.email})
#         return RedirectResponse(url=f"{FRONTEND_URL}/?token={token}")


# @router.get("/google/callback")
# async def google_callback(request: Request, db: Session = Depends(get_session)):
#     async with GoogleSSO(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#     ) as google:
#         user = await google.verify_and_process(request)

#         if not user:
#             return RedirectResponse(url=f"{FRONTEND_URL}/login-failed")

#         # Create or get user
#         db_user = auth_controller.google_register_or_login(
#             db, email=user.email, first_name=user.first_name, last_name=user.last_name
#         )

#         token = auth_controller.create_access_token({"sub": db_user.email})
#         return RedirectResponse(url=f"{FRONTEND_URL}/authcallback?token={token}")
