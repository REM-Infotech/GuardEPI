## Arquivo Configurações

### Defina o dominio do cliente onde estiver 'https://domain.cliente.com'

#### Exemplo:

```python

def csp() -> dict[str]:

    csp_vars = {
    'default-src': [
        '\'self\''
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://cdn.datatables.net',
        'https://unpkg.com',
        'https://code.jquery.com',
        'https://use.fontawesome.com',
        '',
        '\'unsafe-inline\'',
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://cdn.datatables.net',
        'https://unpkg.com',
        '\'unsafe-inline\'',
    ],
    'img-src': [
        '\'self\'',
        'data:',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://cdn.datatables.net',
        'https://unpkg.com',
        'https://cdn-icons-png.flaticon.com',
        'https://domain.cliente.com',
    ],
    'connect-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://cdn.datatables.net',
        'https://unpkg.com',
    ],
    'frame-src': [
        '\'self\'',
        'https://domain.cliente.com',
    ]
}


```

### A def "debugmode" fica inalterada, as configurações dela são feitas via arquivo `.env` 

#### Exemplo

```python

def debugmode() -> bool:

    debug = os.getenv('DEBUG', 'False').lower() in (
        'true', '1', 't', 'y', 'yes')
    return debug

```

```.env

DEBUG = True 


## DEBUG MODE EM PROD TEM QUE SER FALSE!!!

```