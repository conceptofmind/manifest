"""Dummy client."""
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple

from manifest.clients.client import Client
from manifest.request import Request

logger = logging.getLogger(__name__)


class DummyClient(Client):
    """Dummy client."""

    # User param -> (client param, default value)
    PARAMS = {
        "n": ("num_results", 1),
    }

    def connect(
        self,
        connection_str: Optional[str] = None,
        client_args: Dict[str, Any] = {},
    ) -> None:
        """
        Connect to dummpy server.

        This is a dummy client that returns identity responses. Used for testing.

        Args:
            connection_str: connection string.
            client_args: client arguments.
        """
        for key in self.PARAMS:
            setattr(self, key, client_args.pop(key, self.PARAMS[key][1]))

    def close(self) -> None:
        """Close the client."""
        pass

    def get_generation_url(self) -> str:
        """Get generation URL."""
        return "dummy"

    def supports_batch_inference(self) -> bool:
        """Return whether the client supports batch inference."""
        return True

    def get_generation_header(self) -> Dict[str, str]:
        """
        Get generation header.

        Returns:
            header.
        """
        return {}

    def get_model_params(self) -> Dict:
        """
        Get model params.

        By getting model params from the server, we can add to request
        and make sure cache keys are unique to model.

        Returns:
            model params.
        """
        return {"engine": "dummy"}

    def get_request(self, request: Request) -> Tuple[Callable[[], Dict], Dict]:
        """
        Get request string function.

        Args:
            request: request.

        Returns:
            request function that takes no input.
            request parameters as dict.
        """
        if isinstance(request.prompt, list):
            num_results = len(request.prompt)
        else:
            num_results = 1
        request_params = request.to_dict(self.PARAMS)

        def _run_completion() -> Dict:
            return {
                "choices": [{"text": "hello"}]
                * int(request_params["num_results"])
                * num_results
            }

        return _run_completion, request_params

    def get_choice_logit_request(
        self,
        gold_choices: List[str],
        request: Request,
    ) -> Tuple[Callable[[], Dict], Dict]:
        """
        Get request string function for choosing max choices.

        Args:
            gold_choices: choices for model to choose from via max logits.
            request: request.

        Returns:
            request function that takes no input.
            request parameters as dict.
        """
        if isinstance(request.prompt, list):
            num_results = len(request.prompt)
        else:
            num_results = 1
        request_params = {"prompt": request.prompt, "gold_choices": gold_choices}

        def _run_completion() -> Dict:
            return {"choices": [{"text": gold_choices[0]}] * num_results}

        return _run_completion, request_params
