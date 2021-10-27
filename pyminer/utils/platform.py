import os
import sys


def is_windows_platform():
    """
    Function to check, if this is a Windows platform.

    @return flag indicating Windows platform (boolean)
    """
    return sys.platform.startswith(("win", "cygwin"))


def is_mac_platform():
    """
    Function to check, if this is a Mac platform.

    @return flag indicating Mac platform (boolean)
    """
    return sys.platform == "darwin"


def is_linux_platform():
    """
    Function to check, if this is a Linux platform.

    @return flag indicating Linux platform (boolean)
    """
    return sys.platform.startswith("linux")



def is_kde_desktop():
    """
    Function to check, if the current session is a KDE desktop (Linux only).

    @return flag indicating a KDE desktop
    @rtype bool
    """
    if not is_linux_platform():
        return False

    isKDE = False

    desktop = (
            os.environ.get("XDG_CURRENT_DESKTOP", "").lower() or
            os.environ.get("XDG_SESSION_DESKTOP", "").lower() or
            os.environ.get("DESKTOP_SESSION", "").lower()
    )
    if desktop:
        isKDE = "kde" in desktop or "plasma" in desktop
    else:
        isKDE = bool(os.environ.get("KDE_FULL_SESSION", ""))

    return isKDE


def is_gnome_desktop():
    """
    Function to check, if the current session is a Gnome desktop (Linux only).

    @return flag indicating a Gnome desktop
    @rtype bool
    """
    if not is_linux_platform():
        return False

    isGnome = False

    desktop = (
            os.environ.get("XDG_CURRENT_DESKTOP", "").lower() or
            os.environ.get("XDG_SESSION_DESKTOP", "").lower() or
            os.environ.get("GDMSESSION", "").lower()
    )
    if desktop:
        isGnome = "gnome" in desktop
    else:
        isGnome = bool(os.environ.get("GNOME_DESKTOP_SESSION_ID", ""))

    return isGnome

