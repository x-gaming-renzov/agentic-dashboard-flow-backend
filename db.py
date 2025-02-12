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

def insert_ideas_into_insight(idea_ids,insight_id):
    """Inserts an array of idea IDs into the 'children' array of a specific insight."""
    try:
        logger.info(f"Inserting ideas into insight {insight_id}")
        insights_collection = db["insights"]
        insights_collection.update_one(
            {"_id": insight_id},
            {"$push": {"children": {"$each": [{"id": idea_id, "type": "idea"} for idea_id in idea_ids]}}}
        )
    except Exception as e:
        logger.error(f"Error inserting ideas into insight {insight_id}: {e}")

def insert_experiment(experiment):
    """
    Inserts the experiment document into the 'experiments' collection.
    Returns a list of inserted experiment IDs.
    """
    try:
        logger.info("Inserting experiment into MongoDB")
        experiments_collection = db["experiments"]
        result = experiments_collection.insert_one(experiment)
        logger.info(f"Experiment inserted with id: {result.inserted_id}")
        return [str(result.inserted_id)]
    except Exception as e:
        logger.error(f"Error inserting experiment: {e}")
        return []

def add_experiment_to_user(user_id, experiment_id):
    """
    Adds the experiment_id to the user's experiments array.
    If the experiments field does not exist, MongoDB will create it.
    """
    try:
        logger.info(f"Adding experiment {experiment_id} to user {user_id}")
        users_collection = db["users"]
        users_collection.update_one(
            {"_id": user_id},
            {"$push": {"experiments": experiment_id}}
        )
    except Exception as e:
        logger.error(f"Error adding experiment id to user {user_id}: {e}")

def get_offer(offer_ids):
    """
    Retrieves offer details for a list of offer IDs from the 'offers' collection.
    Returns a dictionary mapping each offer ID to its details, for example:
    {
        "offer_id1": {
            "offer_name": "Casual Player Boost Bundle",
            "offer_description": "Description for casual player boost..."
        },
        "offer_id2": {
            "offer_name": "Warrior's Competitive Edge Bundle",
            "offer_description": "Description for warrior's edge..."
        }
    }
    """
    try:
        logger.info(f"Fetching details for offers: {offer_ids}")
        offers_collection = db["offers"]
        cursor = offers_collection.find({"_id": {"$in": offer_ids}})
        offers = {}
        for doc in cursor:
            offers[doc["_id"]] = {
                "offer_name": doc.get("offer_name", "unnamed"),
                "offer_description": doc.get("offer_description", "sample_description")
            }
        return offers
    except Exception as e:
        logger.error(f"Error fetching offers: {e}")
        return {}