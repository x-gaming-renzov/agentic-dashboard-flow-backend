import asyncio
from src.agents.experiment_agent.agent import get_experiment_ready_offer
from src.agents.experiment_agent.utils.cohorts import get_cohorts

async def get_offer_cohorts(chat_id, segment_ids):
    """
    Runs get_experiment_ready_offer and get_cohorts concurrently.
    
    Parameters:
      - chat_id: The chat identifier.
      - segment_ids: A list of two segment IDs.
    
    Returns:
      A tuple containing:
        - offer_ids: The result from get_experiment_ready_offer.
        - cohort_A: The result for the first segment's cohort.
        - cohort_B: The result for the second segment's cohort.
    """
    loop = asyncio.get_running_loop()
    
    # Wrap both synchronous functions in run_in_executor:
    offer_task = loop.run_in_executor(None, get_experiment_ready_offer, chat_id, segment_ids)
    cohort_task_A = loop.run_in_executor(None, get_cohorts, segment_ids[0])
    cohort_task_B = loop.run_in_executor(None, get_cohorts, segment_ids[1])
    
    # Await all tasks concurrently
    offer_ids, cohort_A, cohort_B = await asyncio.gather(
        offer_task,
        cohort_task_A,
        cohort_task_B
    )
    
    return offer_ids, cohort_A, cohort_B