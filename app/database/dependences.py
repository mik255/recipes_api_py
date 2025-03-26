from app.database.config import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()     # Se não houve exceção, faz o commit
    except:
        db.rollback()   # Em caso de erro, faz rollback
        raise
    finally:
        db.close()      # Fecha a sessão sempre