"""
Bankbot FastAPI Application

This module contains the FastAPI application setup for the Bankbot project.
It configures middleware, includes routers for various endpoints, and defines exception handlers.

"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from common.dependencies import db_connection
from endpoints.csrequest import router as csrequest_router
from endpoints.user import router as user_router

app = FastAPI()

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply database connection middleware
app.middleware("http")(db_connection)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom Exception Handler

    Handles HTTPException and returns a JSONResponse with the error details.

    :param request: The incoming request.
    :param exc: The HTTPException to be handled.
    :return: A JSONResponse with the error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Include routers for different endpoints
app.include_router(csrequest_router, prefix="/csrequest")
app.include_router(user_router, prefix="/user")
