from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from crewai_tools import MySQLSearchTool
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import json

load_dotenv()

serp_tool = SerperDevTool(
    search_url="https://docs.crewai.com/",
    n_results=2,
)
# json_data = json.dumps(serp_tool.run(search_query="SerperDevTool"))
# print(json_data)
@CrewBase
class CrewaiSolutionForPaymentSanctionAutomationCrew():
    """CrewaiSolutionForPaymentSanctionAutomation crew"""

    # @agent
    # def internal_system_validator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['internal_system_validator'],
    #         tools=[MySQLSearchTool()],
    #     )

    # @agent
    # def sanctions_watchlist_checker(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['sanctions_watchlist_checker'],
    #         tools=[SerperDevTool()],
    #     )

    @agent
    def public_info_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['public_info_researcher'],
            tools=[serp_tool],
        )

    # @agent
    # def kyc_verifier(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['kyc_verifier'],
    #         tools=[MySQLSearchTool()],
    #     )

    # @agent
    # def level_3_investigator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['level_3_investigator'],
    #         tools=[],
    #     )


    # @task
    # def validate_internal_system_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['validate_internal_system_task'],
    #         tools=[MySQLSearchTool()],
    #     )

    # @task
    # def check_sanctions_watchlist_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['check_sanctions_watchlist_task'],
    #         tools=[SerperDevTool()],
    #     )

    @task
    def research_public_info_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_public_info_task'],
            tools=[serp_tool],
        )

    # @task
    # def verify_kyc_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['verify_kyc_task'],
    #         tools=[MySQLSearchTool()],
    #     )

    # @task
    # def conduct_level_3_investigation_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['conduct_level_3_investigation_task'],
    #         tools=[],
    #     )


    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiSolutionForPaymentSanctionAutomation crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
