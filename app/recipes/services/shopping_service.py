from app.database.dependences import get_db
from app.recipes.dtos.shopping_dto import PostShoppingListRequestDTO
from app.recipes.models.ingredient import Ingredient
from app.recipes.models.shopping_list import ShoppingList
from app.recipes.repository.posts_repository import create_post


def create_shopping_list_service(dto: PostShoppingListRequestDTO, user_id: int):
    with next(get_db()) as db:
        # 1️⃣ Cria a ShoppingList sem itens
        lista = ShoppingList(
            user_id=user_id,
            name=dto.name,
            recipe_id=dto.recipe_id
        )
        db.add(lista)
        db.flush()  # popula lista.id e os timestamps (created_at)

        # 2️⃣ Cria todos os ShoppingItem referenciando lista.id
        itens = []
        for item in dto.shopping_items:
            itens.append(
                Ingredient(
                    name=item.name,
                    quantity=item.quantity,
                    unity=item.unity,
                    price=item.price,
                    shopping_list_id=lista.id,
                    category=item.category,
                    img=item.img,
                    count=item.count,
                    title=item.img,  # Isso parece um erro, pois 'img' é uma string e 'title' é um campo diferente
                    selected=item.selected,
                )
            )
        # Associa os itens à lista
        lista.shopping_items = itens

        # 3️⃣ Persiste tudo de uma vez
        db.commit()
        # Refresh para carregar created_at, updated_at e ids de itens
        db.refresh(lista)
        return lista


def get_shopping_list_service(user_id: int):
    with next(get_db()) as db:
        # 1️⃣ Busca a lista de compras pelo ID
        lista = db.query(ShoppingList).filter(
            ShoppingList.user_id == user_id
        ).all()

        # 2️⃣ Se não encontrar, retorna None
        if not lista:
            return []

        # 3️⃣ Retorna a lista de compras encontrada
        return lista
    
def delete_shopping_list_service(id: int):
    with next(get_db()) as db:
        # 1️⃣ Busca a lista de compras pelo ID
        lista = db.query(ShoppingList).filter(
            ShoppingList.id == id
        ).first()

        # 2️⃣ Se não encontrar, retorna None
        if not lista:
            return None

        # 3️⃣ Deleta a lista de compras encontrada
        db.delete(lista)
        db.commit()
        return lista
    
def update_shopping_list_service(id: int, dto: PostShoppingListRequestDTO):
    with next(get_db()) as db:
        # 1️⃣ Busca a lista de compras pelo ID
        lista = db.query(ShoppingList).filter(
            ShoppingList.id == id
        ).first()


        # 3️⃣ Atualiza os campos da lista de compras
        lista.name = dto.name
        lista.recipe_id = dto.recipe_id

        # 4️⃣ Atualiza os itens da lista de compras
        for item in dto.shopping_items:
            if(item.id is None):
                new_item = Ingredient(
                    name=item.name,
                    quantity=item.quantity,
                    unity=item.unity,
                    price=item.price,
                    shopping_list_id=lista.id,
                    img=item.img,
                    title = item.img,
                    count = item.count,
                    selected = item.selected,
                )
                db.add(new_item)
                db.commit()
                db.flush()
                item.id = new_item.id
                
            shopping_item = db.query(Ingredient).filter(
                Ingredient.id == item.id
            ).first()
            if shopping_item:
                shopping_item.name = item.name
                shopping_item.quantity = item.quantity
                shopping_item.unity = item.unity
                shopping_item.price = item.price
                shopping_item.img = item.img
                shopping_item.category = item.category
                shopping_item.shopping_list_id = lista.id
                shopping_item.count = item.count
                shopping_item.selected = item.selected
                
        db.commit()
        db.refresh(lista)
        return lista
    
    
def get_shopping_list_by_id_service(id: int):
    with next(get_db()) as db:
        # 1️⃣ Busca a lista de compras pelo ID
        lista = db.query(ShoppingList).filter(
            ShoppingList.id == id
        ).first()

        # 2️⃣ Se não encontrar, retorna None
        if not lista:
            return None

        # 3️⃣ Retorna a lista de compras encontrada
        return lista