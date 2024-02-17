class Pokemon:
    def __init__(self, id, name, price, stock, sku, categories, tags, product_link, image_url=None, description=None):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.sku = sku
        self.categories = categories
        self.tags = tags
        self.image_url = image_url
        self.description = description
        self.product_link = product_link

    def __repr__(self):
        return f"<Pokemon(id={self.id}, name={self.name}, price={self.price}, stock={self.stock}, sku={self.sku}, " \
               f"categories={self.categories}, product_link={self.product_link}, tags={self.tags})>"
