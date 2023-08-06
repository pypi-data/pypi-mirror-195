import re


def return_of_response(code:int = 500, status:str = "error", message:str = "No Response", message_detail:str = None, data:list = None,):
    """Membuat response dari request dengan otomatis dengan memasukan parameternya.
    code => untuk response ex: 200, 500, 400, 404, 403 dll
    status => status response seperti success, warning, error
    message => message dar response
    message_detail => detail message yang akan digunakan untuk masuk kedalam history
    data => jika ada response data maka diisi
    """
    return {"code": code, "status": status, "message": message, "messageDetail": message_detail, "data": data}

def additional_response(rows_count:int = None, headers:list = None, footers:dict = None, data_footers:list = None):
    """Tambahan dari return_of_response
    rows_count => jumlah datanya
    headers => headers untuk datatable
    footers => footers untuk datatable
    data_footers => data footers untuk datatble
    
    """
    return {"rowsCount": rows_count, "dataTable": {"headers": headers, "footers": footers}, "dataFooters": data_footers}

def build_message_detail(tipe:int = None, old_data:str = None, new_data:str = None, action:str = None, menu_name:str = None, params_value:list = None, data_name:str = None, params_char:list = None, target:str = None):
    """Digunakan untuk membuat message dan message detail
    tipe => tipe terdiri dari 1, 2, 3 dan 4, 1 utuk action view, 2 untuk insert, 3 untuk update, 4 untuk delete
    old_data => data lama
    new_data => data baru 
    action => aksi dalam bentuk string
    menu_name => nama menunya ketika melakukan event
    param_values => param yang digunakan untuk melakukan action
    data_name => data yang menjadi acuan action
    params_char => parameter yang digunakan
    target => target colom untuk update

    """
    message, message_detail = None, None
    if tipe == 1:
        message = f"{action} {menu_name}"
        message_detail = f"{menu_name} => {action} => Params {params_char} :{params_value if params_value else ''}"
    elif tipe == 2:
        message = f" {data_name} successfully {action} "
        message_detail = f"{menu_name} => {action} => {params_value if params_value else ''}"
    elif tipe == 3:
        message = f"{data_name} successfully {action}"
        message_detail = f"{menu_name} => {action} => Target {target} by Params {params_char} :{old_data} to {new_data}"
    elif tipe == 4:
        message = f"{data_name} successfully {action}"
        message_detail = f"{menu_name} => {action} => Params {params_char} :{params_value}"
    return message, message_detail

def generate_headers(title:list = None, data_index:list = None, isview:list = None):
    """untuk membuat header pada datatable
    title => name header kolomn
    data_index => taget data yang akan diambil
    isview => status akan di tampilkan atau tidak
    
    """
    if not title or not data_index or not isview or len(title) != len(data_index) != len(isview):
        return []
    headers = [{"dataIndex": data_idx, "title": title_idx, "isView": isview_idx} for data_idx, title_idx, isview_idx in zip(data_index, title, isview)] 
    return headers


def generate_footers(title:list = None, data_index:list = None, isview:list = None):
    """untuk membuat header pada datatable
    title => name header kolomn
    data_index => taget data yang akan diambil
    isview => status akan di tampilkan atau tidak
    
    """
    if not title or not data_index or not isview or len(title) != len(data_index) != len(isview):
        return []
    footers = [{"dataIndex": data_idx, "title": title_idx, "isView": isview_idx} for data_idx, title_idx, isview_idx in zip(data_index, title, isview)] 
    return footers


def datatables_view(cursor_connection:str = None, logger:str = None, tablename:str = None, target_column:list = None, column_name:list = None, values:list = None, limit:int = None, page:int = None, order:str = None, 
                        order_tipe:str = None, tipe:int = None, group_values:list = None, disable_row_count:bool = None, menu_name:str = None):
    """Untuk melakukan query datatable
    cursor_connection => cursor koneksi kedatabase
    logger => logger dimana untuk menyimpan log saat error
    tablename => nama table dalam bentuk string
    target_colum => column apa saja yang akan dikeluarkan bisa * atau spesifik dalam bentuk list string seperti ["name","password"]
    column_name => column yang digunakan untuk where dalam bentuk list string seperti ["name","password"]
    values => values dari where pada column name dalam bentuk list string seperti ["name","password"]
    limit => limit dari query
    page => offsetnya
    order => order dengan nama column yang ingin diorder
    order_tipe => tipe ordernya yaitu asc dan desc
    tipe => tipe hasil query, 1 => 1 baris
    group_values => grouping jika dibutuhkan biasanya digunakan saat melakukan perhitungan dalam bentuk list string seperti ["name","password"]
    disable_row_count => jika True maka tidak akan melakukan query penghitungan jumlah rownya jadi akan hemat waktu
    menu_name => nama menu saat melakukan query dan konek ke logger
    """
    data = None
    rows_count = 0
    valid_target = ", ".join(target_column) if target_column else "*"
    valid_columns = " AND ".join([f"{column}=%s" for column in column_name]) if column_name else ""
    valid_limit = f"LIMIT {limit}" if limit else ""
    valid_offset = f"OFFSET {limit * (page)}" if page and limit else ""
    valid_group = " ,".join([f"{group}" for group in group_values]) if group_values else ""
    valid_order = f"ORDER BY {order} {order_tipe}" if order and order_tipe else ""


    query = f"SELECT {valid_target} FROM {tablename}"
    if column_name:
        query += f" WHERE {valid_columns}"
    query_total = query
    query_total += f"{' GROUP BY ' if group_values else ''} {valid_group} "
    query += f"{' GROUP BY ' if group_values else ''} {valid_group} {valid_order} {valid_limit} {valid_offset}"
    with cursor_connection() as cursor:
        try:
            cursor.execute(query, tuple(values) if values else None)
            data = cursor.fetchall() if not tipe else cursor.fetchone()
            logger.handlers.clear()
            if not disable_row_count:
                cursor.execute(query_total, tuple(values) if values else None)
                rows_count = len(cursor.fetchall()) if not tipe else 1
                add_response = additional_response(rows_count= rows_count)
                response = return_of_response(code= 200, status= "success", data= data)
                return {**response, **add_response}
            return return_of_response(code= 200, status= "success", data= data)
        except Exception as e:
            error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
            logger.error(f"||{menu_name}|| {error_message}")
            logger.handlers.clear()
            return return_of_response(message= "Internal Server Error", message_detail= str(e))
        
   
def check_existing_data(cursor_connection:str = None, logger:str = None,tablename:str = None, column_name:list = None, values:list = None, tipe:int = None, lower_status:list = None, menu_name:str = None):
    """Untuk melakukan query datatable
    cursor_connection => cursor koneksi kedatabase
    logger => logger dimana untuk menyimpan log saat error
    tablename => nama table dalam bentuk string
    column_name => column yang digunakan untuk where dalam bentuk list string seperti ["name","password"]
    values => values dari where pada column name dalam bentuk list string seperti ["name","password"]
    tipe => tipe hasil query, 1 => 1 baris
    lower_status => apakah valuenya akan mengalami lower character ex: [True,False]
    menu_name => nama menu saat melakukan query dan konek ke logger
    """
    query = f"select * from {tablename} "
    if column_name and values and (len(column_name) == len(values)):
        query += F"WHERE {' AND '.join([f'LOWER({column}) = lower(%s)' if lower else f'{column} = %s' for column, lower in zip(column_name, lower_status)])}"
    with cursor_connection() as cursor:
        try:
            cursor.execute(query, tuple(values))
            logger.handlers.clear()
            return return_of_response(code= 200, status= "success", message= None, data= cursor.fetchone() if tipe == 1 else cursor.fetchall())
        except Exception as e:
            error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
            logger.error(f"||{menu_name}|| {error_message}")
            logger.handlers.clear()
            return return_of_response(message= "Internal Server Error", message_detail= str(e))


def insert_data(cursor_connection:str = None, logger:str = None,tablename:str = None, column_name:list = None, values:list = None, commit_status:bool = False, menu_name:str = None):
    """Untuk melakukan query datatable
    cursor_connection => cursor koneksi kedatabase
    logger => logger dimana untuk menyimpan log saat error
    tablename => nama table dalam bentuk string
    column_name => column yang digunakan untuk insert dalam bentuk list string seperti ["name","password"]
    values => values dari insert pada column name dalam bentuk list string seperti ["name","password"]
    commit_status => jika True maka akan commit
    menu_name => nama menu saat melakukan query dan konek ke logger
    """
    string_val = ", ".join(["%s"] * len(values))
    column_dec = ", ".join(f"{clm}" for clm in column_name)
    query = f"insert into  {tablename} ({column_dec}) values ({string_val})"
    with cursor_connection(commit= commit_status) as cursor:
        try:
            cursor.execute(query, tuple(values))
            logger.handlers.clear()
            return return_of_response(code= 200, status= "success", message= None)
        except Exception as e:
            error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
            logger.error(f"||{menu_name}|| {error_message}")
            logger.handlers.clear()
            return return_of_response(message= "Internal Server Error", message_detail= str(e))

def update_data(cursor_connection:str = None, logger:str = None,tablename:str = None, update_column:list = None, where_column:list = None, commit_status:bool = False, values:list = None, menu_name:str = None):
    """Untuk melakukan query datatable
    cursor_connection => cursor koneksi kedatabase
    logger => logger dimana untuk menyimpan log saat error
    tablename => nama table dalam bentuk string
    update_column => column yang digunakan untuk target update dalam bentuk list string seperti ["name","password"]
    where_column => colum yang digunakan menjadi where nya dimana  dalam bentuk list string seperti ["name","password"]
    values => values dari update pada column name dalam bentuk list string seperti ["name","password"]
    commit_status => jika True maka akan commit
    menu_name => nama menu saat melakukan query dan konek ke logger
    """
    update_col = ", ".join(f"{clm} = %s " for clm in update_column)
    valid_columns = " AND ".join([f"{column}=%s" for column in where_column]) if where_column else ""

    query = f"update {tablename} set {update_col} "
    if where_column:
        query += f" WHERE {valid_columns}"
    with cursor_connection(commit= commit_status) as cursor:
        try:
            cursor.execute(query, tuple(values))
            logger.handlers.clear()
            return return_of_response(code= 200, status= "success", message= None)
        except Exception as e:
            error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
            logger.error(f"||{menu_name}|| {error_message}")
            logger.handlers.clear()
            return return_of_response(message= "Internal Server Error", message_detail= str(e))

def delete_data(cursor_connection:str = None, logger:str = None,tablename:str = None, delete_column:list = None, values:list = None, commit_status:bool = False, menu_name:str = None):
    """Untuk melakukan query datatable
    cursor_connection => cursor koneksi kedatabase
    logger => logger dimana untuk menyimpan log saat error
    tablename => nama table dalam bentuk string
    delete_column => colum yang digunakan menjadi where nya dimana  dalam bentuk list string seperti ["name","password"]
    values => values dari delete pada column name dalam bentuk list string seperti ["name","password"]
    commit_status => jika True maka akan commit
    menu_name => nama menu saat melakukan query dan konek ke logger
    """
    query = f"delete from {tablename} "
    valid_columns = " AND ".join([f"{column}=%s" for column in delete_column]) if delete_column else ""
    if delete_column:
        query += f" WHERE {valid_columns}"
    with cursor_connection(commit= commit_status) as cursor:
        try:
            cursor.execute(query, tuple(values))
            logger.handlers.clear()
            return return_of_response(code= 200, status= "success", message= None)
        except Exception as e:
            error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
            logger.error(f"||{menu_name}|| {error_message}")
            logger.handlers.clear()
            return return_of_response(message= "Internal Server Error", message_detail= str(e))
        

def validate(username:str = None, password:str = None):
    """untuk memvalidasi username dan password
    username => usrnamenya
    password => passwordnya
    
    """
    pattern = r"[^A-Za-z0-9_]"
    match = re.search(pattern, username)
    if len(str(username)) < 8:
        return return_of_response(code= 400, message= "The length of the username is less than eight character")
    elif len(str(username)) > 20:
        return return_of_response(code= 400, message= "The length of the username is more than twenty character")
    elif match:
        return return_of_response(code= 400, message= "Username have special character")
    elif any(char.isupper() for char in username):
        return return_of_response(code= 400, message= "Username must be lowercase")

    if password:
        if len(str(password)) < 8:
            return return_of_response(code= 400, message= "The length of the password is less than eight character ")
        else:
            if not any(char.isdigit() for char in password):
                password = False
                return return_of_response(code= 400, message= "Password must have one digit of number")
            if not any(char.isupper() for char in password):
                password = False
                return return_of_response(code= 400, message= "Password must have one capital letter")
            if not any(char.islower() for char in password):
                password = False
                return return_of_response(code= 400, message= "Password must have one lowercase letter")
    return return_of_response(code= 200, status= "success", message= None)
    