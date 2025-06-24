"""
Product controller functions for the Inventory Management API
"""
import logging
from connexion import NoContent
import exceptions
from controllers import tools
from models.product import Product  # Import the new Product model

LOG = logging.getLogger(__name__)


def _get_product_by_id(id_: int):
    """Get product by ID or raise ProductNotFound."""
    product = Product.get_by_id(id_)
    if not product:
        LOG.error('Product %s was not found', id_)
        raise exceptions.ProductNotFound(product_id=id_)
    return product


@tools.expected_errors(404)
def product_get_by_id(product_id: int):
    """Get product by ID."""
    product = _get_product_by_id(product_id)
    return product.to_dict()


def product_get_all():
    """Get all products."""
    products = Product.get_all()
    return [p.to_dict() for p in products]


@tools.normal_response(201)
@tools.expected_errors(400, 409)
def product_create(body: dict):
    """Add a new product."""
    # Check for required fields
    if not all(k in body for k in ['name', 'sku', 'quantity', 'price']):
        raise exceptions.BadRequest(message="Name, SKU, quantity, and price are required.")

    # Check for existing SKU
    sku = body.get('sku')
    existing_product = Product.get_by_sku(sku)
    if existing_product:
        LOG.error('Product with SKU %s already exists.', sku)
        raise exceptions.ProductSKUAlreadyExist(sku=sku)

    product = Product(body)
    if product.create():
        LOG.info('Product %s was created successfully!', product.id)
        return product.to_dict()

    LOG.error('Failed to create product with SKU %s due to unknown reason.', product.sku)
    raise exceptions.InternalServerError(message='Failed to create product.')


@tools.expected_errors(400, 404, 409)
def product_update(product_id: int, body: dict):
    """Update product details or stock level."""
    product = _get_product_by_id(product_id)

    # If SKU is updated, check for conflict
    if 'sku' in body and body['sku'] != product.sku:
        sku = body['sku']
        existing_product = Product.get_by_sku(sku)
        if existing_product and existing_product.id != product_id:
            LOG.error('Product with SKU %s already exists in product %s (%i).', sku, existing_product.name,
                      existing_product.id)
            raise exceptions.ProductSKUAlreadyExist(sku=sku)

    if product.update(body):
        LOG.info('Product %s was updated successfully!', product.id)
        return product.to_dict()

    LOG.error('Failed to update product %s due to unknown reason.', product_id)
    raise exceptions.InternalServerError(message='Failed to update product.')


@tools.normal_response(204)
@tools.expected_errors(404)
def product_delete(product_id: int):
    """Delete a product from the inventory."""
    product = _get_product_by_id(product_id)
    product.delete()
    LOG.info('Product %s was deleted successfully!', product.id)
    return NoContent
