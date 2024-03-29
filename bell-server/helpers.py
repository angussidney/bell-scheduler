def system_wide_template_variables():
    return dict(
        docs="https://angussidney.github.io/bell-scheduler/#"
    )


def check_file(file, filetype):
    # Todo: properly check filetype (not just extension)
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == filetype


weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
