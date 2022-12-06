


@Given('Пользователь авторизован с ролью "{role}"')
def step_impl(context, role):
    if role.upper() == 'SUPERADMIN':
        jwt_decode = context.management.decode_jwt(context.management_super_token)
        role = 'Суперадмин'
    elif role == 'Сотрудник ТСП':
        jwt_decode = context.management.decode_jwt(context.tsp_management_token)
        role = 'Сотрудник торгового предприятия'
    elif role == 'Сотрудник ОИВ':
        jwt_decode = context.management.decode_jwt(context.oiv_management_token)
        role = 'Сотрудник социального учреждения'
    assert jwt_decode['role'] == role, 'У авторизованного пользователя не верная роль {0}, ожидалась в ответе {1}'.format(jwt_decode['role'])