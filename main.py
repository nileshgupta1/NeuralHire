import os
import json

from agents.agents import RecruitmentAgents
from tasks.tasks import RecruitmentTasks
from crewai import Crew

def create_dummy_resumes(num_resumes):
    resumes = []
    for i in range(num_resumes):
        resume = {
            "name": f"Candidate {i+1}",
            "qualifications": ["Qualification 1", "Qualification 2"],
            "experience": ["Experience 1", "Experience 2"],
            "skills": ["Skill 1", "Skill 2"]
        }
        resumes.append(resume)
    return resumes

def create_dummy_job_openings(num_jobs):
    job_openings = {
        "finance": [],
        "tech": [],
        "manufacturing": []
    }
    for i in range(num_jobs):
        job = {
            "title": f"Job {i+1}",
            "company": f"Company {i+1}",
            "location": f"Location {i+1}"
        }
        domain = ["finance", "tech", "manufacturing"][i % 3]
        job_openings[domain].append(job)
    return job_openings

def save_data(resumes, job_openings):
    with open("resumes.json", "w") as f:
        json.dump(resumes, f, indent=2)
    with open("job_openings.json", "w") as f:
        json.dump(job_openings, f, indent=2)

def load_data():
    with open("resumes.json", "r") as f:
        resumes = json.load(f)
    with open("job_openings.json", "r") as f:
        job_openings = json.load(f)
    return resumes, job_openings


num_resumes = 10
num_jobs = 15
resumes = create_dummy_resumes(num_resumes)
job_openings = create_dummy_job_openings(num_jobs)
save_data(resumes, job_openings)

resumes, job_openings = load_data()

recruitment_agents = RecruitmentAgents(use_groq=True)
job_hunter = recruitment_agents.job_hunter_agent()
resume_analyst = recruitment_agents.resume_analyst_agent()
candidate_engagement = recruitment_agents.candidate_engagement_agent()
company_investigator = recruitment_agents.company_investigator_agent()
workflow_orchestrator = recruitment_agents.workflow_orchestrator_agent()

recruitment_tasks = RecruitmentTasks()
job_search_task = recruitment_tasks.job_search(job_hunter)
resume_analysis_task = recruitment_tasks.resume_analysis(resume_analyst)
candidate_outreach_task = recruitment_tasks.candidate_outreach(candidate_engagement)
company_research_task = recruitment_tasks.company_research(company_investigator)
final_matching_task = recruitment_tasks.final_matching(workflow_orchestrator)

# Create crew
recruitment_crew = Crew(
    agents=[job_hunter],
    tasks=[job_search_task],
    verbose=True
)

result = recruitment_crew.kickoff()

print("\n\n########################")
print("## Recruitment Results")
print("########################\n")
print(result)