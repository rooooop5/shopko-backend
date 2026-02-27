from app.core.enums import RolesEnum, PermissionsEnum

role_permissions_mapping = {
    RolesEnum.MODERATOR: [
        PermissionsEnum.viewProducts,
        PermissionsEnum.getProduct,
        PermissionsEnum.viewSeller,
        PermissionsEnum.removeSeller,
        PermissionsEnum.viewCustomer,
        PermissionsEnum.removeCustomer,
        PermissionsEnum.removeProduct,
    ],
    RolesEnum.CUSTOMER: [
        PermissionsEnum.viewProducts,
        PermissionsEnum.getProduct,
        PermissionsEnum.placeOrder,
        PermissionsEnum.viewOrder,
        PermissionsEnum.listOrders,
        PermissionsEnum.cancelOrder,
    ],
    RolesEnum.SELLER: [
        PermissionsEnum.viewProducts,
        PermissionsEnum.listProduct,
        PermissionsEnum.getProduct,
        PermissionsEnum.viewOrder,
        PermissionsEnum.listOrders,
        PermissionsEnum.cancelOrder,
        PermissionsEnum.updateProduct,
        PermissionsEnum.removeProduct,
    ]
}
