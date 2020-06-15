import requests
from connectors.core.connector import get_logger

logger = get_logger('CrowdStrike')

class CrowdStrike(object):
    def __init__(self, config):
        self.url = config.get('url')
        self.id = config.get('clientid')
        self.secret = config.get('clientsecret')

        self.base_url = "{0}/".format(self.url)
        if not self.base_url.startswith('https://'):
            self.base_url = 'https://' + self.base_url

    def generate_token(self):
        endpoint = 'oauth2/token'
        # this header is a special header, just for token generations
        # and nothing else
        headers = {'accept': 'application/json',
                   'Content-Type': 'application/x-www-form-urlencoded'
                   }
        data = {'client_id': self.id,
                'client_secret': self.secret
                }

        try:
            tok, status = self.get_call(endpoint, headers, data, payload=None)
            token = tok.get('access_token')
            print("TOKEN: ",token)
            print("STATUS: ", status)
            return token, status

        except Exception as error:
            print(error)


    def get_call(self, endpoint, headers, data, payload=None,):
        url = self.base_url + endpoint
        try:
            response = requests.post(url, headers=headers, params=payload, data=data, verify=False)
            logger.error('{}'.format(response))
            ans = response.json()
            return ans, response.status_code

        except Exception as error:
            print(error)


