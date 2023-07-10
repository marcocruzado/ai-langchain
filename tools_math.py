import os
import openai
from dotenv import load_dotenv
load_dotenv()
from langchain import OpenAI
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool

#configurar su api key
openai.api_key = os.environ.get("OPENAI_API_KEY", "")
os.environ["LANGCHAIN_TRACING"] = "true"


class OperacionesMatematicas(BaseTool):
    name = "operaciones_matematicas"
    description = "Usa esto cuando nesesites cualquier operacion matematica"
    #definimos el metodo run
    def _run(a: float , b: float, run_manager: Optional[CallbackManagerForToolRun] = None) -> float:
        return a*b
    
    async def _arun(a: float , b: float, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> float:
        return a*b