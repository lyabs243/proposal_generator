import os
from fastapi import FastAPI, HTTPException, Security, Depends, status, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from models.proposal_agent import ProposalAgent
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(
    title="Proposal Generator API",
    description="API to generate winning proposals for freelancers based on job descriptions.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Custom exception handler to provide more user-friendly validation error messages.
    """
    errors = []
    for error in exc.errors():
        if error["type"] == "missing":
            field_name = error["loc"][-1]
            errors.append(f"The field '{field_name}' is required but was missing.")
        else:
            errors.append(error["msg"])

    return JSONResponse(
        status_code=422,
        content={"detail": errors[0] if len(errors) == 1 else errors},
    )


# Security Setup
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials"
    )

class JobDescriptionRequest(BaseModel):
    job_description: str = Field(
        ..., 
        title="Job Description",
        description="The full text of the job description or project details provided by the client.",
        example="Looking for a Python developer to build a FastAPI backend..."
    )


class ProposalResponse(BaseModel):
    proposal: str = Field(
        ..., 
        title="Generated Proposal",
        description="The generated proposal text."
    )


@app.get("/", tags=["Home"])
async def root():
    return {"message": "Hello World"}


@app.post(
    "/generate-proposal", 
    response_model=ProposalResponse,
    tags=["Proposal"],
    summary="Generate a proposal from a job description",
    dependencies=[Depends(get_api_key)]
)
async def generate_proposal(request: JobDescriptionRequest):
    """
    **Generates a customized proposal** based on the provided job description.
    
    This endpoint utilizes the `ProposalAgent` to analyze the job description, 
    search for relevant past experience, and generate a professional proposal.
    """
    try:
        agent = ProposalAgent()
        proposal_text = await agent.run(request.job_description)
        return ProposalResponse(proposal=proposal_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating proposal: {str(e)}")