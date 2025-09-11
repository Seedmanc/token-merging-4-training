def remove_blacklisted(tags, blacklist):
    """Remove tags in the blacklist."""
    return [tag for tag in tags if tag not in blacklist]