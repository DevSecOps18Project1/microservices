"""
Analytics controller functions for the Inventory Management API
"""
import logging
import random
from datetime import datetime, timedelta

from controllers import tools
import exceptions
from models.product import Product  # Import Product model
# from models.restock_log import RestockLog

LOG = logging.getLogger(__name__)


@tools.normal_response(200)
def get_low_stock_products(threshold: int = 20):  # Default threshold as per YAML
    """Get a list of products with stock below a defined threshold."""
    if not isinstance(threshold, int) or threshold < 0:
        raise exceptions.AnalyticsInvalidThreshold(threshold=threshold)

    # Assuming `stock_level` is a column in the Product model
    low_stock_products = Product.get_low_quantity(threshold)

    response_data = []
    for product in low_stock_products:
        response_data.append({
            'id': product.id,
            'uuid': product.uuid,
            'name': product.name,
            'sku': product.sku,
            'quantity': product.quantity,
            'threshold': threshold
        })
    return response_data


@tools.normal_response(200)
def get_stock_trend_data():
    """Fetch stock trend data for dashboard visualization (mock data)."""
    all_products = Product.get_all()
    if not all_products:
        LOG.info('No products available to generate trend data.')
        return []

    # restock_logs = RestockLog.get_all()

    # In a real system, this would query historical stock levels
    # or process movement logs to generate trend data.
    # For demonstration, we'll generate some mock data.

    trend_data = []
    end_date = datetime.now()
    # Generate data for the last 30 days
    for product in all_products:
        current_quantity = product.quantity
        for i in range(30):
            date = end_date - timedelta(days=29 - i)
            # Simulate some stock fluctuations (random walk)
            stock_change = random.randint(-5, 5)
            current_quantity = max(0, current_quantity + stock_change)  # Stock can't go below 0

            trend_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'product_id': product.id,
                'product_name': product.name,
                'quantity': current_quantity
            })

    # Group by product and format as per schema
    # (The schema showed per product, then a list of trends)
    # Let's refine to match the provided schema's 'trends' array
    # The schema for StockTrendDataResponse is an object with 'product_id', 'product_name', 'data'
    # and 'data' is an array of objects with 'date' and 'stock_level'.
    # So, we need to return data for each product separately.

    final_trend_output = []
    for product in all_products:
        product_trends = [
            d for d in trend_data
            if d['product_id'] == product.id  # Filter for this product's data
        ]
        # Map to the specific 'data' structure
        formatted_product_trends = [
            {'date': item['date'], 'stock_level': item['quantity']}
            for item in product_trends
        ]

        final_trend_output.append({
            'product_id': product.id,
            'product_name': product.name,
            'data': formatted_product_trends
        })

    # The user's YAML for StockTrendDataResponse shows 'trends' as a top-level array,
    # not grouped by product. Let's revert to that simple list for now,
    # or assume the 'data' inside StockTrendDataResponse is the list of trends.
    # Given the previous YAML, it looks like a single list of all trend points.
    # Let's re-read the provided schema for StockTrendDataResponse carefully.

    # Original schema:
    # StockTrendDataResponse:
    #   type: object
    #   properties:
    #     trends:
    #       type: array
    #       items:
    #         type: object
    #         properties:
    #           date: type string
    #           product_id: type string
    #           stock_level: type integer

    # So, the `trend_data` list we generated is already in the correct format for the `trends` key.
    return trend_data
