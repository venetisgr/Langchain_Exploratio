from tools.tools import get_linkedin_profile_url#, get_profile_url_w_occupation

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

from key_storage import key_dict

def linkedin_url_lookup(name: str, occupation:str=None) -> str:

    """For the provided name and perhaps occupation, it will try to find the matching linkedin profile"""

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",openai_api_key = key_dict["OPENAI_API_KEY"],)

    if occupation==None:
        
        template = """given the full name {name_of_person} I want you to get it me a URL to their Linkedin profile page.
                          Your answer should contain only a URL. If you cannot find the URL return "not found". """
        tools_for_agent1 = [
            Tool(
                name="Crawl Google for linkedin profile page",
                func=get_linkedin_profile_url,
                description="returns google search results for a name search,in order to find the associated Linkedin Page URL for that name",
            )]

        agent = initialize_agent(tools_for_agent1, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True ) #verbose helps us see the reasoning and the subtasks the llm have made      

        prompt_template = PromptTemplate(input_variables=["name_of_person"], template=template)

        linkedin_username = agent.run(prompt_template.format_prompt(name_of_person=name))

    else:

        template = """given the full name {name_of_person} and occupation {occupation} I want you to get it me a URL to their Linkedin profile page.
                          Your answer should contain only a URL. If you cannot find the URL return "not found". """
        tools_for_agent1 = [
            Tool(
                name="Crawl Google for linkedin profile page",
                func=get_linkedin_profile_url,
                description="""returns google search results for a name and an occupation search ,in order to find the associated Linkedin Page URL for that name
                The input to this tool should be a string with a comma between name and occupation, this represents the two inputs you want to use. For example, `Tony Stark, Avengers` would be an example input.""",
            )]

        agent = initialize_agent(tools_for_agent1, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True ) #verbose helps us see the reasoning and the subtasks the llm have made      

        prompt_template = PromptTemplate(input_variables=["name_of_person", "occupation"], template=template)

        linkedin_username = agent.run(prompt_template.format_prompt(name_of_person=name,occupation=occupation))

    

    return linkedin_username