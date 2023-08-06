# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:41:28 2023

@author: Friedrich.Schmidt
"""

import asyncio
from abc import ABCMeta, abstractmethod
from aiohttp_retry import RetryClient, ExponentialRetry
from requests import HTTPError
import google.oauth2.id_token
import google.auth.transport.requests
import json



class Runner():
    def __init__(self, **blocks):
        self.blocks = blocks
        #self.set_execution_plan()
        self.loop = asyncio.get_running_loop()


    def add_blocks(self, **blocks):
        self.blocks = self.blocks | blocks


    def _calculate_execution_plan(self):
        execution_plan = [block_name for block_name in self.blocks]
        last_execution_plan = []
        loops = 0
        while (last_execution_plan != execution_plan) and (loops <= len(self.blocks)):
            last_execution_plan = execution_plan.copy()
            for block_name, block in self.blocks.items():
                for entry in last_execution_plan:
                    if not entry == block_name:
                        for inp in block.inputs:
                            if inp == entry:
                                execution_plan.remove(block_name)
                                execution_plan.insert(execution_plan.index(entry)+1, block_name)
            loops += 1
        return execution_plan

    def set_execution_plan(self, ordered=True):
        if ordered:
            self.execution_plan = [block for block in self.blocks]
        else:
            self.execution_plan = self._calculate_execution_plan()
            # Get a pre calulated version from somewhere else


    async def run_blocks(self):
        future_block_mapping = {}
        for block_name in self.execution_plan:
            block = self.blocks[block_name]
            fut = self.loop.create_future()
            future_block_mapping[block_name] = fut
            block.set_input_futures(future_block_mapping)
            self.loop.create_task(block.run(future=fut))
        
        self.results = {block_name: await fut for block_name, fut in future_block_mapping.items()}
        


class ControlBlock():
    """
    Main controll class which handles the processing and data
    """
    def __init__(self, inputs, *process_classes):
        self.inputs = inputs
        self.process_classes = process_classes
    
    def set_input_futures(self, future_block_mapping):
        self.input_futures = [future_block_mapping[inp] for inp in self.inputs]


    async def _get_data_from_inp_classes(self):
        block_data = {}
        if not self.input_futures:
            return block_data
        for input_future in self.input_futures:
            block_data = block_data | await input_future
        return block_data
            

    async def run(self, future=None):
        processing_data = await self._get_data_from_inp_classes()
        for process_class in self.process_classes:
            processing_data = await process_class.process(processing_data)
        print('Done')
        if future:
            future.set_result(processing_data)
        else:
            return processing_data




class RequiredAttributesMetaClass(ABCMeta):
    required_attributes = []

    def __call__(self, *args, **kwargs):
        obj = super(RequiredAttributesMetaClass, self).__call__(*args, **kwargs)
        obj_name = obj.__class__.__name__
        for attr_name in obj.required_attributes:
            try:
                if not getattr(obj, attr_name):
                    msg = 'Attribute "{}" of class "{}" is empty!'.format(attr_name, obj_name)
                    raise ValueError(msg)
            except AttributeError:
                msg = 'Attribute "{}" has not been set in __init__ of class "{}"!'.format(attr_name, obj_name)
                raise AttributeError(msg)
        return obj



class Invoker(metaclass=RequiredAttributesMetaClass):
    required_attributes = ['url']

    
    def _get_json_auth_header(self, post=False, compress=False):
        """
        Creates an authentification header for Google Cloud HTTP endpoints
        
        url: URL to the desicred Google Cloud HTTP endpoint
        post: Flag whether or not the header is for a post request
        compress: Flag whether or not the data of the post request is compress using gzip
        return: Dictionary with the authorization token and the content type of the payload. Returns None in case of an error
        """ 
        request = google.auth.transport.requests.Request()
        token = google.oauth2.id_token.fetch_id_token(request, self.url)
        
        auth_header = {'Authorization': 'Bearer {}'.format(token), 'x-api-key': ''}
        if post:
            if compress:
                auth_header['Content-Encoding'] = 'gzip'
                auth_header['Content-Type'] = 'application/x-gzip'
            else:
                auth_header['Content-Type'] = 'application/json'
                
        return auth_header
    
    async def _invoke(self, payload):
        retry_options = ExponentialRetry(attempts=5, factor=0, statuses={104, 408, 409, 421, 425, 429, 500, 502, 503, 504})
        retry_client = RetryClient(retry_options=retry_options)
        if payload:
            auth_header = self._get_json_auth_header(post=True)
            response = await retry_client.post(self.url, headers=auth_header, data=json.dumps(payload), timeout=321)
        else:
            auth_header = self._get_json_auth_header(post=False)
            response = await retry_client.get(self.url, headers=auth_header, timeout=15)

        if response.content_type == 'application/json':
            response_payload = await response.json()
        else:
            response_payload = await response.text()

        await retry_client.close()
        return response.status, response_payload

    async def make_request(self, payload):
        response_status, response_payload = await self._invoke(payload)
        if response_status == 200:
            return response_payload
        else:
            err_msg = 'Request to ' + self.url + ' failed with status code: ' + str(response_status)
            if isinstance(response_payload, str):
                err_msg += 'and message: ' + response_payload
            raise HTTPError(err_msg)

    @abstractmethod
    async def process(self, inp_data):
        pass