# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType

from rasa_sdk import Action
from SalesforceDatabase_Connectivity import sf_api_call
import requests
import json

class ActionResourcesList(Action):

    def name(self) -> Text:
        return "action_resources_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        covid_resources = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "Sales Cloud",
                    "subtitle": "Experience :- 3-5 Yrs, Location :- Banglore",
                    "image_url": "https://www.crmwave.com/uploads/6/1/1/8/61183005/8870397_orig.png",
                    "buttons": [{
                            "title": "Apply Now",
                            "type": "postback",
                            "payload": "/apply_now"
                        }
                    ]
                },
                    {
                        "title": "Service Cloud",
                        "subtitle": "Experience :- 3-5 Yrs, Location :- Banglore",
                        "image_url": "https://cloud-elements.com/wp-content/uploads/2018/12/salesforce-service-cloud-logo-600.jpg",
                        "buttons": [{
                                "title": "Apply Now",
                                "type": "postback",
                                "payload": "/apply_now"
                            }
                        ]
                    },
                    {
                        "title": "Community Cloud",
                        "subtitle": "Experience :- 3-5 Yrs, Location :- Banglore",
                        "image_url": "https://cloud4good.com/wp-content/uploads/2016/08/salesforce-community-cloud2.jpg",
                        "buttons": [{
                                "title": "Apply Now",
                                "type": "postback",
                                "payload": "/apply_now"
                            }
                        ]
                    },
                    {
                        "title": "RASA CHATBOT",
                        "subtitle": "Conversational AI",
                        "image_url": "static/rasa.png",
                        "buttons": [{
                            "title": "Rasa",
                            "url": "https://www.rasa.com",
                            "type": "web_url"
                        },
                            {
                                "title": "Rasa Chatbot",
                                "type": "postback",
                                "payload": "/greet"
                            }
                        ]
                    }
                ]
            }
        }

        dispatcher.utter_message(attachment=covid_resources)
        return []


class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["name", "number", "mailid", "position"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:

     sf_api_call('/services/data/v40.0/sobjects/Rasa__c/', method="post", data={
         'First_Name__c': tracker.get_slot("name"),
          'Mobile_No__c':tracker.get_slot("number"),
         'Email__c': tracker.get_slot("mailid")
         })
     dispatcher.utter_message(response="utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Mobile_number=tracker.get_slot("number"),
                                 Email=tracker.get_slot("mailid"),
                                 Position=tracker.get_slot("position"))

     return [SlotSet('name',None),SlotSet('number',None),SlotSet('position',None),SlotSet('mailid',None)]        
