from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.route import Route, RouteLocation, RouteAssignee, RouteStatus, LocationStatus
from app.schemas.route import RouteCreate, RouteResponse, RouteUpdate

router = APIRouter()


@router.post("/", response_model=RouteResponse)
async def create_route(
    route_data: RouteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_route = Route(
        title=route_data.title,
        description=route_data.description,
        date=route_data.date,
        created_by_id=current_user.id
    )
    db.add(new_route)
    await db.flush()
    
    for location_data in route_data.locations:
        location = RouteLocation(
            route_id=new_route.id,
            name=location_data.name,
            address=location_data.address,
            description=location_data.description,
            contact_name=location_data.contact_name,
            contact_phone=location_data.contact_phone,
            order=location_data.order
        )
        db.add(location)
    
    for assignee_id in route_data.assignee_ids:
        assignee = RouteAssignee(route_id=new_route.id, user_id=assignee_id)
        db.add(assignee)
    
    await db.commit()
    
    # Загружаем маршрут со всеми связанными данными
    result = await db.execute(
        select(Route)
        .options(
            selectinload(Route.locations),
            selectinload(Route.assignees).joinedload(RouteAssignee.user)
        )
        .where(Route.id == new_route.id)
    )
    new_route = result.scalars().unique().one()
    
    # Отправляем уведомления назначенным пользователям
    if route_data.assignee_ids:
        from app.websocket.manager import manager
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"🗺️ Sending route notifications to {len(route_data.assignee_ids)} assignees")
        for assignee_id in route_data.assignee_ids:
            logger.info(f"🗺️ Sending notification to user {assignee_id} for route {new_route.id}")
            await manager.send_route_notification(
                user_id=assignee_id,
                route_id=new_route.id,
                route_title=new_route.title,
                assigned_by=current_user.id
            )
    
    return new_route


@router.get("/", response_model=List[RouteResponse])
async def get_routes(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "date",  # date, title, status
    order: str = "desc",  # asc, desc
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import desc, asc
    
    # Определяем поле для сортировки
    sort_field = Route.date
    if sort_by == "title":
        sort_field = Route.title
    elif sort_by == "status":
        sort_field = Route.status
    
    # Определяем направление сортировки
    sort_order = desc(sort_field) if order == "desc" else asc(sort_field)
    
    result = await db.execute(
        select(Route)
        .options(
            selectinload(Route.locations),
            selectinload(Route.assignees).joinedload(RouteAssignee.user)
        )
        .order_by(sort_order)
        .offset(skip)
        .limit(limit)
    )
    routes = result.scalars().unique().all()
    
    # Отладка
    import logging
    logger = logging.getLogger(__name__)
    for route in routes:
        logger.info(f"🗺️ Route {route.id}: {len(route.assignees)} assignees")
        for assignee in route.assignees:
            logger.info(f"  👤 Assignee {assignee.id}: user_id={assignee.user_id}, user={assignee.user}")
            if assignee.user:
                logger.info(f"    ✅ User: {assignee.user.first_name} {assignee.user.last_name}, phone={assignee.user.phone}")
            else:
                logger.info(f"    ❌ User is None!")
    
    return routes


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Route)
        .options(
            selectinload(Route.locations),
            selectinload(Route.assignees).joinedload(RouteAssignee.user)
        )
        .where(Route.id == route_id)
    )
    route = result.scalars().unique().one_or_none()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    return route


@router.put("/{route_id}", response_model=RouteResponse)
async def update_route(
    route_id: int,
    route_update: RouteUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Route).where(Route.id == route_id)
    )
    route = result.scalar_one_or_none()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Проверяем права: только автор может редактировать
    if route.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only route creator can edit it")
    
    # Обновляем базовые поля
    update_data = route_update.dict(exclude_unset=True, exclude={'assignee_ids', 'locations'})
    for field, value in update_data.items():
        setattr(route, field, value)
    
    # Обновляем точки маршрута
    if route_update.locations is not None:
        # Удаляем старые точки
        await db.execute(
            select(RouteLocation).where(RouteLocation.route_id == route_id)
        )
        result = await db.execute(
            select(RouteLocation).where(RouteLocation.route_id == route_id)
        )
        old_locations = result.scalars().all()
        for loc in old_locations:
            await db.delete(loc)
        
        # Добавляем новые точки
        for location_data in route_update.locations:
            location = RouteLocation(
                route_id=route_id,
                name=location_data.name,
                address=location_data.address,
                description=location_data.description,
                contact_name=location_data.contact_name,
                contact_phone=location_data.contact_phone,
                order=location_data.order
            )
            db.add(location)
    
    # Обновляем назначенных пользователей
    if route_update.assignee_ids is not None:
        # Удаляем старых назначенных
        result = await db.execute(
            select(RouteAssignee).where(RouteAssignee.route_id == route_id)
        )
        old_assignees = result.scalars().all()
        for assignee in old_assignees:
            await db.delete(assignee)
        
        # Добавляем новых назначенных
        for assignee_id in route_update.assignee_ids:
            assignee = RouteAssignee(route_id=route_id, user_id=assignee_id)
            db.add(assignee)
    
    await db.commit()
    
    # Загружаем маршрут со всеми связанными данными
    result = await db.execute(
        select(Route)
        .options(
            selectinload(Route.locations),
            selectinload(Route.assignees).joinedload(RouteAssignee.user)
        )
        .where(Route.id == route_id)
    )
    route = result.scalars().unique().one()
    
    return route


@router.delete("/{route_id}")
async def delete_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Route).where(Route.id == route_id))
    route = result.scalar_one_or_none()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Проверяем права: только автор может удалять
    if route.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only route creator can delete it")
    
    await db.delete(route)
    await db.commit()
    
    return {"message": "Route deleted successfully"}


@router.patch("/{route_id}/locations/{location_id}/status")
async def update_location_status(
    route_id: int,
    location_id: int,
    status: LocationStatus,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, что маршрут существует и пользователь назначен на него
    result = await db.execute(
        select(Route)
        .options(selectinload(Route.assignees))
        .where(Route.id == route_id)
    )
    route = result.scalars().unique().one_or_none()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Проверяем, что пользователь назначен на этот маршрут
    is_assignee = any(assignee.user_id == current_user.id for assignee in route.assignees)
    if not is_assignee and route.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not assigned to this route")
    
    # Обновляем статус точки
    result = await db.execute(
        select(RouteLocation).where(
            RouteLocation.id == location_id,
            RouteLocation.route_id == route_id
        )
    )
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    location.status = status
    
    # Проверяем, все ли точки завершены
    result = await db.execute(
        select(RouteLocation).where(RouteLocation.route_id == route_id)
    )
    all_locations = result.scalars().all()
    
    if all(loc.status == LocationStatus.COMPLETED for loc in all_locations):
        route.status = RouteStatus.COMPLETED
    elif any(loc.status in [LocationStatus.ARRIVED, LocationStatus.IN_TRANSIT] for loc in all_locations):
        route.status = RouteStatus.IN_PROGRESS
    
    await db.commit()
    
    return {"message": "Location status updated", "location_id": location_id, "status": status}
