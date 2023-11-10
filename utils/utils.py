def format_file_size(size, decimals=2):
    """Convert byte to relevant user readable size"""
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']
    largest_unit = 'YB'
    step = 1024

    for unit in units:
        if size < step:
            return ('%.' + str(decimals) + 'f %s') % (size, unit)
        size /= step

    return ('%.' + str(decimals) + 'f %s') % (size, largest_unit)