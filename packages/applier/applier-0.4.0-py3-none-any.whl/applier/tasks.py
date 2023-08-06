import logging
import dramatiq
from dramatiq.brokers.redis import RedisBroker

from .commands import apply, sync
from .config import REDIS_HOST, REDIS_PORT

broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT)
dramatiq.set_broker(broker)

logger = logging.getLogger(__name__)


@dramatiq.actor
def sync_and_apply():
    logger.info("Starting sync...")
    sync()

    logger.info("Starting apply...")
    apply()

    logger.info("Completed!")
