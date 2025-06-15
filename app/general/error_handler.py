import os
import shutil  # для удаления папки
import sqlite3


def get_description_and_solution(error: str):
    description_and_solution = []


    if (error == 'PhoneNumberInvalidError' or error == 'UsernameOccupiedError' or error == 'AuthKeyUnregisteredError'
          or error == 'TimeoutError' or error == 'TypeError' or error == 'ConnectionError' or error == 'AttributeError'):
        description_and_solution.append('Устаревшие данные для входа')
        description_and_solution.append('Войдите в tg аккаунт и добавьте новую tdata в программу')
    elif error == 'UserDeactivatedBanError' or error =='ChatNotFound':# ChatNotFound может возникнуть когда аккаунт заблокирован и тем самым он не может найти чат
        description_and_solution.append('Аккаунт заблокирован')
        description_and_solution.append('Удалите аккаунт')
    elif error == 'SessionPasswordNeededError':
        description_and_solution.append('У аккаунта установленна двухфакторная аутентификация')
        description_and_solution.append('Уберите её')
    elif error == 'FloodWaitError' or error == "PeerFloodError" or error == "UserRestrictedError":
        description_and_solution.append('Аккаунт получил спам-блок')
        description_and_solution.append('Добавьте аккаунт в активные через 24 часа или ранее')
    elif error == 'TFileNotFound':
        description_and_solution.append('Файл с данными для входа не найден')
        description_and_solution.append('Удалите аккаунт и добавьте новую tdata')
    else:
        description_and_solution.append('Неизвестная ошибка')
        description_and_solution.append('если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу')

    return description_and_solution  # вернёт ошибку и её решение

def error_handler(error: str,id_folder: int,account_type: str)-> list: # необходимо его вызывать

    description_and_solution = get_description_and_solution(error)

    if error == 'FloodWaitError' or error == "PeerFloodError":
        temporary_ban = _change_folder(id_folder, account_type, 'temporary_ban')
        _change_db(id_folder, account_type, temporary_ban,'temporary_ban', description_and_solution)
    elif (error == 'PhoneNumberInvalidError' or error == 'UsernameOccupiedError' or error == 'AuthKeyUnregisteredError'
          or error == 'TimeoutError' or error == 'UserDeactivatedBanError' or error == 'SessionPasswordNeededError'
            or error == 'TypeError' or error == 'ConnectionError' or error == 'AttributeError'):
        id_in_login_error = _change_folder(id_folder, account_type,'login_error')
        _change_db(id_folder, account_type, id_in_login_error, 'login_error', description_and_solution)
    else:
        id_in_login_error = _change_folder(id_folder, account_type,'login_error')
        _change_db(id_folder, account_type, id_in_login_error,'login_error', description_and_solution)

    return description_and_solution

def _change_folder(id_folder: int,account_type: str, target_account_type: str):
    root_project_dir = '..'


    folder_path = root_project_dir + f'/accounts/{account_type}_accounts'

    directory_name = folder_path + "/" + str(id_folder)
    os.rename(directory_name, directory_name + "_copy")  # переименовываем
    directory_name = directory_name + "_copy"
    shutil.copytree(directory_name, root_project_dir + f'/accounts/{target_account_type}_accounts/{str(id_folder)}_copy')  # копирование
    shutil.rmtree(directory_name)

    counter_folder = 0  # отображает кол-во папок которые есть в target_account_type
    while True:
        directory_name = root_project_dir + f"/accounts/{target_account_type}_accounts/{counter_folder}"
        if os.path.isdir(directory_name):
            counter_folder += 1
        else:
            break

    os.rename(root_project_dir + f'/accounts/{target_account_type}_accounts/{str(id_folder)}_copy',
              root_project_dir + f"/accounts/{target_account_type}_accounts/{counter_folder}")  # переименовываем

    while True:  # переименовываем папки откуда скопировали
        id_folder += 1
        old_directory_name = folder_path + "/" + str(id_folder)
        if os.path.isdir(old_directory_name):
            os.rename(old_directory_name, folder_path + "/" + str(id_folder - 1))  # переименовываем
        else:
            break
    return counter_folder  # возвращает новый id который присвоили в login_error


def _change_db(id: int,account_type: str, id_in_target_type: int, target_account_type: str, error_description_solution: list):
    root_project_dir = '..'

    connection = sqlite3.connect(root_project_dir + '/working_files/data_base.sqlite3')
    cursor = connection.cursor()

    cursor.execute(f"UPDATE accounts SET id = ?, account_status = ?,error = ?, solution_error = ?  WHERE id = ? AND account_status = ?",
        (id_in_target_type, target_account_type, error_description_solution[0], error_description_solution[1], id, account_type))
    connection.commit()  # сохранение
    # удаление данных из БД

    while True:
        id += 1
        cursor.execute(f"SELECT id FROM accounts WHERE id = ? AND account_status = ? ", (id, account_type))
        account_from_db = cursor.fetchone()
        if account_from_db:  # если такая строка есть в БД
            cursor.execute(f"UPDATE accounts SET id = ?  WHERE id = ? AND account_status = ?",
                           (id - 1, id, account_type))
            connection.commit()  # сохранение
        else:
            break

    connection.close()