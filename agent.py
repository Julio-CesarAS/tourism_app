from langchain.llms import OpenAI 
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain
import logging


logging.basicConfig(level=logging.INFO)

        
class agent:
    def __init__(
        self,
        open_ai_api_key,
        model= 'gpt-4o',
        temperature = 0,
        verbose = True
    ):
        
        self.logger = logging.getLogger(__name__)
        if verbose:
            self.logger.setLevel(logging.INFO)
        
        
        self._openai_key = open_ai_api_key
        self.chat_model = ChatOpenAI(model=model,
                                     temperature=temperature,
                                     openai_api_key=self._openai_key)
        self.verbose = verbose
     
        
    def get_attractions(self, request):
        attractions_template = AttractionsTemplate()
        mapping_template = MappingTemplate()
        center_map_template = CenterMapTemplate()
        
        travel_agent = LLMChain(
            llm=self.chat_model,
            prompt=attractions_template.chat_prompt,
            verbose=self.verbose,
            output_key='agent_suggestion'
        )
        
        coordinates_converter = LLMChain(
            llm=self.chat_model,
            prompt=mapping_template.chat_prompt,
            verbose=self.verbose,
            output_key='coordinates'
        )
        
        center_calculation = LLMChain(
            llm=self.chat_model,
            prompt=center_map_template.chat_prompt,
            verbose=self.verbose,
            output_key='center_info'
        )

        overall_chain = SequentialChain(
            chains=[travel_agent,
                    coordinates_converter,
                    center_calculation],
            input_variables=["request"],
            output_variables=["agent_suggestion",
                              "coordinates",
                              "center_info"],
            verbose=self.verbose
        )

        return overall_chain(
            {"request": request},
            return_only_outputs=True
        )
        
print(type(agent))