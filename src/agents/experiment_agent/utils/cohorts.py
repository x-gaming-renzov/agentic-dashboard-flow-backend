from ...data_agent.agent import get_data_from_db
from .databases import get_mongo_db

def get_cohorts(segment_id):
    db = get_mongo_db().get_collection("segments")
    segment_details = db.find_one({"_id": segment_id})

    if not segment_details:
        return None
    
    criteria = segment_details['criteria']
    
    query = f"""Return list of uuids of players that fall in the segment. 
    Segment details: {criteria}. 
    RULES: ONLY RETURN UUIDS IN SINGLE COLUMN"""

    data = get_data_from_db(query)

    return data