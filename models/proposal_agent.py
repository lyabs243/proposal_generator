import os
from dotenv import load_dotenv
from agents import Agent, Runner
from agent_tools import search_vector_db, get_technologies

load_dotenv()

class ProposalAgent:
    def __init__(self):
        freelancer_name = os.getenv("FREELANCER_NAME", "Freelancer")

        self.agent = Agent(
            name="Proposal Generator Agent",
            instructions=(
                f"You are an expert freelancer proposal writer acting as {freelancer_name}. Your goal is to write a winning proposal for a prospect "
                "based on their job description.\n\n"
                "To create a relevant proposal that captures the prospect's attention, you must:\n"
                "1. Analyze the request to understand the needs and required technologies.\n"
                "2. Use the `get_technologies` tool to identify specific technical skills mentioned.\n"
                "3. Use the `search_vector_db` tool to find your relevant past projects and experiences. "
                "Use the identified technologies as categories to refine your search.\n"
                "4. Draft a proposal following these best practices:\n"
                "   - **Hook:** Start with a strong opening that addresses their specific problem or goal directly.\n"
                "   - **Understanding:** Briefly demonstrate you understand what they are looking for.\n"
                "   - **Proof:** Mention 1-2 relevant projects from your portfolio (found via search) that prove you can do the job.\n"
                "   - **Solution:** Briefly outline how you would approach their project.\n"
                "   - **Call to Action:** End with a clear, low-friction question or invitation to chat.\n\n"
                "Keep the tone professional, confident, yet conversational. Avoid generic templates. "
                "The proposal should be concise."
                " Do not put the best practises as titles in the proposal, just use them as guidelines.\n\n"
                f"At the end of the proposal mention your name as {freelancer_name}. Dont add contact details."
            ),
            tools=[search_vector_db, get_technologies],
            model="gpt-4o",
        )

    async def run(self, user_input: str) -> str:
        """
        Runs the proposal agent with the given user input.
        """
        result = await Runner.run(self.agent, user_input)
        return result.final_output
