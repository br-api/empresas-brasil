# Empresas do Brasil (CNPJs)

Biblioteca em Python que coleta informações cadastrais de empresas do Brasil (CNPJ) obtidas de fontes oficiais (Receita Federal do Brasil - RFB) e exporta para um formato legível por humanos (CSV ou JSON).

> Python library that collects cadastral information of companies from Brazil (CNPJ) provided by official sources (Federal Revenue of Brazil - RFB) and exports results to a human-readable format (CSV or JSON).

## Instalação

```bash
pip install -e git+https://github.com/br-api/empresas-brasil.git
```

## Biblioteca

Esta biblioteca é um cliente da [API Empresas do Brasil](https://rapidapi.com/brapi/api/empresas/) fornecida via plataforma [RapidAPI](https://rapidapi.com/). Para usa-lá é necessário a criação de um usuário no RapidAPI e assinatura da API para obter uma chave privada para fazer requisições HTTP. Porém, para fins didáticos, você pode usar a seguinte chave de maneira gratuita:
- `RAPID_API_KEY=ea67d6a65emshb685a95313a55ccp1b132bjsnb5e966cbb0cf`

Exemplo para coletar informações de uma única empresa pelo CNPJ:

``` python
>>> from empresas_brasil.client import BrazilCompanyClient
>>> client = BrazilCompanyClient(api_key="ea67d6a65emshb685a95313a55ccp1b132bjsnb5e966cbb0cf")
>>> companies = client.get_many(
    tax_ids=["00394460005887"] # CNPJ
)
```

Exemplo para coletar informações de múltiplas empresas pelo CNPJ:

``` python
>>> from empresas_brasil.client import BrazilCompanyClient
>>> client = BrazilCompanyClient(api_key="ea67d6a65emshb685a95313a55ccp1b132bjsnb5e966cbb0cf")
>>> companies = client.get_many(
    tax_ids=["00394460005887", "00396895004201"] # CNPJs
)
```

# CLI

Como alternativa, use o comando abaixo em um terminal para armazenar os resultados num arquivo `.csv`:

```bash
export RAPID_API_KEY=ea67d6a65emshb685a95313a55ccp1b132bjsnb5e966cbb0cf
empresas_brasil --key $RAPID_API_KEY --id 00394460005887 --id 00396895004201 --path exemplo.csv
```

Ou use o comando abaixo em um terminal para armazenar os resultados num arquivo `.json`:

```bash
empresas_brasil --key $RAPID_API_KEY --id 00394460005887 --id 00396895004201 --path exemplo.json
```

## Schema

Schema de informações coletadas de uma empresa:

```json
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

## Referência

- https://rapidapi.com/brapi/api/empresas

## Licença
A licença do código é LGPL3 e dos dados convertidos Creative Commons Attribution ShareAlike. Caso utilize os dados, cite a fonte original e quem tratou os dados, como: Fonte: Receita Federal do Brasil. Caso compartilhe os dados, utilize a mesma licença.
