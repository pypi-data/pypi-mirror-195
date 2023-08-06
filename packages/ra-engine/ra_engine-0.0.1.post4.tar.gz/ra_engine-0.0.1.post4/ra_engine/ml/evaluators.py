import requests
from ra_engine.core.app import RAEApp
from ra_engine.type_def.ml import TrainData, PredData, MLData, TSData
import pandas as pd


class EvaluatorML:
    def __init__(
        self,
        endpoint: str,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        self.rae_app: RAEApp = app
        self.ml_data = MLData(
            TrainData(train_df, features, targets, train_config),
            PredData(pred_df, pred_config),
        )
        self._app = app.app()
        self.endpoint = endpoint
        self.response = None
        self._json = None
        if self._app is None:
            raise ValueError("RAEApp is not initialized. Please run app.init() first.")
        if self._app.result is None:
            raise ValueError(
                "Provided RAEApp is not authenticated properly. Please check your credentials."
            )
        self.run()

    def run(self):
        self.response = requests.get(
            self.rae_app.credentials.host + self.endpoint,
            json=self.ml_data.as_dict(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._app.result['jwt']}",
            },
        )
        self._json = self.response.json()
        return self.response

    def inputs(self):
        return self.ml_data.as_dict()

    def result(self):
        if self.response.status_code == 200:
            return self._json
        raise Exception(
            "No result available. status_code: "
            + str(self.response.status_code)
            + " "
            + self.response.text
        )

    def predictions(self, as_df=False):
        if self._json is not None:
            res = self._json.get("result", None)
            if res is not None and as_df:
                return pd.DataFrame(res)
            else:
                return res
        else:
            raise Exception("No result available. Please run result() first.")

    def scores(self):
        return self._json.get("score", None)

    def status_code(self):
        return self.response.status_code


class EvaluatorTS:
    def __init__(
        self,
        endpoint: str,
        app: RAEApp,
        train_df: pd.DataFrame,
        dates_col: str,
        target_col: str,
        train_config: dict = None,
        forcast_for: int = 1,
    ):

        self.rae_app: RAEApp = app
        self.ts_data = TSData(
            train_df, dates_col, target_col, train_config, forcast_for
        )
        self._app = app.app()
        self.endpoint = endpoint
        self.response = None
        self._json = None
        if self._app is None:
            raise ValueError("RAEApp is not initialized. Please run app.init() first.")
        if self._app.result is None:
            raise ValueError(
                "Provided RAEApp is not authenticated properly. Please check your credentials."
            )
        self.run()

    def run(self):
        self.response = requests.get(
            self.rae_app.credentials.host + self.endpoint,
            json=self.ts_data.as_dict(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._app.result['jwt']}",
            },
        )

        self._json = self.response.json()
        return self.response

    def inputs(self):
        return self.ts_data.as_dict()

    def result(self):
        if self.response.status_code == 200:
            return self._json
        raise Exception(
            "No result available. status_code: "
            + str(self.response.status_code)
            + " "
            + self.response.text
        )

    def predictions(self, as_df=False):
        if self._json is not None:
            res = self._json.get("result", None)
            if res is not None and as_df:
                return pd.DataFrame(res)
            else:
                return res
        else:
            raise Exception("No result available. Please run result() first.")

    def scores(self):
        return self._json.get("score", None)

    def status_code(self):
        return self.response.status_code
