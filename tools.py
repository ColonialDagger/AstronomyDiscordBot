from configparser import ConfigParser


def import_configs(config_file='config.ini'):
    config = ConfigParser()
    config.read(config_file)
    return config


def savefile(text, dir):
    """
    Saves/overwrites file.

    Parameters
    -----------
    text: `list`|`str`|`Response`
        Content representing each line of file to be written.

    dir: :class:`str`
        String path of file.
    """
    with open(dir, 'w') as f:
        for item in text:
            f.write("%s\n" % item)
    return


def appendfile(text, dir):
    """
    Appends text to file.

    Parameters
    -----------
    text: :class:`list`
        List representing each line of file to be written.

    dir: :class:`str`
        String path of file.
    """
    with open(dir, 'a') as f:
        for str in text:
            f.write(str)


def readfile(dir):
    """
    Reads file, returns list of each line.

    Parameters
    -----------
    dir: :class:`str`
        String path of file.
    """
    try:
        with open(dir) as f:
            return [line[:-1] for line in f.readlines()]
    except FileNotFoundError:
        print('Error! File' + str(dir) + ' not found.\n')
