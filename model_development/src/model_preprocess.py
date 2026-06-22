from typing import Any


class Preprocess:
    """Preprocessing and postprocessing hooks called by ClearML Serving per request."""

    def preprocess(
        self, body: dict, _state: dict, _collect_custom_statistics_fn=None
    ) -> Any:
        return [body.get("text", "")]

    def postprocess(
        self, data: Any, _state: dict, _collect_custom_statistics_fn=None
    ) -> dict:
        if hasattr(data, 'tolist'):
            data = data.tolist()
        
        # If data is a list, get the first element
        if isinstance(data, list):
            prediction = data[0]
        else:
            prediction = data
            
        return {"label": str(prediction)}