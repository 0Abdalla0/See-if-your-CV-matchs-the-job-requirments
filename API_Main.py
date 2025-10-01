import uvicorn
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os

# --- Import your existing CrewAI crew and tools ---
# This assumes your project structure is:
# /main_api.py
# /src
#   /hr
#     /crew.py
#     /... (agents, tasks, etc.)
# /CVReadTool.py
from src.hr.crew import Hr 
from CVReadTool import CVReadTool 
from crewai_tools import FileReadTool


# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# CREATE THE FASTAPI APPLICATION
# --------------------------------------------------------------------------
app = FastAPI(
    title="HR ATS CrewAI API",
    description="An API that leverages a CrewAI team to analyze CVs against job descriptions.",
    version="1.0.0",
)


# --------------------------------------------------------------------------
# DEFINE THE PRIMARY API ENDPOINT
# --------------------------------------------------------------------------
@app.post("/analyze-cv/", tags=["CV Analysis"])
async def analyze_cv_endpoint(
    cv_file: UploadFile = File(..., description="The candidate's CV file (PDF, DOCX, TXT)."),
    job_description_file: UploadFile = File(..., description="The Job Description file (TXT, MD).")
):
    """
    This endpoint takes a CV and a job description, uses CrewAI agents to analyze them,
    and returns the analysis result.
    """
    cv_path = f"temp_{cv_file.filename}"
    jd_path = f"temp_{job_description_file.filename}"

    try:
        logger.info(f"Received files for analysis: CV='{cv_file.filename}', JD='{job_description_file.filename}'")

        # --- Save uploaded files temporarily to disk ---
        # CrewAI tools often work best with file paths, so we create temporary files.
        with open(cv_path, "wb") as buffer:
            buffer.write(await cv_file.read())
        
        with open(jd_path, "wb") as buffer:
            buffer.write(await job_description_file.read())

        logger.info(f"Temporary files created: '{cv_path}' and '{jd_path}'")

        # --- Prepare inputs for your crew using the file paths ---
        cv_tool = CVReadTool()
        file_reader = FileReadTool()

        # Use the appropriate tool method, likely `_run` or `run`
        cv_text = cv_tool.run(file_path=cv_path)
        job_desc_text = file_reader.run(file_path=jd_path)
        
        inputs = {
            'CV': cv_text,
            'JobDescription': job_desc_text,
        }

        # --- Kick off your actual CrewAI crew ---
        logger.info("Initiating CrewAI kickoff...")
        hr_crew_instance = Hr()
        result = hr_crew_instance.crew().kickoff(inputs=inputs)
        logger.info("CrewAI analysis completed successfully.")
        
        return JSONResponse(
            status_code=200,
            content={"status": "success", "analysis_result": str(result)}
        )

    except Exception as e:
        logger.error(f"An error occurred during the analysis process: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occurred: {str(e)}"
        )
    finally:
        # --- Clean up the temporary files to be tidy ---
        if os.path.exists(cv_path):
            os.remove(cv_path)
        if os.path.exists(jd_path):
            os.remove(jd_path)
        logger.info("Cleaned up temporary files.")


@app.get("/", tags=["Health Check"])
def read_root():
    """A simple endpoint to confirm the API is alive and running."""
    return {"status": "HR ATS API is operational"}


# --------------------------------------------------------------------------
# MAKE THE APP RUNNABLE
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # This allows you to run `python main_api.py` directly for development
    uvicorn.run(app, host="0.0.0.0", port=8000)

