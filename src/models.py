from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class FavouritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(
        back_populates="user_favourites_planet")
    planet: Mapped["Planets"] = relationship(
        back_populates="planets_favorites")

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }


class FavouritePeople(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(
        back_populates="user_favourites_people")
    people: Mapped["People"] = relationship(back_populates="peoples_favorites")

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "user_id": self.user_id
        }


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    user_favourites_people: Mapped[List["FavouritePeople"]] = relationship(
        back_populates="user")
    user_favourites_planet: Mapped[List["FavouritePlanet"]] = relationship(
        back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,

            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(400), nullable=False)
    description: Mapped[str] = mapped_column(String(120), nullable=False)
    galaxy: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[str] = mapped_column(String(120), nullable=False)
    gravity: Mapped[int] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=False)

    planets_favorites: Mapped[List["FavouritePlanet"]
                              ] = relationship(back_populates="planet")
    people: Mapped[list["People"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "name": self.name,
            "galaxy": self.galaxy,
            "population": self.population,
            "gravity": self.gravity,
            "image": self.image

        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(400), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[int] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=False)
    planet_of_birth: Mapped[int] = mapped_column(ForeignKey("planets.id"))

    planet: Mapped["Planets"] = relationship(back_populates="people")
    peoples_favorites: Mapped[List["FavouritePeople"]
                              ] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "image": self.image,
            "planet_of_birth": self.planet_of_birth
        }
