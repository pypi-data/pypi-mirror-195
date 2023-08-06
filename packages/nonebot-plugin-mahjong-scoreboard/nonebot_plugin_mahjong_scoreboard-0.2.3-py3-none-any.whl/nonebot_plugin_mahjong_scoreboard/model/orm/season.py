from collections import UserDict
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import Column, Integer, DateTime, String, Enum, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship

from ._data_source import data_source
from .types.userdict import UserDict as SqlUserDict
from ..enums import SeasonState, SeasonUserPointChangeType
from ...utils.userdict import DictField

if TYPE_CHECKING:
    from .game import GameOrm
    from .group import GroupOrm
    from .user import UserOrm


class SeasonConfig(UserDict):
    south_game_enabled: bool = DictField()
    south_game_origin_point: Optional[int] = DictField(default=None)
    south_game_horse_point: Optional[List[int]] = DictField(default_factory=list)
    east_game_enabled: bool = DictField()
    east_game_origin_point: Optional[int] = DictField(default=None)
    east_game_horse_point: Optional[List[int]] = DictField(default_factory=list)
    point_precision: int = DictField(default=0)  # PT精确到10^point_precision


@data_source.registry.mapped
class SeasonOrm:
    __tablename__ = 'seasons'

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    group_id: int = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group: 'GroupOrm' = relationship('GroupOrm', foreign_keys='SeasonOrm.group_id')

    state: SeasonState = Column(Enum(SeasonState), nullable=False, default=SeasonState.initial)

    code: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)

    start_time: Optional[datetime] = Column(DateTime)
    finish_time: Optional[datetime] = Column(DateTime)

    config: SeasonConfig = Column(SqlUserDict(SeasonConfig), nullable=False)

    accessible: bool = Column(Boolean, nullable=False, default=True)
    create_time: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_time: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    delete_time: Optional[datetime] = Column(DateTime)

    __table_args__ = (
        Index("seasons_group_id_code_idx", "group_id", "code"),
    )


@data_source.registry.mapped
class SeasonUserPointOrm:
    __tablename__ = 'season_user_points'

    season_id: int = Column(Integer, ForeignKey('seasons.id'), nullable=False, primary_key=True)
    season: 'SeasonOrm' = relationship('SeasonOrm', foreign_keys='SeasonUserPointOrm.season_id')

    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    user: 'UserOrm' = relationship('UserOrm', foreign_keys='SeasonUserPointOrm.user_id')

    point: int = Column(Integer, nullable=False, default=0)

    create_time: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_time: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)


@data_source.registry.mapped
class SeasonUserPointChangeLogOrm:
    __tablename__ = 'season_user_point_change_logs'

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    season_id: int = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    season: 'SeasonOrm' = relationship('SeasonOrm', foreign_keys='SeasonUserPointChangeLogOrm.season_id')

    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    user: 'UserOrm' = relationship('UserOrm', foreign_keys='SeasonUserPointChangeLogOrm.user_id')

    change_type: SeasonUserPointChangeType = Column(Enum(SeasonUserPointChangeType), nullable=False)
    change_point: int = Column(Integer, nullable=False)

    related_game_id: Optional[int] = Column(Integer, ForeignKey('games.id'))
    related_game: Optional['GameOrm'] = relationship('GameOrm',
                                                     foreign_keys='SeasonUserPointChangeLogOrm.related_game_id')

    create_time: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("seasons_related_game_id_idx", "related_game_id"),
    )


__all__ = ("SeasonOrm", "SeasonUserPointOrm", "SeasonUserPointChangeLogOrm")
