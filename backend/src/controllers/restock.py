"""
Restocking Operations controller functions for the Inventory Management API
"""
import logging
from connexion import NoContent
import exceptions
from controllers import tools
from models.product import Product  # Import Product model
from models.restock_log import RestockLog  # Import RestockLog model
from datetime import datetime

LOG = logging.getLogger(__name__)


def _get_product_by_id_for_restock(id_: int):
    """Helper to get product by ID or raise ProductNotFound (specific for restock)."""
    product = Product.get_by_id(id_)
    if not product:
        LOG.error('Product %s was not found for restock operation', id_)
        raise exceptions.ProductNotFound(product_id=id_)
    return product


@tools.normal_response(200)
@tools.expected_errors(400, 404)
def product_restock(product_id: int, body: dict):
    """Restock a specific product."""
    quantity = body.get('quantity')
    reason = body.get('reason')

    product = _get_product_by_id_for_restock(product_id)

    if not isinstance(quantity, int) or quantity <= 0:
        LOG.info('Product %s restocked by %d units. New quantity: %d', product.id, quantity, product.quantity)
        raise exceptions.RestockLogInvalidQuantity(quantity=quantity)

    # Update product quantity
    product.quantity += quantity
    product.update({'quantity': product.quantity})
    LOG.info('Product %s restocked by %d units. New quantity: %d', product.id, quantity, product.quantity)

    # Create a restock log entry
    data = {'product_id': product_id, **body}
    restock_log = RestockLog(data)

    restock_log.create()
    LOG.info('Restock log created for product %s.', product.id)
    return product.to_dict()  # Return updated product details


@tools.normal_response(200)
def get_restock_history():
    """Get a history of restocking logs."""
    restock_logs = RestockLog.get_all()
    return [log.to_dict() for log in restock_logs]
