import os
from pymongo import MongoClient
from util import logger, log_error

# Environment variables
MONGO_URI = os.getenv("XG_MONGO_URI")
MONGO_DB = os.getenv("XG_MONGO_DB")

# MongoDB client setup
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

def get_metric_ids_for_idea(idea_id):
    """
    Retrieve all metric IDs that belong to an idea via its segments.

    :param idea_id: The unique ID of the idea.
    :return: A list of unique metric IDs or an empty list if no metrics are found.
    """
    try:
        logger.info(f"Fetching idea with ID: {idea_id}")

        # Fetch the idea document
        idea = db.ideas.find_one({"_id": idea_id})
        if not idea:
            logger.warning(f"Idea with ID {idea_id} not found.")
            return []

        # Extract segment IDs associated with the idea
        segment_ids = idea.get("segments", [])
        if not segment_ids:
            logger.info(f"No segments found for idea ID {idea_id}.")
            return []

        logger.info(f"Found segments for idea ID {idea_id}: {segment_ids}")

        # Fetch all metrics associated with the segments
        metrics = set()
        segments = db.segments.find({"_id": {"$in": list(map(str, segment_ids))}})
        for segment in segments:
            segment_metrics = segment.get("metrics", [])
            metrics.update(segment_metrics)

        logger.info(f"Metrics collected for idea ID {idea_id}: {list(metrics)}")
        return list(metrics)

    except Exception as e:
        log_error(f"Error retrieving metrics for idea ID {idea_id}", e)
        return []
