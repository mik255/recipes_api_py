from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.recipes.models.midia import Midia

from app.recipes.models.post import Post

class MidiaRepository:

    @staticmethod
    def create(db: Session, url: str, type: str) -> Midia:
        try:
            # Cria a nova instância de mídia
            midia = Midia(url=url, type=type)
            # Adiciona a nova mídia ao banco de dados
            db.add(midia)
            db.commit()  # Confirma a transação
            db.refresh(midia)  # Atualiza o objeto com o ID gerado
            return midia
        except Exception as e:
            db.rollback()  # Se ocorrer um erro, reverte a transação
            raise HTTPException(status_code=500, detail=f"Erro ao criar a mídia: {str(e)}")

    @staticmethod
    def get_all(db: Session) -> list[Midia]:
        try:
            # Retorna todas as mídias da base de dados
            return db.query(Midia).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao obter as mídias: {str(e)}")

    @staticmethod
    def get_by_id(db: Session, midia_id: int) -> Midia:
        try:
            # Busca uma mídia pelo ID
            return db.query(Midia).filter(Midia.id == midia_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar a mídia: {str(e)}")

    @staticmethod
    def update(db: Session, midia_id: int, url: str, type: str) -> Midia:
        try:
            # Busca a mídia no banco de dados
            midia = db.query(Midia).filter(Midia.id == midia_id).first()
            if midia:
                # Atualiza os campos da mídia
                midia.url = url
                midia.type = type
                db.commit()  # Confirma a transação
                db.refresh(midia)  # Atualiza a instância com os novos dados
                return midia
            else:
                raise HTTPException(status_code=404, detail="Mídia não encontrada")
        except Exception as e:
            db.rollback()  # Se ocorrer um erro, reverte a transação
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar a mídia: {str(e)}")

    @staticmethod
    def delete(db: Session, midia_id: int) -> bool:
        try:
            # Busca a mídia no banco de dados
            midia = db.query(Midia).filter(Midia.id == midia_id).first()
            if midia:
                db.delete(midia)  # Deleta a mídia
                db.commit()  # Confirma a transação
                return True
            else:
                raise HTTPException(status_code=404, detail="Mídia não encontrada")
        except Exception as e:
            db.rollback()  # Se ocorrer um erro, reverte a transação
            raise HTTPException(status_code=500, detail=f"Erro ao excluir a mídia: {str(e)}")

    @staticmethod
    def associate_midia_to_post(db: Session, post_id: int, midia_id: int) -> bool:
        try:
            # Verifica se o post existe
            post = db.query(Post).filter(Post.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post não encontrado")

            # Verifica se a mídia existe
            midia = db.query(Midia).filter(Midia.id == midia_id).first()
            if not midia:
                raise HTTPException(status_code=404, detail="Mídia não encontrada")

            # Cria a associação entre o post e a mídia
            post_midia = PostMidia(post_id=post.id, midia_id=midia.id)
            db.add(post_midia)
            db.commit()  # Confirma a transação
            db.refresh(post_midia)  # Atualiza a instância com o ID gerado
            return True
        except Exception as e:
            db.rollback()  # Se ocorrer um erro, reverte a transação
            raise HTTPException(status_code=500, detail=f"Erro ao associar a mídia ao post: {str(e)}")
