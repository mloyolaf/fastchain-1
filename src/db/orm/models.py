from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
    DeclarativeBase,
)
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class Template(Base):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    system_template: Mapped[str] = mapped_column(nullable=True)
    human_template: Mapped[str] = mapped_column(nullable=False)
    ai_template: Mapped[str] = mapped_column(nullable=False)

# class Template(Base):
#     __tablename__ = "templates"

#     id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
#     template: Mapped[str] = mapped_column(nullable=False)
#     template_id: Mapped[int] = mapped_column(ForeignKey("templates.id"), nullable=True)
#     template_type: Mapped[str] = mapped_column(nullable=False)
#     next_template: Mapped[List["Template"]] = relationship("Template", remote_side=[id])
    
