from typing import Any, List
from doctor.api import deps
from doctor.crud.crud_dummy import dummydoctor
from doctor.crud.crud_utility import user
from doctor.models.usermodel import User
from doctor.schemas.user import UserDummyApi, UserDummyCreate, UserDummyUpdate
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from doctor.helper import csv_reader


router = APIRouter()


@router.get('/read-dummies', response_model=List[UserDummyApi])
async def read_dummydoctors(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):

    items = await dummydoctor.get_multi_dummy(db=db, skip=skip, limit=limit)
    return items

# for single Dummy Doctor


@router.get('/read-dummy/{id}', response_model=UserDummyApi)
async def read_dummydoctor(*, db: Session = Depends(deps.get_db), id: str) -> Any:

    item = await dummydoctor.get(db=db, id=id)
    return item


@router.put('/update-dummy/{id}', response_model=UserDummyApi)
async def update_dummy(*, db: Session = Depends(deps.get_db), id: str, item_in: UserDummyUpdate, current_user: User = Depends(deps.get_active_superusr_or_admin)) -> Any:
    """ 
    Update the dummy doctor
    """
    item = await dummydoctor.get(db=db, id=id)
    if not item:
        raise HTTPException(
            status_code=400, detail='Doctor Not Found!'
        )
    item = await dummydoctor.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.post("/create-dummy")
async def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: UserDummyCreate,
    current_user: User = Depends(deps.get_active_superusr_or_admin)
) -> Any:
    """
    Create new dummy doctor.
    """
    item = await dummydoctor.create_dummydoctor(
        db=db, obj_in=item_in, user_id=current_user.id)
    return {'success': 'Dummy users creation successfull.'}


@router.delete('/remove-dummy/{id}', response_model=UserDummyApi)
async def remove_dummy(*, db: Session = Depends(deps.get_db), id: str, current_user: User = Depends(deps.get_active_superusr_or_admin)) -> Any:

    item = await dummydoctor.get(db=db, id=id)

    if not item:
        raise HTTPException(
            status_code=400, detail='Doctor Not Found!'
        )
    dummy = await dummydoctor.remove(db=db, id=id)
    return dummy


@router.post('/csv-to-doctors')
async def csv_to_doctor(*, background_tasks : BackgroundTasks, db: Session = Depends(deps.get_db), file: UploadFile = File(...), current_user: User = Depends(deps.get_active_superusr_or_admin)):

    contents = file.file.read()

    data = await csv_reader.read_csv_file(contents=contents, schema=UserDummyCreate)

    # dummies = await dummydoctor.create_dummydoctors(db=db, dummy_list=data,user_id=current_user.id)

    # dummmy doctors will be created in the  background
    background_tasks.add_task(dummydoctor.create_dummydoctors, db=db, dummy_list=data, user_id=current_user.id)

    return {'success': 'Doctors creation from csv file has been added in the task!'}
    
