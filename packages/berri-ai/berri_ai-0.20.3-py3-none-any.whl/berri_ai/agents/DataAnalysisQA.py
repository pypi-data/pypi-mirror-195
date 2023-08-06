from llama_index import PromptHelper, SimpleWebPageReader, GPTSimpleVectorIndex, GPTListIndex, GPTTreeIndex
import os
import requests
import uuid
import json
import base64
from pathlib import Path
from llama_index import download_loader 
from llama_index.readers.file.tabular_parser import CSVParser
from langchain.agents import initialize_agent, Tool
from langchain import OpenAI
from llama_index import Document
from langchain import PromptTemplate
import re
from langchain.chains import LLMChain
import asyncio
import pandas as pd
import fuzzywuzzy
from fuzzywuzzy import process
import numpy as np
from berri_ai.agents.DataAnalysisPrompt import PANDAS_CHAIN_DEFAULT_PROMPT
from berri_ai.search_strategies.bm25.DocStore_CSV import DocStore
from berri_ai.ComplexInformationQA import ComplexInformationQA
import os 
os.environ["OPENAI_API_KEY"] = "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"

class DataAnalysisQA:
    def __init__(self,
               df,
               openai_api_key,
               additional_functions=None,
               additional_descriptions=None):
      self.df = df
      self.openai_api_key = openai_api_key
      if additional_functions != None and additional_descriptions != None and len(
          additional_functions) == len(additional_descriptions):
        self.additional_functions = additional_functions
        self.additional_descriptions = additional_descriptions
      self.unique_values = []
      for column in self.df.columns: 
        unique_val = self.df[column].unique().ravel()
        self.unique_values.extend(unique_val)

    def likely_col(self, keywords):
      output = ""
      if len(keywords) > 1:
        output += ". These are the keywords from the user's query: " + ' '.join(keywords)
      
      for keyword in keywords: 
        # List of tuples containing the similarity score and the string
        scores = process.extract(keyword, self.unique_values) # use fuzzymatching to find similar words in list
    
        # Sort the list of tuples by similarity score
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Get the string in the column with the highest similarity
        most_similar_string = sorted_scores[0][0]
    
        # Get the column index for the string with the highest similarity
        most_similar_column_index = self.df.columns[self.df.isin([most_similar_string]).any()].tolist()[0] 
        output_str =  '. When the user says ' + keyword + ' most likely they mean: ' + most_similar_string + ' and the column containing it is: ' + most_similar_column_index
        output += output_str
      return output

    def keyword_extractor(self, query_str):
      llm = OpenAI(temperature=0.7)
      prefix = """A user is asking questions about a spreadsheet. Extract the keywords from the user query that might make sense as names of columns or values in a spreadsheet. If you are not certain, say 'I am not certain', do not make things up. If there are multiple keywords, separate them with a comma (,).
    \n
    User Query: Top cat5 by YoY
    Keywords: cat5, YoY 
    \n
    User Query: How many sku's do we have for variant handles?
    Keywords: sku, variant handle 
    \n
    User Query: Top cat5 by YoY that is very low competition
    Keywords: cat5, YoY, very low competition
    \n
    User Query: """
      input = prefix + query_str 
      input += "\n Keywords: "
      return llm(input)

    def check_if_col_or_not(self, user_query):
      # use llm to get keywords 
      keywords = self.keyword_extractor(user_query)
      keywords = keywords.split(",")
      updated_query = user_query
      # use fuzzy match to compare keyword in keywords to column names and see if there's a likely match
      values = []
      for keyword in keywords: 
        # List of tuples containing the similarity score and the string
        scores = process.extract(keyword, self.df.columns.unique().ravel())
    
        # Sort the list of tuples by similarity score
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        if int(sorted_scores[0][1]) < 85: # if the keyword match is below 85/100, then it's probably a value inside a column, and not a column name.
          values.append(keyword.strip())
        elif int(sorted_scores[0][1]) >= 90:
          updated_query += '. When the user says ' + keyword + ' they are most likely referring to this column: ' + sorted_scores[0][0] + '.'
        print("sorted_scores: ", sorted_scores)
        # Get the string in the column with the highest similarity
        most_similar_string = sorted_scores[0][0]
        print(keyword, most_similar_string)
      return updated_query, values

    def pandas_chain(self, user_query, sheet_col_names):
      prompt_template = PANDAS_CHAIN_DEFAULT_PROMPT
      prompt = PromptTemplate(
        input_variables=["sheet_col_names", "user_query"],
        template=prompt_template)
      
      formatted_prompt = prompt.format(sheet_col_names = sheet_col_names, user_query = user_query)
      llm = OpenAI(temperature=0.7, best_of=3)
      pd_output = llm(formatted_prompt)
      return pd_output

    def conditional_search(self, query):
      sheet_col_names = ", ".join([col for col in self.df.columns])
      pd_output = self.pandas_chain(user_query=query,
                                    sheet_col_names=sheet_col_names)
      # extract pandas expression
      if "Final Pandas Expression" in pd_output:
        # run eval
        print(pd_output)
        pandas_expression = pd_output.split("Final Pandas Expression:")[1].strip()
        match = re.search("(?:`)?df(.*)", pandas_expression).group(1)
        if match:
          match = match.replace("df", "self.df")
          df_expression = "self.df" + match
          print("df_expression: ", df_expression)
          value = eval(df_expression)
          return (value, pd_output)
        else:
          return pd_output
      else:
        return pd_output

    def query(self, user_input: str):
      # check if column or not 
      user_input, values = self.check_if_col_or_not(user_input)
      print(values)
      for value in values: 
        if "I am not certain" in value:
          return {"response": "I am not certain, could you rephrase that?", "references": "I checked if your question had keywords that either belonged to a column or could possibly be a value in the spreadsheet"}
      likely_columns = ""
      if len(values) > 0:
        likely_columns = self.likely_col(values)
        print("likely columns: ", likely_columns)
      # pass in query + context into conditional search and get answer
      final_input_str = user_input + "." + likely_columns
      print("final_input_str: ", final_input_str)
      output = self.conditional_search(final_input_str)
      if len(output) == 2: 
        response = output[0]
        references = "I think the keywords mentioned were: " + ",".join(values) + ". And my final input into the pandas expression model was: " + final_input_str + ". And this is what the model came up with: " + output[1]
      return {"response": response, "references": references}