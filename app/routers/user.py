from .. import models , schemas , utils
from fastapi import Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.get("/",response_model=List[schemas.Userout])
async def get_all_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@router.get("/{id}",response_model=schemas.Userout)
async def get_user_by_id(id:int,db: Session = Depends(get_db)):
    get_user_query = db.query(models.User).filter(models.User.id == id)
    user = get_user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Has not Found")

    return user

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Userout)
async def create_user(user:schemas.user,db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user