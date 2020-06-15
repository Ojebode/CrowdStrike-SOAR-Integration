from connectors.core.connector import get_logger, ConnectorError
from .crowdstrike_utils import CrowdStrike
import json

logger = get_logger('CrowdStrike')


def get_token(config):
    try:
        sny = CrowdStrike(config)
        token, status = sny.generate_token()
        return token, status

    except Exception as error:
        logger.exception(str(error))
        raise ConnectorError(str(error))


def contain_host(config, params):
    try:
        v_token, v_status = get_token(config)
        endpoint = 'devices/entities/devices-actions/v2'
        sny = CrowdStrike(config)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(v_token)
                   }

        host_ID = params.get('hostid')
        payload = {"action_name": "contain"
                   }
        data = {"ids": [host_ID]}
        if v_status == 201:
            response, status = sny.get_call(endpoint, headers, data=json.dumps(data), payload=payload)
            print("V_token: ", v_token)
            print("V_status: ", v_status)
            print("Headers: ", headers)
            print("Data: ", data)
            print(status)
            return response

    except Exception as error:
        logger.exception(str(error))
        raise ConnectorError(str(error))


def lift_hostcontainment(config, params):
    try:
        v_token, v_status = get_token(config)
        endpoint = 'devices/entities/devices-actions/v2'
        sny = CrowdStrike(config)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(v_token)
                   }

        host_ID = params.get('lifthostid')
        payload = {"action_name": "lift_containment"
                   }
        data = {"ids": [host_ID]}
        if v_status == 201:
            response, status = sny.get_call(endpoint, headers, data=json.dumps(data), payload=payload)
            print("V_token: ", v_token)
            print("V_status: ", v_status)
            print("Headers: ", headers)
            print("Data: ", data)
            print(status)
            return response

    except Exception as error:
        logger.exception(str(error))
        raise ConnectorError(str(error))


def _check_health(config):
    try:
        conn = CrowdStrike(config)
        token, resp_code= conn.generate_token()
        if resp_code == 201:
            logger.info("CrowdStrike Connector Available")
            print("Status code is: ", resp_code)
            return True
        else:
            print("Status code is: ", resp_code)
            raise ConnectorError('connector is not available.')
    except Exception as error:
        logger.exception(str(error))
        raise ConnectorError(str(error))


operations = {
    'contain_host': contain_host,
    'lift_hostcontainment': lift_hostcontainment,
}
