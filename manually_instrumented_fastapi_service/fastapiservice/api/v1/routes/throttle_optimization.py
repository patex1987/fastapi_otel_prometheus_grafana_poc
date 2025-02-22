"""
Routes related to throttle optimization, i.e. generating a throttle sequence
for getting from point A to point B
"""

from fastapi import APIRouter


throttle_router = APIRouter()


class GAResponse:
    pass


class GARequest:
    pass


@throttle_router.post("/run", response_model=GAResponse)
def calculate_throttle_sequence(request: GARequest):
    """
    generates a throttle sequence to get from point A to point B
    """
    # throttle_sequence = run_genetic_algorithm(request.parameters, request.config)
    #
    # # Save the run in the database
    # ga_run = GARun(id=run_id, config=request.config.dict(), result=throttle_sequence)
    # db.add(ga_run)
    # try:
    #     db.commit()
    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail="Database error")
    #
    # return GAResponse(run_id=run_id, throttle_sequence=throttle_sequence)
    return GAResponse()
