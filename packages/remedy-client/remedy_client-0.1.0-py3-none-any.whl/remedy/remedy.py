import requests
import sys
import re
import json
import base64
import os

from remedy import exceptions

class RemedyClient:
    """
    A REST Client class for BMC Remedy ITSM.

    :param endpoint: Remedy endpoint.
    :type endpoint: str
    :param proxies: List of proxies
    :type proxies: dict
    :param username: Username
    :type username: str
    :param password: User password
    :type password: str
    """


    def __init__(self, endpoint="", proxies=None, username="", password=""):
        self.endpoint = endpoint
        self.proxies = proxies
        self.username = username
        self.password = password
        self.endpoint_smartit = self.endpoint.replace('-restapi','-smartit')
        self.headers = {}
        self.authenticate()


    def query(self, uri, data=None, params=None, headers={}, method='GET'):
        """
        Request the uri and returns the response.

        :param uri: Remedy API uri..
        :type uri: str
        :param data: Request data.
        :type data: dict
        :param params: Request parameters.
        :type params: dict
        :param headers: Request headers.
        :type headers: dict
        :param method: HTTP method.
        :type method: str

        :returns: HTTP Status Code
        :rtype: integer
        """
        url = f'{self.endpoint}{uri}'
        headers.update(self.headers)
        
        response = requests.request(
            method,
            url,
            data=data,
            params=params,
            headers=headers,
            proxies=self.proxies
        )
       
        if response.status_code not in [200, 201, 204]:
            raise exceptions.RemedyError(f'{response.status_code} - {response.text}')

        try:
            return response.json()
        except:
 	       return response.text
 

    def close(self):
        """
        Close the connection to BMC Remedy ITSM.

        :returns: HTTP Status Code
        :rtype: integer
        """
        return self.delete_token()


    def authenticate(self):
        """
        Authenticat against BMC Remedy ITSM.

        :returns: is_authenticated
        :rtype: bool
        """
        token = self.get_token()
        self.token = f'AR-JWT {token}'
        self.headers = { 'Authorization': self.token }

        return True

    
    def is_authenticated(self):
        """ 
        Returns if the client is authenticated
        :returns: is_authenticated
        :rtype: bool
        """
        if not self.token:
            return False
        return True


    def get_token(self):
        """
        Return token using the URI `api/jwt/login` and update the class 
        instance attribute with that value.

        :returns: token
        :rtype: str
        """
        uri = f'/api/jwt/login'
        params = [
            ('username', self.username),
            ('password', self.password)
        ]

        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }

        token = self.query(uri, method='POST', headers=headers, params=params)

        return token


    def delete_token(self):
        """
        Delete token using the URI `api/jwt/logout`

        :returns: HTTP Status Code
        :rtype: int
        """
        uri = f'/api/jwt/logout'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = self.query(uri, method='POST', headers=headers)

        return response


    def get_form(self, form_name):
        """
        Query Remedy form using the URI `/api/arsys/v1/entry/:form_name`

        :param form_name: Remedy form name
        :type form_name: str
        :returns: Form
        :rtype: dict
        """
        uri = f'/api/arsys/v1/entry/{form_name}'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = self.query(uri, method='GET', headers=headers)

        return response

