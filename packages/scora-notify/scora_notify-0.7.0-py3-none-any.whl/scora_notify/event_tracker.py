from mixpanel import Mixpanel
import uuid
from datetime import datetime
import re

import logging

class EventTracker():
    
    def __init__(self, mixpanel_token, project, tenant, is_enabled=True):
        """Initializes the event tracker

        Args:
            mixpanel_token (str): Mixpanel Project token. (refering to the Performance Analytics Project)
            project (str): Name of the project being tracked. (refering to the code's project)
            tenant (str): Tenant name. (refering to the Performance Analytics Project)
            is_enabled (bool, optional): Whether to enable tracking. Defaults to True.
        """
        self.MIXPANEL_TOKEN = mixpanel_token
        self.PROJECT = project
        self.TENANT = tenant
        self.IS_ENABLED = is_enabled
        
        if not self.IS_ENABLED: return
        
        self.mp = Mixpanel(self.MIXPANEL_TOKEN)
        self.session_id = uuid.uuid1().int
        
        self.event_time_start = {}
        
    def _validate_event_name(self,event_name):
        if type(event_name)!=str:
            raise ValueError("Make sure event name is a string")
           
    def _get_parsed_event_name(self,event_name):
        self._validate_event_name(event_name)
        
        event_name= re.sub(r' |-', '_', event_name)
        
        event_name = f"{self.PROJECT}_{event_name}"
        return event_name.upper()
    
    def _get_parsed_properties(self, properties):
        new_props = {}
        for key in properties:
            new_key = re.sub(r' |-', '_', key)
            new_key = f"{self.PROJECT}_{new_key}".upper()
            new_props[new_key] = properties[key]
            
        new_props['Tenant'] = self.TENANT
        new_props['Project'] = self.PROJECT
        
        return new_props
    
    def _add_context_to_properties(self, properties):
        return {**properties, "Project":self.PROJECT, "Tenant": self.TENANT}
    
    def track(self, event_name, properties={}):
        if not self.IS_ENABLED: return
        
        event_name = self._get_parsed_event_name(event_name)
        properties = self._get_parsed_properties(properties)
        
        if event_name in self.event_time_start:
            delta = datetime.now() - self.event_time_start[event_name] 
            duration = delta.total_seconds()
            properties = {**properties, 'Duration':duration}
            del self.event_time_start[event_name]

        self.mp.track(self.session_id, event_name, properties)
        
        logging.info(f"Event {event_name} successfully tracked")
       
    def time_event(self, event_name):
        if not self.IS_ENABLED: return
        
        event_name = self._get_parsed_event_name(event_name)
        
        self.event_time_start[event_name] = datetime.now()