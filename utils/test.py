import os
from utils.load_config import LoadConfig
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import QuerySQLDatabaseTool
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from sqlalchemy import create_engine

APPCFG = LoadConfig()
print("La dirección de la base de datos es:", APPCFG.sqldb_directory)

def test_sql_query_execution(message: str):
    """
    Función para probar la ejecución de una consulta SQL usando LangChain con SQLite.

    Args:
        message (str): La pregunta que se quiere hacer a la base de datos.

    Returns:
        str: Respuesta generada por la cadena ejecutada.
    """
    # Verificar si la base de datos existe
    if os.path.exists(APPCFG.sqldb_directory):
        try:
            db = SQLDatabase.from_uri(f"sqlite:///{APPCFG.sqldb_directory}")
            print(f"Conectando a la base de datos en: {APPCFG.sqldb_directory}")

            execute_query = QuerySQLDatabaseTool(db=db)
            write_query = create_sql_query_chain(APPCFG.langchain_llm, db)
            print(f"Consulta generada: {write_query}")


            answer_prompt = PromptTemplate.from_template(APPCFG.agent_llm_system_role)
            answer = answer_prompt | APPCFG.langchain_llm | StrOutputParser()

            # Crear la cadena de ejecución
            chain = (
                    RunnablePassthrough.assign(query=write_query).assign(
                        result=itemgetter("query") | execute_query
                    )
                    | answer
            )
            # Invocar la cadena con la consulta
            response = chain.invoke({"question": message})

            # Retornar la respuesta
            return response
        except Exception as e:
            # Manejo de errores si algo falla en la ejecución de la consulta
            return f"Error al ejecutar la consulta: {e}"
    else:
        return "La base de datos SQL no existe. Por favor, crea el 'sqldb.db' primero."


# Ejemplo de mensaje que se quiere hacer a la base de datos
message = "Quiero saber qué zapatos están disponibles"

# Probar la función de ejecución SQL
response = test_sql_query_execution(message)
print("Respuesta de la consulta:", response)


