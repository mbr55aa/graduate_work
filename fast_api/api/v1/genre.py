import logging
from http import HTTPStatus
from typing import List, Literal, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from core.config import ErrorMessage
from models.genre import GenreAPI, GenreBriefAPI
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/{genre_id}',
            response_model=GenreAPI,
            summary="Genre search by ID",
            description="<b>Name and description of the genre with the given ID</b><br>"
                        "<pre>An example of a call that should be handled by the API:<br>"
                        "#GET /api/v1/genre/fb58fd7f-7afd-447f-b833-e51e45e2a778</pre>",
            response_description="Genre name and description",
            tags=['Genres']
            )
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> GenreAPI:
    """Genre search function by ID"""
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.GENRE_NOT_FOUND)
    return GenreAPI(
        uuid=genre.uuid,
        name=genre.name,
        description=genre.description,
        film_ids=[film['id'] for film in genre.films]
    )


@router.get('/',
            response_model=List[GenreBriefAPI],
            summary="List of genres",
            description="<b>List of all genres with pagination</b><br>"
                        "<pre>Examples of call that should be handled by the API:<br>"
                        "#GET /api/v1/genre?sort=name.raw&page[size]=50&page[number]=1<br>"
                        "#GET /api/v1/genre?filter[film]=ff00b2a9-9e85-44af-922f-5f3504b82c15"
                        "&sort=name.raw&page[size]=50&page[number]=1</pre>",
            response_description="List of genres: genre name and description",
            tags=['Genres']
            )
async def genre_list(
        sort: Literal["name.raw"] = "name.raw",
        filter_film: Optional[UUID] = Query(None, alias="filter[film]"),
        page_size: int = Query(10, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        genre_service: GenreService = Depends(get_genre_service)
) -> List[GenreBriefAPI]:
    """Function to get a list of all genres."""
    logging.debug(f"Получили параметры {sort=}-{type(sort)}, {filter_film=}-{type(filter_film)},"
                  f" {page_size=}-{type(page_size)}, {page_number=}-{type(page_number)}")
    genres = await genre_service.get_list(filter_film, sort, page_size, page_number)
    if not genres:
        # Если выборка пустая, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum
        # Такой код будет более поддерживаемым
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.GENRE_NOT_FOUND)
    return [GenreBriefAPI(uuid=genre.id, name=genre.name, description=genre.description) for genre in genres]
