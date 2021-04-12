from fastapi import status

responses = {
    status.HTTP_201_CREATED: {
        "description": "Элемент создан",
        "content": {
            "application/json": {
                "example": {
                    "message": "created"
                }
            }
        }},
    status.HTTP_400_BAD_REQUEST: {
        "description": "Неверный формат входных данных",
        "content": {
            "application/json": {
                "example": {
                    "message": "bad request"
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Запрашиваемый ресурс не найден",
        "content": {
            "application/json": {
                "example": {
                    "message": "Not found"
                }
            }
        }
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Ошибка сервера",
        "content": {
            "application/json": {
                "example": {
                    "message": "Internal Server Error"
                }
            }
        }
    }
}
