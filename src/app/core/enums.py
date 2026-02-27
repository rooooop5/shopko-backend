from enum import Enum


class RolesEnum(str, Enum):
    MODERATOR = "moderator"
    SELLER = "seller"
    CUSTOMER = "customer"


class PermissionsEnum(Enum):
    viewProducts = "view_products"  # customer,seller,moderator
    listProduct = "list_product"  # seller
    getProduct = "get_product"  # customer,seller,moderator
    placeOrder = "place_order"  # customer
    viewOrder = "view_order"  # customer,seller
    listOrders = "list_orders"  # customer,seller
    cancelOrder = "cancel_order"  # customer,seller
    updateProduct = "update_product"  # seller
    viewSeller = "view_seller"  # moderator
    removeSeller = "remove_seller"  # moderator
    viewCustomer = "view_customer"  # moderator
    removeCustomer = "remove_customer"  # moderator
    removeProduct = "remove_product"  # seller,moderator
