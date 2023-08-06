import openai
import random

fnsload = """ ╔═══╗╔═╗ ╔╗╔═══╗╔╗     ╔╗  
 ║╔══╝║║╚╗║║║╔═╗║║║     ║║  
 ║╚══╗║╔╗╚╝║║╚══╗║║   ╔╗║╚═╗
 ║╔══╝║║╚╗║║╚══╗║║║ ╔╗╠╣║╔╗║
╔╝╚╗  ║║ ║║║║╚═╝║║╚═╝║║║║╚╝║
╚══╝  ╚╝ ╚═╝╚═══╝╚═══╝╚╝╚══╝
                            
                            
"""
print(fnsload)

def getgpt(OpenAI_Token, Request):
	openai.api_key = OpenAI_Token
	try:
		resp = openai.Completion.create(
			engine="text-davinci-002",
			prompt=Request,
			max_tokens=1024,
			n=1,
			stop=None,
			temperature=0.5,
		).get("choices")[0].text
		return print(resp)
	except Exception as e:
		return print(f'Error while connect to openai.\nError: {e}')


#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
