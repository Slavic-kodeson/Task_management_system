from email.mime.text import MIMEText


def validate_file(filename, filesize, get_config_field):
    file_extension = filename.split('.')[-1] if "." in filename else None

    valid_extension: bool = file_extension in get_config_field("extensions")
    valid_filesize: bool = filesize <= get_config_field("filesize_max")

    return valid_extension & valid_filesize, file_extension


def add_text():
    pass


def add_file():
    pass


def remove_text():
    pass
