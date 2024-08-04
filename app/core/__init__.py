# from .rabbitmq import RabbitHelper
#
#
# rabbitmq_helper = RabbitHelper()
import json
from .secrets import get_secret


secret_manager = json.loads(get_secret())
