import psycopg2
import psycopg2.extras

CATALOG_QUERY = """
SELECT p.id,
       c.name AS category,
       m.name AS manufacturer,
       p.name,
       p.image,
       p.composition,
       p.price,
       COALESCE(SUM(si.quantity), 0) AS quantity,
       EXISTS (
           SELECT 1
           FROM order_items oi
           JOIN stock_items s ON s.id = oi.stock_item_id
           JOIN orders o ON o.id = oi.order_id
           WHERE s.product_id = p.id
             AND o.order_date >= %(period_start)s
             AND o.order_date < %(period_end)s
       ) AS ordered_in_period
FROM products p
JOIN subcategories sc ON sc.id = p.subcategory_id
JOIN categories c ON c.id = sc.category_id
JOIN manufacturers m ON m.id = p.manufacturer_id
LEFT JOIN stock_items si ON si.product_id = p.id
GROUP BY p.id, c.name, m.name
ORDER BY p.id
"""


class DatabaseError(Exception):
    pass


class Database:
    def __init__(self, config):
        try:
            self._connection = psycopg2.connect(**config)
        except psycopg2.Error as error:
            raise DatabaseError(str(error).strip()) from error

    def fetch_catalog(self, period_start, period_end):
        params = {"period_start": period_start, "period_end": period_end}
        try:
            with self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(CATALOG_QUERY, params)
                return cursor.fetchall()
        except psycopg2.Error as error:
            self._connection.rollback()
            raise DatabaseError(str(error).strip()) from error
