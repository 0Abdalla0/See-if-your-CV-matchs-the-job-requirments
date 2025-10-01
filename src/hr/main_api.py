import uvicorn
import logging
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Path
from fastapi.responses import JSONResponse

# --- Import your existing CrewAI crew and tools ---
from src.hr.crew import Hr 
from CVReadTool import CVReadTool 
from crewai_tools import FileReadTool

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Re-add your job titles list ---
job_titles = [
    # A comprehensive list of job titles... (shortened for brevity)
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Data Scientist", "Machine Learning Engineer", "Cybersecurity Analyst",
    "Product Manager", "UI/UX Designer", "Engineering Manager" 
]

# --------------------------------------------------------------------------
# CREATE THE FASTAPI APPLICATION
# --------------------------------------------------------------------------
app = FastAPI(
    title="HR ATS CrewAI API",
    description="A comprehensive API for running, training, and managing the HR analysis crew.",
    version="1.1.0",
)

# --- Helper Function to Process Inputs ---
# This avoids code repetition across endpoints.
async def process_inputs_from_files(cv_file: UploadFile, job_description_file: UploadFile):
    """Saves uploaded files temporarily and extracts their text content."""
    cv_path = f"temp_{cv_file.filename}"
    jd_path = f"temp_{job_description_file.filename}"

    try:
        with open(cv_path, "wb") as buffer:
            buffer.write(await cv_file.read())
        with open(jd_path, "wb") as buffer:
            buffer.write(await job_description_file.read())
        
        logger.info(f"Temporary files created: '{cv_path}', '{jd_path}'")
        
        cv_tool = CVReadTool()
        file_reader = FileReadTool()
        
        cv_text = cv_tool.run(file_path=cv_path)
        job_desc_text = file_reader.run(file_path=jd_path)
        
        return {
            'CV': cv_text,
            'JobDescription': job_desc_text,
            'JobTitlesList': job_titles
        }
    finally:
        if os.path.exists(cv_path):
            os.remove(cv_path)
        if os.path.exists(jd_path):
            os.remove(jd_path)

# --------------------------------------------------------------------------
# API ENDPOINTS (Conversion of your functions)
# --------------------------------------------------------------------------

@app.post("/run/", tags=["Crew Actions"])
async def run_crew_endpoint(
    cv_file: UploadFile = File(..., description="Candidate's CV file."),
    job_description_file: UploadFile = File(..., description="Job Description file.")
):
    """
    Equivalent to your 'run' function. Analyzes a CV against a job description.
    """
    try:
        inputs = await process_inputs_from_files(cv_file, job_description_file)
        logger.info("Kicking off the crew for analysis...")
        result = Hr().crew().kickoff(inputs=inputs)
        return {"status": "success", "result": str(result)}
    except Exception as e:
        logger.error(f"Error in /run/ endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train/", tags=["Crew Actions"])
async def train_crew_endpoint(
    n_iterations: int = Form(..., description="Number of training iterations."),
    filename: str = Form(..., description="Filename for saving training output."),
    cv_file: UploadFile = File(..., description="CV file for training."),
    job_description_file: UploadFile = File(..., description="Job Description for training.")
):
    """
    Equivalent to your 'train' function.
    """
    try:
        inputs = await process_inputs_from_files(cv_file, job_description_file)
        logger.info(f"Starting training for {n_iterations} iterations, output to '{filename}'...")
        Hr().crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        return {"status": "success", "message": "Training completed."}
    except Exception as e:
        logger.error(f"Error in /train/ endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/replay/{task_id}", tags=["Crew Actions"])
async def replay_crew_endpoint(
    task_id: str = Path(..., description="The ID of the task to replay.")
):
    """
    Equivalent to your 'replay' function.
    """
    try:
        logger.info(f"Replaying task with ID: {task_id}")
        result = Hr().crew().replay(task_id=task_id)
        return {"status": "success", "message": f"Replayed task {task_id}", "result": str(result)}
    except Exception as e:
        logger.error(f"Error in /replay/ endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test/", tags=["Crew Actions"])
async def test_crew_endpoint(
    n_iterations: int = Form(..., description="Number of testing iterations."),
    eval_llm: str = Form(..., description="The language model to use for evaluation (e.g., 'gpt-4')."),
    cv_file: UploadFile = File(..., description="CV file for testing."),
    job_description_file: UploadFile = File(..., description="Job Description for testing.")
):
    """
    Equivalent to your 'test' function.
    """
    try:
        inputs = await process_inputs_from_files(cv_file, job_description_file)
        logger.info(f"Starting test for {n_iterations} iterations with eval_llm: {eval_llm}...")
        Hr().crew().test(n_iterations=n_iterations, eval_llm=eval_llm, inputs=inputs)
        return {"status": "success", "message": "Testing completed."}
    except Exception as e:
        logger.error(f"Error in /test/ endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", tags=["Health Check"])
def read_root():
    """Confirms the API is running."""
    return {"status": "HR ATS API is operational"}

# --- To run this file directly ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

