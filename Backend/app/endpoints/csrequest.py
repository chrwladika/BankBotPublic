"""
Chat and Request Endpoints

This module defines endpoints for handling chat interactions and customer service requests.

"""

from fastapi import APIRouter, HTTPException, Request, Depends, WebSocket
from pydal import DAL
import json

from models.enum import Roles
from models.user import User
from models.chatdata import ChatData
from services.csrequest_service import get_page_csrequests, get_csrequest_by_id, schedule_call
from services.card_service import lockCard
from typing import List
from fastapi.responses import JSONResponse
from fastapi import WebSocket
from models.csrequest import CSRequest
from config.auth_config import AZURE_KEY
import os
import openai

#openai.api_type = "azure"
#openai.api_base = "Your.azure.instance"
#openai.api_version = "2023-03-15-preview"
openai.api_key = AZURE_KEY

router = APIRouter()

@router.post("/chat/{user_id}")
async def get_response_gpt(request: Request, chat_data: ChatData, user_id: int):

    db: DAL = request.state.db
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "system", "content": """Sie sind BankAssistantGPT, ein großes Sprachmodell, das von OpenAI trainiert wurde. Handeln Sie als professioneller Callcenter-Agent für Ihre Bank, bei der Sie arbeiten. Sie beantworten Fragen von Kunden Ihrer Bank. Sagen Sie mir nicht, dass Sie ein KI-Modell sind. Das weiß ich schon. Gehen Sie einfach wie folgt vor:

 

Lesen Sie den Kontext sorgfältig durch und wenden Sie ihn an. Stellen Sie sicher, dass Sie Ihre Berechnungen und Argumente buchstabieren, damit jeder sie überprüfen kann. Formulieren Sie alles bis ins kleinste Detail und überspringen Sie keinen Schritt! Antworten Sie immer auf Deutsch!

 

Stellen Sie sicher, dass Sie alle Ihre Quellen überprüfen und Nachweise über die Quellen liefern, die Sie zur Generierung Ihrer Antwort verwenden. Verwenden Sie nur den bereitgestellten Kontext. Achten Sie darauf, Halluzinationen im Close-Domain- und Open-Domain-Bereich zu vermeiden. Seien Sie in Ihrer Argumentation und Antwort äußerst sachlich und faktenbasiert. Verwenden Sie Ihr bestes Urteilsvermögen, um festzustellen, ob Ihre Quellen wahrheitsgetreu, sachlich, real und zuverlässig sind. Benutzen Sie für Ihre Begründung und Antwort keine unzuverlässigen und nicht vertrauenswürdigen Quellen. Versuchen Sie immer, Ihre Quellen zu zitieren, wo immer Sie können.

 

Dies ist der Kontext:

 

Sie sind sehr hilfsbereit und wissen alles über Ihre Bank. Sie helfen den Kunden der Bank bei der Lösung ihrer Probleme wie den folgenden:

 

- Kreditkarte sperren
- Kreditkarte stornieren
- Kreditkarte erneuern
- Beantworten Sie häufig gestellte Fragen
- Öffnungszeiten
- Lassen Sie sich vom Bankberater zurückrufen
- allgemeine Informationen über die Bank einholen
- Vereinbaren Sie einen Termin mit einem Bankberater
- Finanzberatung

 

Hier sind einige wichtige Verfahren, die Sie befolgen müssen:

 

Wenn Sie in Ihrem Kontext keine sachliche Antwort finden, sagen Sie einfach: „Ich weiß die Antwort nicht, aber ich kann Sie mit einem Bankberater verbinden.“

 

Lassen Sie uns dies Schritt für Schritt erarbeiten, um sicherzustellen, dass wir die richtige Antwort haben.

 

Antworten Sie immer auf Deutsch!"""},
                  {"role": "user", "content": chat_data.message}],
        functions= [
        {
            "name": "meaningoflife",
            "description": "This function returns the meaning of life",
            "parameters": {
                "type": "object",
                "properties": {
                    "user": {
                        "type": "string",
                        "description": "The name of the user"
                    }
                },
                "required": ["user"]
            }
        },
        {
            "name": "lockCard",
            "description": "This function locks/cancels/disables a card",
            "parameters": {
                "type": "object",
                "properties": {
                    "cardnumber": {
                        "type": "string",
                        "description": "The card number of the card to be locked/canceled/disabled"
                    }
                },
                "required": ["cardnumber"]
            }
        },
        {
            "name": "schedule_call",
            "description": "This function schedules a call with an agent of the bank. It should be used when a customer wants to speak to a human.",
            "parameters": {
                "type": "object",
                "properties": {
                    "request": {
                        "type": "string",
                        "description": "The reason why the call is to be scheduled."
                    },
                    "telephone": {
                        "type": "string",
                        "description": "The client's telephone number where he wants to get called on."
                    }
                },
                "required": ["request", "telephone"]
            }
        },
        {
            "name": "book_appointment",
            "description": "This function books an appointment with an advisor of the bank. This is not a phone call and is to be done in person. For more complicated inquiries appointments are recommended.",
            "parameters": {
                "type": "object",
                "properties": {
                    "request": {
                        "type": "string",
                        "description": "The reason why the call is to be scheduled."
                    },
                    "date": {
                        "type": "string",
                        "description": "The date on which the appointment is to take place."
                    }
                },
                "required": ["request", "date"]
            }
        }
        ],
        function_call="auto",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    function_name = ""
    if response['choices'][0]['message'].get("function_call", None):
        function_name = response['choices'][0]['message']["function_call"]["name"]
        func = globals()[response['choices'][0]['message']["function_call"]["name"]]

        #parsing of args needed
        if response['choices'][0]['message']["function_call"]["name"] == "schedule_call":
            converted_dict = json.loads(response['choices'][0]['message']["function_call"]["arguments"])
            converted_dict["db"]= db
            converted_dict["userID"] = user_id
            converted_dict["category"] = ""
            print(converted_dict)
            output = func(**converted_dict)
        elif response['choices'][0]['message']["function_call"]["name"] == "book_appointment":
            converted_dict = json.loads(response['choices'][0]['message']["function_call"]["arguments"])
            output = str(converted_dict)
            responsetwo = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[{"role": "system", "content": """Sie sind BankAssistantGPT, ein großes Sprachmodell, das von OpenAI trainiert wurde. Handeln Sie als professioneller Callcenter-Agent für Ihre Bank, bei der Sie arbeiten. Sie beantworten Fragen von Kunden Ihrer Bank. Sagen Sie mir nicht, dass Sie ein KI-Modell sind. Das weiß ich schon. Gehen Sie einfach wie folgt vor:
        
         
        
        Lesen Sie den Kontext sorgfältig durch und wenden Sie ihn an. Stellen Sie sicher, dass Sie Ihre Berechnungen und Argumente buchstabieren, damit jeder sie überprüfen kann. Formulieren Sie alles bis ins kleinste Detail und überspringen Sie keinen Schritt! Antworten Sie immer auf Deutsch!
        
         
        
        Stellen Sie sicher, dass Sie alle Ihre Quellen überprüfen und Nachweise über die Quellen liefern, die Sie zur Generierung Ihrer Antwort verwenden. Verwenden Sie nur den bereitgestellten Kontext. Achten Sie darauf, Halluzinationen im Close-Domain- und Open-Domain-Bereich zu vermeiden. Seien Sie in Ihrer Argumentation und Antwort äußerst sachlich und faktenbasiert. Verwenden Sie Ihr bestes Urteilsvermögen, um festzustellen, ob Ihre Quellen wahrheitsgetreu, sachlich, real und zuverlässig sind. Benutzen Sie für Ihre Begründung und Antwort keine unzuverlässigen und nicht vertrauenswürdigen Quellen. Versuchen Sie immer, Ihre Quellen zu zitieren, wo immer Sie können.
        
         
        
        Dies ist der Kontext:
        
         
        
        Sie sind sehr hilfsbereit und wissen alles über Ihre Bank. Sie helfen den Kunden der Bank bei der Lösung ihrer Probleme wie den folgenden:
        
         
        
        - Kreditkarte sperren
        - Kreditkarte stornieren
        - Kreditkarte erneuern
        - Beantworten Sie häufig gestellte Fragen
        - Öffnungszeiten
        - Lassen Sie sich vom Bankberater zurückrufen
        - allgemeine Informationen über die Bank einholen
        - Vereinbaren Sie einen Termin mit einem Bankberater
        - Finanzberatung
        
         
        
        Hier sind einige wichtige Verfahren, die Sie befolgen müssen:
        
         
        
        Wenn Sie in Ihrem Kontext keine sachliche Antwort finden, sagen Sie einfach: „Ich weiß die Antwort nicht, aber ich kann Sie mit einem Bankberater verbinden.“
        
         
        
        Lassen Sie uns dies Schritt für Schritt erarbeiten, um sicherzustellen, dass wir die richtige Antwort haben.
        
         
        
        Antworten Sie immer auf Deutsch!"""},
                          {"role": "user", "content": chat_data.message},
                          {"role": "function", "name": "book_appointment", "content": "{\"output\"}:" + f"\"{output}\"" + "}"},
                          {"role": "system", "content": "Es ist nun deine Aufgabe diesen Termin zu überprüfen. Fall der Termin auf einen Wochentag zwischen 8 und 17 Uhr fällt, dann schreibe dem Nutzer, dass ein Termin mit dem Berater vereinbar wurde. Der Timeslot sollte 1 Stunde betragen. Versuche die Wünsche des Nutzers zu erfüllen und bei zu wenig Infos, entscheide selbst. Falls der Termin außerhalb von 8 bis 17 Uhr ist oder auf ein Wochenende fällt, frage nach einem neuen Termin."}],
                functions= [
                {
                    "name": "meaningoflife",
                    "description": "This function returns the meaning of life",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user": {
                                "type": "string",
                                "description": "The name of the user"
                            }
                        },
                        "required": ["user"]
                    }
                },
                {
                    "name": "lockCard",
                    "description": "This function locks/cancels/disables a card",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "cardnumber": {
                                "type": "string",
                                "description": "The card number of the card to be locked/canceled/disabled"
                            }
                        },
                        "required": ["cardnumber"]
                    }
                },
                {
                    "name": "schedule_call",
                    "description": "This function schedules a call with an agent of the bank. It should be used when a customer wants to speak to a human.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "request": {
                                "type": "string",
                                "description": "The reason why the call is to be scheduled."
                            },
                            "telephone": {
                                "type": "string",
                                "description": "The client's telephone number where he wants to get called on."
                            }
                        },
                        "required": ["request", "telephone"]
                    }
                },
                {
                    "name": "book_appointment",
                    "description": "This function books an appointment with an advisor of the bank. This is not a phone call and is to be done in person. For more complicated inquiries appointments are recommended.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "request": {
                                "type": "string",
                                "description": "The reason why the call is to be scheduled."
                            },
                            "date": {
                                "type": "string",
                                "description": "The date on which the appointment is to take place."
                            }
                        },
                        "required": ["request", "date"]
                    }
                }
                ],
                function_call="auto",
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        else:
            output = func(response['choices'][0]['message']["function_call"]["arguments"])

        if responsetwo != None:
            response = responsetwo
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[{"role": "system", "content": """Sie sind BankAssistantGPT, ein großes Sprachmodell, das von OpenAI trainiert wurde. Handeln Sie als professioneller Callcenter-Agent für Ihre Bank, bei der Sie arbeiten. Sie beantworten Fragen von Kunden Ihrer Bank. Sagen Sie mir nicht, dass Sie ein KI-Modell sind. Das weiß ich schon. Gehen Sie einfach wie folgt vor:
    
     
    
    Lesen Sie den Kontext sorgfältig durch und wenden Sie ihn an. Stellen Sie sicher, dass Sie Ihre Berechnungen und Argumente buchstabieren, damit jeder sie überprüfen kann. Formulieren Sie alles bis ins kleinste Detail und überspringen Sie keinen Schritt! Antworten Sie immer auf Deutsch!
    
     
    
    Stellen Sie sicher, dass Sie alle Ihre Quellen überprüfen und Nachweise über die Quellen liefern, die Sie zur Generierung Ihrer Antwort verwenden. Verwenden Sie nur den bereitgestellten Kontext. Achten Sie darauf, Halluzinationen im Close-Domain- und Open-Domain-Bereich zu vermeiden. Seien Sie in Ihrer Argumentation und Antwort äußerst sachlich und faktenbasiert. Verwenden Sie Ihr bestes Urteilsvermögen, um festzustellen, ob Ihre Quellen wahrheitsgetreu, sachlich, real und zuverlässig sind. Benutzen Sie für Ihre Begründung und Antwort keine unzuverlässigen und nicht vertrauenswürdigen Quellen. Versuchen Sie immer, Ihre Quellen zu zitieren, wo immer Sie können.
    
     
    
    Dies ist der Kontext:
    
     
    
    Sie sind sehr hilfsbereit und wissen alles über Ihre Bank. Sie helfen den Kunden der Bank bei der Lösung ihrer Probleme wie den folgenden:
    
     
    
    - Kreditkarte sperren
    - Kreditkarte stornieren
    - Kreditkarte erneuern
    - Beantworten Sie häufig gestellte Fragen
    - Öffnungszeiten
    - Lassen Sie sich vom Bankberater zurückrufen
    - allgemeine Informationen über die Bank einholen
    - Vereinbaren Sie einen Termin mit einem Bankberater
    - Finanzberatung
    
     
    
    Hier sind einige wichtige Verfahren, die Sie befolgen müssen:
    
     
    
    Wenn Sie in Ihrem Kontext keine sachliche Antwort finden, sagen Sie einfach: „Ich weiß die Antwort nicht, aber ich kann Sie mit einem Bankberater verbinden.“
    
     
    
    Lassen Sie uns dies Schritt für Schritt erarbeiten, um sicherzustellen, dass wir die richtige Antwort haben.
    
     
    
    Antworten Sie immer auf Deutsch!"""},
                          {"role": "user", "content": chat_data.message},
                          {"role": "function", "name": function_name, "content": "{\"status\"}:" + f"\"{output}\"" + "}"}],
                functions = [
                    {
                        "name": "meaningoflife",
                        "description": "This function returns the meaning of life",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user": {
                                    "type": "string",
                                    "description": "The name of the user"
                                }
                            },
                            "required": ["user"]
                        }
                    },
                    {
                        "name": "lockCard",
                        "description": "This function locks/cancels/disables a card",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "cardnumber": {
                                    "type": "string",
                                    "description": "The card number of the card to be locked/canceled/disabled"
                                }
                            },
                            "required": ["cardnumber"]
                        }
                    },
                    {
                        "name": "schedule_call",
                        "description": "This function schedules a call with an agent of the bank. It should be used when a customer wants to speak to a human.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "request": {
                                    "type": "string",
                                    "description": "The reason why the call is to be scheduled."
                                },
                                "telephone": {
                                    "type": "string",
                                    "description": "The client's telephone number where he wants to get called on."
                                }
                            },
                            "required": ["request", "telephone"]
                        }
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

    return JSONResponse(content={"response": str(response['choices'][0]['message']['content'])}, status_code=200)

def meaningoflife(user):
    """
    Get the meaning of life for a user.

    Args:
        user (str): User's name.

    Returns:
        str: Meaning of life for the user.
    """
    return f"the meaning of {user}'s life is {user}"

def book_appointment(args):
    return str(args)

@router.post("/csrequest/")
async def create_csrequest(request: Request, csrequest: CSRequest):
    """
            Create a customer service request.

            Args:
                csrequest (CSRequest): CSRequest object containing request details.
                request (Request): FastAPI request.

            Returns:
                JSONResponse: CSRequest creation status.
            """
    db: DAL = request.state.db

    # call service for validation of training here

    csrequest_id = db.training.insert(**(csrequest.dict()))

    return JSONResponse(content={"detail": "CSRequest created successfully under id {}".format(str(csrequest_id))},
                        status_code=201)


@router.get("/csrequestpage/")
async def get_page_csrequest(request: Request, page: int = 1, category: str = ""):
    """
        Get a page of customer service requests.

        Args:
            request (Request): FastAPI request.
            page (int): Page number.
            page_size (int): Number of requests per page.

        Returns:
            JSONResponse: Page of CSRequests.
    """
    db: DAL = request.state.db

    page = get_page_csrequests(db, page, category)

    return JSONResponse(content={"page": page.dict()}, status_code=200)


@router.get("/csrequest/{id}")
async def get_csrequest(request: Request, id: int):
    """
        Get a customer service request by ID.

        Args:
            request (Request): FastAPI request.
            id (int): Request ID.

        Returns:
            JSONResponse: CSRequest details.
        """
    db: DAL = request.state.db

    csrequest = get_csrequest_by_id(db, id)

    if csrequest is None:
        return JSONResponse(content={"csrequest": csrequest}, status_code=404)

    return JSONResponse(content={"csrequest": csrequest}, status_code=200)




@router.get("/appointments/")
async def get_appointments():
    """
        Get appointments data.

        Returns:
            JSONResponse: Appointments data.
        """
    return JSONResponse(content={"data":""}, status_code=200)