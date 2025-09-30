# Create a folder of 10 job requirement files (JSON + human-readable Markdown) for the same tech roles,
# plus a machine-readable "matching rules" JSON that you can use to programmatically test CVs.
import os
import json
import datetime

out_dir = "/mnt/data/job_requirements"
os.makedirs(out_dir, exist_ok=True)

roles = [
    {
        "id": "software_engineer",
        "title": "Software Engineer",
        "years_experience_min": 3,
        "must_have": ["Python or Java", "REST API design", "SQL", "Git"],
        "nice_to_have": ["Docker", "Kubernetes", "AWS", "Microservices", "CI/CD"],
        "degree": "BSc in Computer Science or equivalent",
        "responsibilities": [
            "Design, implement and maintain backend services",
            "Participate in code reviews and mentoring",
            "Collaborate with product and QA to deliver features"
        ],
        "keywords": ["python","java","spring","flask","rest","api","postgresql","mysql","docker","kubernetes","aws","microservices","ci/cd","github actions"]
    },
    {
        "id": "frontend_developer",
        "title": "Frontend Developer",
        "years_experience_min": 2,
        "must_have": ["HTML/CSS", "JavaScript (ES6+)", "React or Vue"],
        "nice_to_have": ["TypeScript", "Accessibility (WCAG)", "Performance optimization", "Unit testing"],
        "degree": "BSc in Software Engineering or equivalent",
        "responsibilities": [
            "Implement responsive, accessible UIs",
            "Create reusable UI components and stories",
            "Work with designers to polish UX"
        ],
        "keywords": ["react","vue","javascript","typescript","html","css","tailwind","next.js","vite","webpack","lighthouse","accessibility","jest","rtl"]
    },
    {
        "id": "backend_developer",
        "title": "Backend Developer",
        "years_experience_min": 3,
        "must_have": ["Server-side language (Node.js/Go/Java/Python)", "Databases (SQL or NoSQL)", "RESTful API design"],
        "nice_to_have": ["Message queues (Kafka/RabbitMQ)", "Terraform", "Monitoring/metrics"],
        "degree": "BSc in Computer Science or equivalent",
        "responsibilities": [
            "Build and maintain server-side services",
            "Optimize DB queries and design schemas",
            "Ensure reliability and observability"
        ],
        "keywords": ["node","go","express","gin","sql","mongodb","kafka","redis","docker","postgresql","terraform","ci/cd"]
    },
    {
        "id": "data_scientist",
        "title": "Data Scientist",
        "years_experience_min": 2,
        "must_have": ["Python", "pandas", "scikit-learn", "SQL"],
        "nice_to_have": ["XGBoost", "Deep learning", "Airflow", "model deployment experience"],
        "degree": "BSc in Statistics/CS/Math or equivalent",
        "responsibilities": [
            "Build predictive models and run experiments",
            "Perform feature engineering and analysis",
            "Deploy and monitor models in production"
        ],
        "keywords": ["python","pandas","scikit-learn","xgboost","tensorflow","pytorch","sql","airflow","etl","feature engineering","a/b testing"]
    },
    {
        "id": "ml_engineer",
        "title": "Machine Learning Engineer",
        "years_experience_min": 3,
        "must_have": ["Python", "PyTorch or TensorFlow", "Model deployment (Docker/Serving)"],
        "nice_to_have": ["ONNX", "CUDA", "MLflow", "Edge optimization"],
        "degree": "MSc preferred (or proven experience)",
        "responsibilities": [
            "Train and optimize ML models",
            "Build scalable inference pipelines",
            "Collaborate with data scientists and engineers"
        ],
        "keywords": ["pytorch","tensorflow","onnx","cuda","mlflow","fastapi","torchscript","docker","kubernetes","inference"]
    },
    {
        "id": "devops_engineer",
        "title": "DevOps Engineer",
        "years_experience_min": 3,
        "must_have": ["Terraform or CloudFormation", "Kubernetes or Docker", "CI/CD pipelines"],
        "nice_to_have": ["Prometheus/Grafana", "AWS/GCP/Azure", "Ansible"],
        "degree": "BSc in Computer Science or equivalent",
        "responsibilities": [
            "Manage IaC and cloud infrastructure",
            "Automate deployments and observability",
            "Improve reliability and incident response"
        ],
        "keywords": ["terraform","kubernetes","docker","jenkins","github actions","aws","gcp","ansible","prometheus","grafana","helm"]
    },
    {
        "id": "product_manager",
        "title": "Product Manager (Tech)",
        "years_experience_min": 2,
        "must_have": ["Product roadmap experience", "Stakeholder communication", "Data-driven decision making"],
        "nice_to_have": ["A/B testing", "SQL or analytics tools", "SaaS experience"],
        "degree": "Degree in CS, Business, or equivalent experience",
        "responsibilities": [
            "Define product vision and roadmap",
            "Coordinate cross-functional teams",
            "Measure success and iterate"
        ],
        "keywords": ["roadmap","product management","a/b testing","mixpanel","amplitude","jira","user research","stakeholder"]
    },
    {
        "id": "uxui_designer",
        "title": "UX/UI Designer",
        "years_experience_min": 2,
        "must_have": ["Figma or Sketch", "Prototyping", "User research"],
        "nice_to_have": ["Design systems", "Front-end basics (HTML/CSS)"],
        "degree": "Degree in Design or related field",
        "responsibilities": [
            "Design user-centered interfaces and prototypes",
            "Conduct usability testing and research",
            "Maintain design system"
        ],
        "keywords": ["figma","sketch","prototyping","usability testing","design system","ux research","adobe xd"]
    },
    {
        "id": "qa_engineer",
        "title": "QA Engineer",
        "years_experience_min": 2,
        "must_have": ["Test automation (Selenium/Playwright)", "Test plan creation", "Bug tracking tools"],
        "nice_to_have": ["Performance testing (JMeter)", "API testing (Postman)"],
        "degree": "Degree in CS or related field",
        "responsibilities": [
            "Create and maintain automated test suites",
            "Plan and execute manual and exploratory tests",
            "Report and track defects"
        ],
        "keywords": ["selenium","playwright","postman","jmeter","testrail","test automation","ci/cd","pytest"]
    },
    {
        "id": "sre_engineer",
        "title": "Site Reliability Engineer (SRE)",
        "years_experience_min": 3,
        "must_have": ["Linux systems", "SLOs/SLIs and monitoring", "Kubernetes or orchestration"],
        "nice_to_have": ["Chaos engineering", "Capacity planning", "Distributed systems"],
        "degree": "BSc in Computer Science or equivalent",
        "responsibilities": [
            "Define and measure reliability targets",
            "Automate incident response and runbooks",
            "Improve system scalability and resilience"
        ],
        "keywords": ["slo","sli","kubernetes","prometheus","grafana","linux","ansible","chaos engineering","capacity planning"]
    },
]

# Write JSON and Markdown versions
for r in roles:
    json_path = os.path.join(out_dir, f"{r['id']}.json")
    md_path = os.path.join(out_dir, f"{r['id']}.md")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(r, f, indent=2)
    md_content = f"# {r['title']}\n\n" + \
                 f"**Minimum years experience:** {r['years_experience_min']}\n\n" + \
                 f"**Required:**\n\n" + "\n".join([f"- {x}" for x in r['must_have']]) + "\n\n" + \
                 f"**Nice to have:**\n\n" + "\n".join([f"- {x}" for x in r['nice_to_have']]) + "\n\n" + \
                 f"**Degree:** {r['degree']}\n\n" + \
                 f"**Responsibilities:**\n\n" + "\n".join([f"- {x}" for x in r['responsibilities']]) + "\n\n" + \
                 f"**Keywords for automated matching:**\n\n" + ", ".join(r['keywords']) + "\n"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

# Create a matching_rules.json that gives a simple scoring algorithm suggestion
matching_rules = {
    "description": "Simple matching rules to score a CV against a job requirement.\nScoring suggestion:\n- +3 points for each 'must_have' skill found (match by keyword)\n- +1 point for each 'nice_to_have' found\n- +2 points if years_experience >= years_experience_min\n- +2 points if degree matches or is close\n- Normalize score to percentage by dividing by maximum possible and multiplying by 100\n",
    "algorithm": {
        "must_have_weight": 3,
        "nice_to_have_weight": 1,
        "experience_weight": 2,
        "degree_weight": 2
    },
    "notes": "Match keywords case-insensitively. Keywords lists are included in each job JSON under 'keywords'."
}
with open(os.path.join(out_dir, "matching_rules.json"), "w", encoding="utf-8") as f:
    json.dump(matching_rules, f, indent=2)

# README
readme = f"""Job Requirements package
Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

Contents:
- 10 job requirement files (JSON) and corresponding human-readable Markdown files.
- matching_rules.json: a suggested scoring algorithm and notes to help you build an automated tester.

Usage ideas:
- Use the JSON files to build a script that parses CV text, looks for keywords, compares years of experience and degree, and computes a match score using matching_rules.json.
- The 'keywords' field provides many tokens you can search the CVs for. Use case-insensitive matching and allow simple stemming (e.g., 'docker' matches 'Docker').

Notes:
- These are templates for testing only. Adjust weights and rules to match your hiring policy.
"""
with open(os.path.join(out_dir, "README.txt"), "w", encoding="utf-8") as f:
    f.write(readme)

print(f"✅ Job requirements package created at: {out_dir}")