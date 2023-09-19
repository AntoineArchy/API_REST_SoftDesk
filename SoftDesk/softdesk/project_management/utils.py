def parse_url(url):
    """
    Analyse une URL pour extraire les identifiants des ressources.

    Args:
        url (str): URL à analyser.

    Returns:
        dict: Dictionnaire contenant les identifiants des ressources.
    """
    parsed_url = dict()
    split_url = url.split('/')
    for url_idx, url_part in enumerate(split_url):
        if not url_part.isdigit():
            continue
        parsed_url[f"{split_url[url_idx - 1]}_id"] = url_part
    return parsed_url
