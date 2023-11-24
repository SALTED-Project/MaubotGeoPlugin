
from maubot import Plugin, MessageEvent
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from mautrix.types import EventType
from typing import Type
from maubot.handlers import command, event
import requests


from os import path

from io import BytesIO
import jmespath
import geopy.distance
from requests.structures import CaseInsensitiveDict
from requests.models import Response

BASE_PATH = path.dirname(path.realpath(path.realpath(__file__)+"/.."))



class Config(BaseProxyConfig):

    """ Plugin configuration
    """
    
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        """ Update configuration settings
        Configuration file `base-config.yaml` is in the main directory of this project.
        This method is used to register all settings.
        """
        helper.copy("publish_service_entities")
        helper.copy("max_distance")
        
       

class GeoBot(Plugin):
    """ Geo Bot, that uses the right before sent message into the room to extract geo information.
    """


    config: Config    

    @classmethod
    def get_config_class(cls) -> Type[Config]:
        return Config

    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    last_messages = {}
    
    @event.on(EventType.ROOM_MESSAGE)
    async def message_handler(self, event: MessageEvent) -> None:
        try:
            self.last_messages[event.room_id] = event.content.geo_uri  
        except:
            print("No location could be extracted from the last message sent in this room.")
    
    
    @command.new(name="help", require_subcommand=False)
    async def help_command(self, event: MessageEvent) -> None:
        """ This method (`!help`) sends helpful information to the chatroom
        """

        answer = f"<h2>Possible commands:</h2>"
        answer += f"<table>"
        answer += f"<tr><td><strong>!location</strong></td><td>Get all organizations, and their Agenda Analytics KPI, near the previously posted location.</td></tr>"
        answer += f"</table>"
        
        await event.respond(answer,allow_html=True)
    
    
    @command.new(name="hello", require_subcommand=False)
    async def hello_get(self, event: MessageEvent) -> None:
        """ This method (`!hello`) says hello 
        """
        
        await event.respond("Hello, I am a bot. I'm delighted that you're talking to me. I can tell you what organizations are in my background property graph near the previously posted location. Need help addressing me with commands? Use !help)")
        
        
    @command.new(name="location", require_subcommand=False)
    async def get_location(self, event: MessageEvent) -> None:
        await event.respond("Hello, I will get the location you just posted and process it, to help you further! This is what i got:")
        try:
            if event.room_id in self.last_messages:            
                # set max distance  
                
                
                try:
                    last_geo_uri = self.last_messages[event.room_id]
                    # for fixed location sharing: last_geo_uri = "geo:49.38009801791189,8.6791740144996"
                    # for live location sharing: last_geo_uri = "geo:49.3798276,8.6792076;u=20.0"

                    # remove "geo:""
                    last_geo_uri = last_geo_uri.removeprefix('geo:')
                    # remove additional info given, when live location is shared
                    last_geo_uri = last_geo_uri.split(';')[0]
                    # divide into lat and long
                    lat, long = last_geo_uri.split(',')
                    answer = f"... I got the following coordiantes from you: lat {lat} and long {long}"
                    await event.respond(answer)           
                except:
                    answer = "I'm sorry, but I could not extract any information about your location from the last post in this chat. Are you sure you shared your location, befor you gave me the !location command?"
                    await event.respond(answer)        
                    # end function call
                    return  
            
                
                try:
                    # get all organization entities                    
                    api_url = self.config['publish_service_entities'] + "/Organization"
                    headers = CaseInsensitiveDict()
                    headers["Accept"] = "application/json"
                    headers["Content-Type"] = "application/json"            

                    r_invoke:Response = requests.get(
                        api_url,
                        headers=headers
                    )
                    json_entities = r_invoke.json()                
                    broker_answer0 = f"My request to scorpio broker was successful. I am processing the results received and will see if there is something for you. This my take a second, since I have to evaluate {len(json_entities)} obtained organizations. "
                    await event.respond(broker_answer0)     
                
                except:
                    broker_answer0 = "My request to scorpio broker was not successful. Maybe try it again later, or contact the support team at team@agenda-analytics.eu \U0001F635"
                    await event.respond(broker_answer0)   
                    # end function call
                    return         

                try:
                    # check if returned entities are within a range of X km to the before posted location                    
                    near_entities=[]
                    for result in json_entities:
                        # extract lat_result and long_result
                        result_lat = jmespath.search('location.value.coordinates[0]', result)
                        result_long = jmespath.search('location.value.coordinates[1]', result)
                        coords_1 = (result_lat, result_long)
                        coords_2 = (lat, long)
                        dist = geopy.distance.geodesic(coords_1, coords_2).km
                        if dist < int(self.config["max_distance"]):
                            near_entities.append(result)
                    if len(near_entities) == 0:
                        answer = f"I found {len(near_entities)} organizations within the {self.config['max_distance']} km range of you. Try again at another location :)."
                        await event.respond(answer)  
                        # end function call
                        return
                    else:
                        answer = f"I found {len(near_entities)} organization(s) within the {self.config['max_distance']} km range of you. I will now try to get you additional info from the broker..."
                        await event.respond(answer)  
                except:
                    answer = "I'm sorry, I have a problem evaluating the results I got. Maybe try it again later, or contact the support team at team@agenda-analytics.eu \U0001F635"
                    await event.respond(answer)   
                    # end function call
                    return  


                try:
                    # get all related kpi entities
                    api_url =  self.config['publish_service_entities'] + "/KeyPerformanceIndicator"
                    headers = CaseInsensitiveDict()
                    headers["Accept"] = "application/json"
                    headers["Content-Type"] = "application/json"            

                    r_invoke:Response = requests.get(
                        api_url,
                        headers=headers
                    )
                    json_kpis = r_invoke.json()

                    broker_answer1 = f"My requests to scorpio broker was successful. This may take a second, since I have to analyse {len(json_kpis)} obtained KeyPerformanceIndicator entities. "
                    await event.respond(broker_answer1)     
                except:
                    broker_answer1 = "My request to scorpio broker was not successful. Maybe try it again later, or contact the support team at team@agenda-analytics.eu \U0001F635"
                    await event.respond(broker_answer1)   
                    # end function call
                    return      
                
                
                # filter out all relevant KPI entities
                result_list = []
                for entity in near_entities:
                    # extract lat_result and long_result
                    entity_id = entity["id"]
                    # # debug log
                    # await event.respond(f"This is the entity: {entity}")
                    # # debug log
                    # await event.respond(f"Those are the fitting KPIs: {[kpi for kpi in json_kpis if jmespath.search('organization.value', kpi) == entity_id]}")
                    result_list.append([entity, [kpi for kpi in json_kpis if jmespath.search('organization.value', kpi) == entity_id]])
                    # debug log
                    # await event.respond(str([entity, [kpi for kpi in json_kpis if jmespath.search('organization.value', kpi) == entity_id]]))         
                
                try:
                    # create results table
                    answer = f"<h2>Nearby organizations (max. distance = {self.config['max_distance']} km):</h2>"
                    answer += "<table><tr><th>#</th><th>Organization</th><th>KPIs</th></tr>"
                    for i,result in enumerate(result_list):    
                        await event.respond(result[0]['name']['value'])
                        await event.respond(str(result[1]))                              
                        answer += "<tr>"
                        answer += f"<td>{i}.</td>"
                        try:
                            answer += f"<td>{result[0]['name']['value']}</td>"
                        except KeyError:
                            answer += "<td>extracting error</td>"
                        try:
                            answer += f"<td>{str(result[1])}</td>"
                        except IndexError:
                            answer += "<td>nothing found</td>"
                        answer += "</tr>"
                    answer += "</table>"
                    await event.respond(answer,allow_html=True)
                            
                except:
                    # create results table
                    answer = f"<h2>Nearby organizations (max. distance = {self.config['max_distance']} km):</h2>"
                    answer += "<table><tr><th>#</th><th>Organization</th><th>KPIs</th></tr>"
                    answer += "<tr>"
                    answer += "<td>-</td>"
                    answer += "<td>error</td>"
                    answer += "<td>-</td>"
                    await event.respond(answer,allow_html=True)
                

            else:
                answer = "... nothing. I'm really sorry, but your last message does not contain a location I can read. Maybe you did not share any? Or you shared a live location, which is also not processable for me!"
                await event.respond(answer,allow_html=True)
        
        except:
            answer = "There was an error. Maybe try it again later, or contact the support team at team@agenda-analytics.eu \U0001F635"
            await event.respond(answer,allow_html=True)


        
