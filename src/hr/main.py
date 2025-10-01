import sys
import warnings
from crewai import Crew
from crewai_tools import FileReadTool
from CVReadTool import CVReadTool
from hr.crew import Hr

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

job_titles = [
    # Software & Development
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Mobile App Developer", "DevOps Engineer", "Software Engineer",
    "Cloud Engineer", "QA Engineer", "Test Automation Engineer",
    "Game Developer", "Embedded Systems Engineer",

    # Data & AI
    "Data Analyst", "Data Scientist", "Machine Learning Engineer",
    "AI Engineer", "Business Intelligence Analyst", "Data Engineer",
    "NLP Engineer", "Computer Vision Engineer",

    # Cybersecurity & IT
    "Cybersecurity Analyst", "Security Engineer", "Ethical Hacker",
    "Penetration Tester", "IT Support Specialist", "Systems Administrator",
    "Network Engineer", "Cloud Security Specialist", "SOC Analyst",

    # Product & Business
    "Product Manager", "Project Manager", "Business Analyst",
    "Scrum Master", "Technical Program Manager", "Operations Manager",
    "Growth Manager",

    # Design & UX
    "UI/UX Designer", "Product Designer", "Graphic Designer",
    "Motion Designer", "Game Designer",

    # Emerging Tech
    "Blockchain Developer", "Web3 Engineer", "AR/VR Developer",
    "Robotics Engineer", "IoT Engineer",

    # Leadership
    "Engineering Manager", "Technical Lead", "Director of Technology",
    "Chief Technology Officer", "Chief Data Officer", "Head of Product"
]

def get_inputs():
    cv_tool = CVReadTool()
    file_reader = FileReadTool()

    cv_path = "C:/Users/abdal/hr/fake_cvs/02_frontend_developer_ali_hassan.txt"
    job_desc_path = "C:/Users/abdal/hr/job_requirements/frontend_developer.txt"

    cv_text = cv_tool._run(file_path=cv_path)
    job_desc_text = file_reader._run(file_path=job_desc_path)

    return {
        'CV': cv_text,
        'JobDescription': job_desc_text,
        'JobTitlesList': job_titles
    }

def run():
    inputs = get_inputs()
    try:
        Hr().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    inputs = get_inputs()
    try:
        Hr().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    try:
        Hr().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    inputs = get_inputs()
    
    try:
        Hr().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
