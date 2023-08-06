##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .LoginServer import login as oauth_login
from .HoldoverTime import HoldoverTime
from .Workloads import Workloads
from requests.exceptions import ConnectionError

import phonenumbers

# Generic Operating System Services
import datetime, json, os
from typing import Union

# Optumi imports
import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    ServiceException,
    OptumiException,
)

DEBUG_LOGIN = False

# We will keep various lists from the controller in place of enums
_machines = None
_providers = None
_graphics_card_types = None


def machines():
    """Returns the current list of machines from inventory.

    Returns:
        list of str: Available machine sizes as strings
    """
    if _machines is None:
        _update_inventory_info()
    return _machines


def providers():
    """Returns the current list of providers from inventory.

    Returns:
        list of str: Available cloud providers as strings
    """
    if _providers is None:
        _update_inventory_info()
    return _providers


def graphics_card_types():
    """Returns the current list of graphics card types from inventory.

    Returns:
        list of str: Available GPP card types as strings
    """
    if _graphics_card_types is None:
        _update_inventory_info()
    return _graphics_card_types


def _update_inventory_info():
    global _machines, _providers, _graphics_card_types

    user_information = json.loads(optumi.core.get_user_information(True).text)

    _machines = []
    _providers = []
    _graphics_card_types = []

    for machine in user_information["machines"]:
        name = machine["name"]
        provider = name.split(":")[0]
        graphics_card_type = machine["graphicsCardType"]

        if not machine in _machines:
            _machines.append(name)

        if not provider in _providers:
            _providers.append(provider)

        if not graphics_card_type in _graphics_card_types:
            _graphics_card_types.append(graphics_card_type)

    _machines.sort()
    _providers.sort()
    _graphics_card_types.sort()


def login(
    connection_token=None,
    save_token=True,
):
    """Logs in to the optumi platform. If a connection token is provided as an argument or found on the disk, that is used to complete the login, otherwise a new browser tab is opened to prompt for credentials.

    Args:
        connection_token (str, optional): An optumi correction token (can be found in the webapp). Defaults to None.
        save_token (bool, optional): Whether to store the login token on disk. Defaults to True.

    Raises:
        NotLoggedInException: If login was unsuccessful
        OptumiException: If we could not perform the browser login
    """
    dnsName = optumi.utils.get_portal()
    port = optumi.utils.get_portal_port()

    # On a dynamic machine we do not need to get an okta token
    if optumi.utils.is_dynamic():
        if DEBUG_LOGIN:
            print("Dynamic login")
        if not optumi.login.check_login(dnsName, port):
            if DEBUG_LOGIN:
                print("Not logged in")
            login_status, message = optumi.login.login_rest_server(
                dnsName,
                port,
                "",
                login_type="dynamic",
                save_token=save_token,
            )
    else:
        if DEBUG_LOGIN:
            print("Normal login")
        if not optumi.login.check_login(dnsName, port):
            if DEBUG_LOGIN:
                print("Not logged in")
            if connection_token == None:
                if DEBUG_LOGIN:
                    print("No connection token")
                if DEBUG_LOGIN:
                    print("Trying login with disk token")
                # Try to log in with the login token from the disk
                login_status, message = optumi.login.login_rest_server(
                    dnsName, port, login_type="token", save_token=save_token
                )

                # Fall back on the browser login
                if login_status != 1:
                    if DEBUG_LOGIN:
                        print("Trying browser login")
                    try:
                        login_status, message = optumi.login.login_rest_server(
                            dnsName,
                            port,
                            oauth_login(),
                            login_type="oauth",
                            save_token=save_token,
                        )
                        if login_status != 1:
                            raise NotLoggedInException("Login failed: " + message)
                    except RuntimeError:
                        raise OptumiException(
                            "Unable to perform browser login from Notebook. Try logging in with a connection token as shown here: https://optumi.notion.site/Login-using-a-connection-token-710bccdeaf734cbf825aae94b79a8109"
                        )
            else:
                if DEBUG_LOGIN:
                    print("Connection token")
                login_status, message = optumi.login.login_rest_server(
                    dnsName,
                    port,
                    connection_token,
                    login_type="token",
                    save_token=save_token,
                )
                if login_status != 1:
                    raise NotLoggedInException("Login failed: " + message)

    user_information = json.loads(optumi.core.get_user_information(True).text)

    print("Logged in", user_information["name"])


def logout(remove_token=True):
    """Logs out of the Optumi service and optionally remove the associated token.

    Args:
        remove_token (bool, optional):  If set to True, will remove the associated token on logout. Defaults to True.
    """
    try:
        optumi.login.logout(remove_token=remove_token)
    except NotLoggedInException:
        pass


def get_phone_number():
    """Retrieve the user's phone number.

    Returns:
        str: the user's phone number
    """
    return json.loads(optumi.core.get_user_information(False).text)["phoneNumber"]


def set_phone_number(phone_number):
    """Prompts the user for a verification code and sets user's phone number.

    Args:
        phone_number (str): The phone number with which the user wants to set

    Raises:
        OptumiException: If the phone number is invalid or the verification code is not correct
    """
    if phone_number == "":
        optumi.core.clear_phone_number()
    else:
        number = phonenumbers.parse(phone_number, "US")
        if not phonenumbers.is_valid_number(number):
            raise OptumiException(
                "The string supplied did not seem to be a valid phone number."
            )

        formatted_number = phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.E164
        )

        optumi.core.send_verification_code(formatted_number)

        while True:
            code = input("Enter code sent to " + formatted_number + ": ")
            text = optumi.core.check_verification_code(formatted_number, code).text

            if text:
                print(text)
                # This is kind of sketchy but wont break if the message changes, it will just continue prompting the user for their code
                if text == "Max check attempts reached":
                    break
            else:
                optumi.set_user_information("notificationsEnabled", True)
                break


def get_holdover_time():
    """Get the current holdover time. Holdover time is the period of time machines are kept active (provisioned) after a workload finishes. Holdover time is global and applies to all workloads.

    Returns:
        HoldoverTime: the holdover time
    """
    res = optumi.core.get_user_information(False)
    return HoldoverTime(
        int(
            json.loads(optumi.core.get_user_information(False).text)["userHoldoverTime"]
        )
        // 60  # Convert to minutes
    )


def set_holdover_time(holdover_time: Union[int, HoldoverTime]):
    """Set the holdover time. Holdover time is the period of time machines are kept active (provisioned) after a workload finishes. Holdover time is global and applies to all workloads.

    Args:
        holdover_time (Union[int, HoldoverTime]): Holdover time as either an int representing minutes or a HoldoverTime object.
    """
    optumi.core.set_user_information(
        "userHoldoverTime",
        str(
            holdover_time.seconds
            if type(holdover_time) is HoldoverTime
            else holdover_time * 60  # Convert to seconds
        ),
    )


def get_connection_token():
    """Returns a dictionary representing the connection token in the format {'expiration': '<ISO 8601 string>', 'token': '<token string>'}"""
    return json.loads(optumi.core.get_connection_token(False).text)


def redeem_signup_code(signupCode):
    """Redeems a signup code used for accessing the optumi API.

    Args:
        signupCode (str): Signup code given by Optumi.
    """
    optumi.core.redeem_signup_code(signupCode)


def send_notification(message, details=True):
    """Sends a notification via text message, to the number associated with the user running this command.
    Optionally, additional details about the workload will be attached to the end of the message given as the first parameter (if this is called from a dynamic machine).
    If no phone number is associated with the user, a warning message will be printed to console instead.

    Args:
        message (str): the message to send as a string
        details (bool, optional): Wether to include details about the current workload (if this is called from a dynamic machine). Defaults to True.
    """
    if get_phone_number():
        optumi.core.send_notification(
            "From " + str(Workloads.current()) + ": " + message
            if details and optumi.utils.is_dynamic()
            else message
        )
    else:
        print("Unable to send notification - no phone number specified")
