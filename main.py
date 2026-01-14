from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from models.proposal_agent import ProposalAgent

app = FastAPI(
    title="Proposal Generator API",
    description="API to generate winning proposals for freelancers based on job descriptions.",
    version="1.0.0"
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
    summary="Generate a proposal from a job description"
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