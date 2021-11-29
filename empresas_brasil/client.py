"""Provides functions to query companies from Brazil."""
from typing import List, Union

import click
import requests
import pandas as pd


class BrazilCompanyClient():

    def __init__(self, api_key: str = "ea67d6a65emshb685a95313a55ccp1b132bjsnb5e966cbb0cf") -> None:
        """Brazilian Company API client.

        This service class provides functions to query companies from Brazil using the following API:
            - https://rapidapi.com/brapi/api/empresas

        Args:
            api_key: the RapidAPI key to authenticate the requests.
        """
        self._api_default_method = "GET"
        self._api_url = 'https://empresas.p.rapidapi.com/'
        self._api_headers = {
            'x-rapidapi-host': "empresas.p.rapidapi.com",
            'x-rapidapi-key': api_key
        }

    def get_one(self, tax_id: str) -> dict:
        """Collect one company by its tax ID from the API.

        Args:
            tax_id: Company tax ID (CNPJ).

        Returns:
            A dict with company information as the schema below:
            ```
            {
                "type": "object",
                "properties": {
                    "taxIdNumber": {
                        "type": "string",
                        "description": "Número do documento (CNPJ no Brasil)"
                    },
                    "officialName": {
                        "type": "string",
                        "description": "Nome oficial (razão social) da empresa"
                    },
                    "tradeName": {
                        "type": "string",
                        "description": "Nome fantasia da empresa"
                    },
                    "creationDate": {
                        "type": "string",
                        "description": "Data de criação do registro referente a empresa"
                    },
                    "size": {
                        "type": "string",
                        "description": "Porte da empresa"
                    },
                    "legalNature": {
                        "type": "string",
                        "description": "Descrição da natureza jurídica da empresa"
                    },
                    "meiOptant": {
                        "type": "string",
                        "description": "Indicador da existência da opção pelo Microempreendedor Individual (MEI)"
                    },
                    "simplesOptant": {
                        "type": "string",
                        "description": "Indicador da existência da opção pelo registro tributário Simples Nacional"
                    },
                    "partnershipType": {
                        "type": "string",
                        "description": " Indicador se é Matriz ou Filial"
                    },
                    "taxIdStatus": {
                        "type": "string",
                        "description": "Status da empresa na Receita Federal"
                    },
                    "taxIdStatusDate": {
                        "type": "string",
                        "description": "Data de atualização do status da empresa na Receita Federal"
                    },
                    "addressStreet": {
                        "type": "string",
                        "description": "'Nome do logradouro onde se localiza a empresa"
                    },
                    "addressDetails": {
                        "type": "string",
                        "description": "Complemento para o endereço de localização da empresa"
                    },
                    "addressNeighborhood": {
                        "type": "string",
                        "description": "Bairro onde se localiza a empresa"
                    },
                    "addressZipCode": {
                        "type": "string",
                        "description": "Código de endereçamento postal referente ao logradouro no qual a empresa esta localizada."
                    },
                    "addressCity": {
                        "type": "string",
                        "description": "Município de jurisdição onde se encontra a empresa"
                    },
                    "addressState": {
                        "type": "string",
                        "description": "Unidade da federação em que se encontra a empresa"
                    },
                    "economicActivities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "description": "Lista de atividades econômicas registradas pela empresa",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "Código da atividade econômica"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Descrição atividade econômica"
                                },
                                "isMain": {
                                    "type": "string",
                                    "description": "Indicador se atividade econômica é primária"
                                }
                            }
                        }
                    }
                }
            }
            ```

        Raises:
            HTTPError: if the response status code is not HTTP 200.
        """
        url = f'{self._api_url}/{tax_id}'

        response = requests.request(method=self._api_default_method, url=url, headers=self._api_headers)

        if response.status_code == 200:
            return response.json()

        raise response.raise_for_status()

    def get_many(self, tax_ids: List[str], as_dataframe: bool=False) -> Union[List[dict], pd.DataFrame]:
        """Collect many companies cadastral information by their tax IDs from the API.

        See doc `BrazilCompanyClient:get_one` class for more information about the company schema.

        Args:
            tax_ids: Company tax IDs (CNPJs).
            as_dataframe: `as_dataframe==False` returns the result as a `List`. Otherwise, returns as `pd.Dataframe`

        Returns:
            Cadastral information of companies.

        Raises:
            HTTPError: if the response status code is not HTTP 200.
        """
        companies =  [self.get_one(cnpj) for cnpj in tax_ids if cnpj]

        if as_dataframe:
            companies = pd.DataFrame(data=companies)

        return companies

    def export(self, tax_ids: List[str], result_path: str):
        """
        Args:
            tax_ids: Company tax IDs (CNPJs).
            result_path: file path specifying a mimetype (eg .csv or .json) to store company collection

        Raises:
            ValueError: if result path is not defined (None).
            SyntaxError: if result path mimetype is not specified.
            NotImplementedError: if result path mimetype is not supported.
        """
        if not result_path:
            raise ValueError("Result path param is not defined.")

        if "." not in result_path:
            raise SyntaxError("Result path mimetype (eg .csv or .json) is not specified in path.")

        format = result_path.split(".")[-1]

        if format not in ("csv", "json"):
            raise NotImplementedError(f"Result path mimetype `.{format}` is not supported.")

        companies = self.get_many(tax_ids=tax_ids, as_dataframe=True)

        if format == "csv":
            companies.to_csv(result_path, index=False)
        elif format == "json":
            companies.to_json(result_path, orient="records")


@click.command()
@click.option("-i", "--id", type=str, multiple=True, help="Company public tax ID (CNPJ)")
@click.option("-p", "--path", type=str, help="File path to save the collection result")
@click.option("-k", "--key", required=True, type=str, help="The Rapid API key")
def run(
    id: List[str],
    path: str,
    key: str,
) -> None:
    """Runs the Brazilian Company Client."""
    service = BrazilCompanyClient(api_key=key)
    service.export(tax_ids=id, result_path=path)


if __name__ == "__main__":
    run()
