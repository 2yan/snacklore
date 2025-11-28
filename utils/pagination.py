"""Pagination helper utilities."""
from flask import request


def get_pagination_params():
    """Extract pagination parameters from request."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Limit per_page to max 100
    per_page = min(per_page, 100)
    # Ensure page is at least 1
    page = max(page, 1)
    
    return page, per_page


def paginate_query(query, page, per_page):
    """Paginate a SQLAlchemy query."""
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages


def format_pagination_response(items, total, page, per_page, pages=None):
    """Format paginated response."""
    if pages is None:
        pages = (total + per_page - 1) // per_page if total > 0 else 0
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': pages
    }

