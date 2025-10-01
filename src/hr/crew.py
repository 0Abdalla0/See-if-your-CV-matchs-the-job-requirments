from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from CVReadTool import CVReadTool

@CrewBase
class Hr():
    agents: List[BaseAgent]
    tasks: List[Task]


    @agent
    def CVReaderAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['CVReaderAgent'],
            tools=[
                CVReadTool(),  
            ],
            verbose=True,
            memory=True,
            output_file='keywords.md'
        )

    @agent
    def JobFittingAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['JobFittingAgent'],
            verbose=True
        )

    @agent
    def AlternativeClassifierAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['AlternativeClassifierAgent'],
            verbose=True
        )

    @agent
    def ReportingAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['ReportingAgent'],
            verbose=True,
            output_file='final_report.md'
        )


    @task
    def CVReader_task(self) -> Task:
        return Task(
            config=self.tasks_config['CVReader_task'],
        )

    @task
    def JobFitting_task(self) -> Task:
        return Task(
            config=self.tasks_config['JobFitting_task'],
        )

    @task
    def AlternativeClassifier_task(self) -> Task:
        return Task(
            config=self.tasks_config['AlternativeClassifier_task'],
        )

    @task
    def Reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['Reporting_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
