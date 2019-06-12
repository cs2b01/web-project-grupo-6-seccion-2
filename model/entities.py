from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector
import datetime


class Usuario(connector.Manager.Base):
    __tablename__ = 'usuarios'
    correo     = Column(String(200), primary_key=True)
    nombre     = Column(String(150))
    apellido   = Column(String(150))
    contrasena = Column(String(50))
    usuario    = Column(String(50))
    record     = Column(Integer)


class Categoria(connector.Manager.Base):
    __tablename__ = 'categorias'
    id      = Column(Integer, Sequence('categoria_id_seq'), primary_key=True)
    nombre  = Column(String(50))


class Pregunta(connector.Manager.Base):
    __tablename__ = 'preguntas'
    id            = Column(Integer, Sequence('pregunta_id_seq'), primary_key=True)
    enunciado     = Column(String(1500))
    correcta      = Column(String(1500))
    equivocada1   = Column(String(1500))
    equivocada2   = Column(String(1500))
    equivocada3   = Column(String(1500))
    categoria_id  = Column(Integer, ForeignKey('categorias.id'))
    categoria     = relationship(Categoria, foreign_keys=[categoria_id])

