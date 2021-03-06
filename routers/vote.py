from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from schemas.vote import Vote
from database import database, models
from security import oath

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: Vote,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oath.get_current_user),
):

    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"vote does not exists",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote removed successfully"}
