from langchain import LLMChain, PromptTemplate
from langchain.agents import AgentExecutor, ZeroShotAgent

from qabot.data_loader_tool import DuckDBTool


def get_duckdb_data_query_chain(llm, database):
    tool = DuckDBTool(engine=database)

    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad"],
        template=_DEFAULT_TEMPLATE,
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    tool_names = [tool.name]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=[tool],
        verbose=True
    )

    return agent_executor


_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct DuckDB query to run,
then look at the results of the query and return the answer. 
 
Unless the user specifies in their question a specific number of examples to obtain, always limit your query
to at most {top_k} results. You can order the results by a relevant column to return the most interesting 
examples in the database.

Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query
for columns that do not exist. Also, pay attention to which column is in which table.

Use the following format:

Input: "Description of input data here"
Extension: Extension of the input data
Action: the action to take, should be one of [execute]
Action Input: "SQL Query to load data"
Final Answer: Name of table or view that was created

For example:
 
Input: "open test.parquet from the data folder"
Extension: parquet
Action: execute
Action Input: "CREATE TABLE test AS SELECT * FROM 'data/test.parquet';"
Final Answer: test

For example:
 
Input: "import data/records.json as customers"
Extension: json
Action: execute
Action Input: "CREATE table customers AS SELECT * FROM 'data/records.json';"
Final Answer: customers

Another Example:

Input: "create a view of the covid data from "s3://covid19-lake/enigma-jhu-timeseries/csv/jhu_csse_covid_19_timeseries_merged.csv"
Extension: csv
Action: execute
Action Input: "CREATE VIEW covid AS SELECT * FROM 's3://covid19-lake/enigma-jhu-timeseries/csv/jhu_csse_covid_19_timeseries_merged.csv';"
Final Answer: covid

{agent_scratchpad}

Input: {input}"""
