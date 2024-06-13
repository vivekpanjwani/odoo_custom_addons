import xmlrpc.client

url = 'http://0.0.0.0:9015'
db = 'Vivek'
username = 'admin'
password = 'admin'


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid:
    print("Authentication Success")
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # search method
    manager_ids = models.execute_kw(db, uid, password, 'emp.model', 'search' ,[[['is_manager','=', True]]],{'offset': 1, 'limit': 3})
    print("---Manager Ids----->>", manager_ids)

    # read method
    if manager_ids:
        # fields_to_read = ['name', 'is_manager']  # Replace with the fields you want to read
        manager_rec = models.execute_kw(db, uid, password, 'emp.model', 'read' ,[manager_ids], {'fields': ['id', 'name']})
        print("----Manager Fields---->>", manager_rec)

    # search count method
    manager_count = models.execute_kw(db, uid, password, 'emp.model', 'search_count' ,[[['is_manager','=', True]]])
    print("-----Manager Count---->>", manager_count)

    # list records using fields_get()
    manager_field_get = models.execute_kw(db, uid, password, 'emp.model', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
    print("-----Manager Records fields_get---->>", manager_field_get)

    # search_read method
    manager_search_read = models.execute_kw(db, uid, password, 'emp.model', 'search_read', [[['is_manager', '=', True]]], {'fields': ['name', 'country_id'], 'limit': 5})
    print("-----Manager search_read fields---->>", manager_search_read)

    # create new record
    # id = models.execute_kw(db, uid, password, 'emp.model', 'create', [{'name': "Jackyyyyyyy",'phone': "9999999999"}])
    # print("New Record", id)

    # update records
    # up_record = models.execute_kw(db, uid, password, 'emp.model', 'write', [[54], {'name': "Oggyy"}])
    # # get record name after having changed it
    # get_updated_rec = models.execute_kw(db, uid, password, 'emp.model', 'name_get', [[54]])
    # print("----------Updated Record------------>>", get_updated_rec)

    # delete record
    # delete_rec = models.execute_kw(db, uid, password, 'emp.model', 'unlink', [[56]])
    # # check if the deleted record is still in the database
    # check_rec = models.execute_kw(db, uid, password, 'emp.model', 'search', [[['id', '=', 56]]])
    # print("-----Deleted Record----->", check_rec)

    # models.execute_kw(db, uid, password, 'ir.model', 'create', [{
    #     'name': "Custom Model",
    #     'model': "x_custom_model",
    #     'state': 'manual',
    # }])
    # models.execute_kw(db, uid, password, 'x_custom_model', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
    emp_read_group = models.execute_kw(db, uid, password, 'emp.model', 'read_group', [()] ,{'fields': ['name', 'id'], 'limit': 6 , 'groupby': ['partner_id']})
    print("-----Employee emp_read_group fields---->>", emp_read_group)

else:
    print("Authentication Failed")