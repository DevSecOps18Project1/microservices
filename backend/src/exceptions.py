class MyBaseException(Exception):
    msg_fmt = 'An unknown exception occurred.'
    title = 'Internal Server Error'
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs

            except Exception:  # pylint: disable=W0718
                self._log_exception()
                message = self.msg_fmt

        self.message = message
        super().__init__(message)

    def _log_exception(self):
        # kwargs doesn't match a variable in the message
        # log the issue and the kwargs
        pass

    def final_message(self):
        msg = {'message': self.message, 'code': self.code, 'title': self.title}
        return msg

    def __repr__(self):
        dict_repr = self.__dict__
        dict_repr['class'] = self.__class__.__name__
        return str(dict_repr)


# General templates:


class BadRequest(MyBaseException):
    msg_fmt = 'Bad request'
    title = 'Bad request'
    code = 400


class Unauthorized(MyBaseException):
    msg_fmt = 'Not authorized.'
    title = 'Unauthorized'
    code = 401


class Forbidden(MyBaseException):
    msg_fmt = 'Access forbidden.'
    title = 'Forbidden'
    code = 403


class ItemNotFound(MyBaseException):
    msg_fmt = 'Resource could not be found.'
    title = 'Not Found'
    code = 404


class Conflict(MyBaseException):
    msg_fmt = 'Resource already exists.'
    title = 'Conflict'
    code = 409


class InvalidJsonScheme(BadRequest):
    msg_fmt = '%(scheme_error)s'


class InvalidInput(BadRequest):
    msg_fmt = '%(input_error)s'


# Specific exceptions

class UserNotFound(ItemNotFound):
    msg_fmt = 'User %(user_id)s could not be found.'


class UserEmailAlreadyExist(BadRequest):
    msg_fmt = 'User with email %(email)s already exists.'


# Specific exceptions (new for Multi-Tenant Warehouse)

class TenantNotFound(ItemNotFound):
    msg_fmt = 'Tenant %(tenant_id)s could not be found.'


class TenantNameAlreadyExist(Conflict):
    msg_fmt = 'Tenant with name %(name)s already exists.'


class WarehouseNotFound(ItemNotFound):
    msg_fmt = 'Warehouse %(warehouse_id)s could not be found.'


class WarehouseNameAlreadyExist(Conflict):
    msg_fmt = 'Warehouse with name %(name)s already exists for tenant %(tenant_id)s.'


class ProductNotFound(ItemNotFound):
    msg_fmt = 'Product %(product_id)s could not be found.'


class ProductSKUAlreadyExist(Conflict):
    msg_fmt = 'Product with SKU %(sku)s already exists.'


class RestockLogInvalidQuantity(BadRequest):
    msg_fmt = 'Restock log request has invalid quantity %(quantity)i. Quantity must be a positive integer.'


class AnalyticsInvalidThreshold(BadRequest):
    msg_fmt = 'Invalid low stock threshold %(threshold)i. Threshold must be a not negative integer.'


# ====

class WarehousePermissionNotFound(ItemNotFound):
    msg_fmt = 'Warehouse permission %(permission_id)s could not be found.'


class WarehousePermissionAlreadyExist(Conflict):
    msg_fmt = 'Permission for user %(user_id)s to warehouse %(warehouse_id)s already exists.'


class InvalidRole(BadRequest):
    msg_fmt = 'Invalid role: %(role)s.'


class TenantUserMismatch(BadRequest):
    msg_fmt = 'User %(user_id)s does not belong to tenant %(tenant_id)s.'


class CrossTenantOperationForbidden(Forbidden):
    msg_fmt = 'Operation across tenants is forbidden.'


class SystemAdminTenantAssociationForbidden(BadRequest):
    msg_fmt = 'System admin users cannot be associated with a tenant.'


class RegularUserCannotCreateUsers(Forbidden):
    msg_fmt = 'Regular users cannot create new users.'


class TenantAdminCannotCreateSystemAdmins(Forbidden):
    msg_fmt = 'Tenant administrators cannot create system administrators.'


class TenantAdminCannotManageOtherTenants(Forbidden):
    msg_fmt = 'Tenant administrator cannot manage resources of other tenants.'


class UserNotRegular(BadRequest):
    msg_fmt = 'Permissions can only be assigned to regular users.'


class CannotAssignPermissionToSystemAdmin(BadRequest):
    msg_fmt = 'Cannot assign warehouse permissions to system administrators.'


class PermissionTenantMismatch(BadRequest):
    msg_fmt = 'Permission tenant ID mismatch with user or warehouse tenant ID.'
