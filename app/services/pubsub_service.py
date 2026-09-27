"""Pub/Sub Real-time Ingestion Interface"""
import logging
import asyncio
import json
from typing import Dict, Any, Callable, List

logger = logging.getLogger(__name__)

class PubSubService:
    def __init__(self, topic_id: str = "cardguard-transactions-dev"):
        self.topic_id = topic_id
        self._listeners: List[Callable[[Dict[str, Any]], None]] = []
        self._queue: asyncio.Queue = asyncio.Queue()

    async def publish_transaction(self, transaction: Dict[str, Any]) -> str:
        """Publishes transaction to real-time ingestion topic."""
        message_id = f"MSG-{transaction['transaction_id']}"
        logger.info(f"Published transaction {transaction['transaction_id']} to PubSub topic {self.topic_id}")
        await self._queue.put(transaction)
        return message_id

    async def consume_messages(self, handler: Callable[[Dict[str, Any]], None]):
        """Consumes real-time transactions from ingestion queue."""
        while True:
            tx = await self._queue.get()
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(tx)
                else:
                    handler(tx)
            except Exception as e:
                logger.error(f"Error processing transaction message: {e}")
            finally:
                self._queue.task_done()

pubsub_service = PubSubService()
