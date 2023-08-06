import openai
fnsload = """ ╔═══╗╔═╗ ╔╗╔═══╗╔╗     ╔╗  
 ║╔══╝║║╚╗║║║╔═╗║║║     ║║  
 ║╚══╗║╔╗╚╝║║╚══╗║║   ╔╗║╚═╗
 ║╔══╝║║╚╗║║╚══╗║║║ ╔╗╠╣║╔╗║
╔╝╚╗  ║║ ║║║║╚═╝║║╚═╝║║║║╚╝║
╚══╝  ╚╝ ╚═╝╚═══╝╚═══╝╚╝╚══╝
                            
                            
"""
print(fnsload)

def getgpt(tkn, req):
	openai.api_key = tkn
	resp = openai.Completion.create(
		engine="text-davinci-002",
		prompt=req,
		max_tokens=1024,
		n=1,
		stop=None,
		temperature=0.5,
	).get("choices")[0].text
	return resp

def getpass(symb):
	return print('Generating pass, please wait...')

