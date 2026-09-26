from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.pattern_match import SETTING_KEY
from app.repositories import settings_repo

router = APIRouter()


class SettingsUpdate(BaseModel):
    default_match_pattern: bool | None = None


@router.get("/settings")
def settings():
    return settings_repo.get_all()


@router.post("/settings")
def update_settings(body: SettingsUpdate):
    if body.default_match_pattern is not None:
        settings_repo.set_value(SETTING_KEY, "1" if body.default_match_pattern else "0")
    return settings_repo.get_all()
