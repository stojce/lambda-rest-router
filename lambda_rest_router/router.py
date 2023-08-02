""" AWS Lambda Router module """

import re
from functools import lru_cache
import importlib
import base64
import json

AVAILABLE_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

# pylint: disable=too-few-public-methods
class LambdaRouter:
    """
    AWS Lambda router.
    """

    def __init__(self, routes):
        if len(routes) == 0:
            raise KeyError("No routes defined")

        self.routes = routes

    def __get_matching_route(self, path, method):
        if method not in AVAILABLE_METHODS:
            raise KeyError(f"Method {method} is not supported")

        possible_routes = self.__compiled_routes().get(
            self.__get_route_hash_from_path(path)
        )

        for route in possible_routes:
            reg_arr = []
            path_parts = route.split("/")
            for part in path_parts:
                if part.startswith("<"):
                    reg_arr.append(f"(?P{part}[^/]*)")
                else:
                    reg_arr.append(part)
            regex_pattern = r"\/".join(reg_arr)
            if match := re.fullmatch(regex_pattern, path):
                if route_call := self.routes[route].get(method):
                    return route_call, match.groupdict()

        raise KeyError(f"Route {path} with method {method} not found")

    def __get_route_hash_from_path(self, path):
        route_parts = path.split("/")
        return f"{route_parts[0]}_{str(len(route_parts) - 1)}"

    def __extract_params(self, event):
        path = event["pathParameters"]["proxy"]
        method = event["requestContext"]["http"]["method"]

        query_string = event.get("queryStringParameters", {})
        body_str = event.get("body", "{}")
        if body_str and event.get("isBase64Encoded"):
            body_str = base64.b64decode(body_str)
        body = json.loads(body_str)
        request = {**query_string, **body}

        return path, method, request

    @lru_cache
    def __compiled_routes(self) -> dict:
        """
        Returns a dictionary of route hashes and their associated routes.
        The function iterates over the values of the `routes` dictionary and splits
        each route by the forward slash ("/").
        It then creates a unique hash for each route based on the first part of the
        route and the number of parts in total.
        If the hash does not exist in the `route_hashes` dictionary, it adds an empty
        list for that hash.
        It then appends the route to the list associated with the hash.
        Finally, it returns the `route_hashes` dictionary.

        :return: A dictionary containing route hashes and their associated routes.
        :rtype: dict
        """
        route_hashes = {}

        for route in self.routes.keys():
            route_hash = self.__get_route_hash_from_path(route)
            if route_hash not in route_hashes:
                route_hashes[route_hash] = []
            route_hashes[route_hash].append(route)

        return route_hashes

    def call_route(self, event, **kwargs):
        """
        Calls the appropriate route handler based on the provided path, method, and request.

        Args:
            event (dict): The Lambda event.
            **kwargs: Additional keyword arguments.

        Raises:
            KeyError: If the module or class for the route is not defined well.

        Returns:
            The result of calling the route handler method.
        """

        path, method, request = self.__extract_params(event)

        call, params = self.__get_matching_route(path, method)
        params.update(request)

        call_parts = call.split("/")
        if len(call_parts) != 2:
            raise KeyError(
                f"Module for route {path} with method {method} is not defined well"
            )

        module = call_parts[0]
        mod = importlib.import_module(module)

        class_parts = call_parts[1].split(":")
        if len(class_parts) != 2:
            raise KeyError(
                f"Class for route {path} with method {method} is not defined well"
            )

        class_ = getattr(mod, class_parts[0])

        instance = class_(**kwargs)
        method_ = getattr(instance, class_parts[1])

        return method_(**params)
