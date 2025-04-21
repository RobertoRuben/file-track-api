class Scopes:

    DOCUMENT_CATEGORY_READ = "document_category:read"
    DOCUMENT_CATEGORY_CREATE = "document_category:create"
    DOCUMENT_CATEGORY_UPDATE = "document_category:update"
    DOCUMENT_CATEGORY_DELETE = "document_category:delete"

    ROLE_READ = "role:read"
    ROLE_CREATE = "role:create"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"

    DEPARTMENT_READ = "department:read"
    DEPARTMENT_CREATE = "department:create"
    DEPARTMENT_UPDATE = "department:update"
    DEPARTMENT_DELETE = "department:delete"

    DOCUMENTARY_TOPIC_READ = "documentary_topic:read"
    DOCUMENTARY_TOPIC_CREATE = "documentary_topic:create"
    DOCUMENTARY_TOPIC_UPDATE = "documentary_topic:update"
    DOCUMENTARY_TOPIC_DELETE = "documentary_topic:delete"

    SETTLEMENT_READ = "settlement:read"
    SETTLEMENT_CREATE = "settlement:create"
    SETTLEMENT_UPDATE = "settlement:update"
    SETTLEMENT_DELETE = "settlement:delete"

    SUBMITTER_READ = "submitter:read"
    SUBMITTER_CREATE = "submitter:create"
    SUBMITTER_UPDATE = "submitter:update"
    SUBMITTER_DELETE = "submitter:delete"

    POSITION_READ = "position:read"
    POSITION_CREATE = "position:create"
    POSITION_UPDATE = "position:update"
    POSITION_DELETE = "position:delete"

    EMPLOYEE_READ = "employee:read"
    EMPLOYEE_CREATE = "employee:create"
    EMPLOYEE_UPDATE = "employee:update"
    EMPLOYEE_DELETE = "employee:delete"

    HAMLET_READ = "hamlet:read"
    HAMLET_CREATE = "hamlet:create"
    HAMLET_UPDATE = "hamlet:update"
    HAMLET_DELETE = "hamlet:delete"

    DEPARTMENT_CONNECTION_READ = "department_connection:read"
    DEPARTMENT_CONNECTION_CREATE = "department_connection:create"
    DEPARTMENT_CONNECTION_UPDATE = "department_connection:update"
    DEPARTMENT_CONNECTION_DELETE = "department_connection:delete"

    USER_READ = "user:read"
    USER_CREATE = "user:create"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"

    DOCUMENT_READ = "document:read"
    DOCUMENT_CREATE = "document:create"
    DOCUMENT_UPDATE = "document:update"
    DOCUMENT_DELETE = "document:delete"

    ROLE_SCOPES = {
        "SUPER ADMIN": [
            DOCUMENT_CATEGORY_READ,
            DOCUMENT_CATEGORY_CREATE,
            DOCUMENT_CATEGORY_UPDATE,
            DOCUMENT_CATEGORY_DELETE,
            ROLE_READ,
            ROLE_CREATE,
            ROLE_UPDATE,
            ROLE_DELETE,
            DEPARTMENT_READ,
            DEPARTMENT_CREATE,
            DEPARTMENT_UPDATE,
            DEPARTMENT_DELETE,
            DOCUMENTARY_TOPIC_READ,
            DOCUMENTARY_TOPIC_CREATE,
            DOCUMENTARY_TOPIC_UPDATE,
            DOCUMENTARY_TOPIC_DELETE,
            SETTLEMENT_READ,
            SETTLEMENT_CREATE,
            SETTLEMENT_UPDATE,
            SETTLEMENT_DELETE,
            SUBMITTER_READ,
            SUBMITTER_CREATE,
            SUBMITTER_UPDATE,
            SUBMITTER_DELETE,
            POSITION_READ,
            POSITION_CREATE,
            POSITION_UPDATE,
            POSITION_DELETE,
            EMPLOYEE_READ,
            EMPLOYEE_CREATE,
            EMPLOYEE_UPDATE,
            EMPLOYEE_DELETE,
            HAMLET_READ,
            HAMLET_CREATE,
            HAMLET_UPDATE,
            HAMLET_DELETE,
            DEPARTMENT_CONNECTION_READ,
            DEPARTMENT_CONNECTION_CREATE,
            DEPARTMENT_CONNECTION_UPDATE,
            DEPARTMENT_CONNECTION_DELETE,
            USER_READ,
            USER_CREATE,
            USER_UPDATE,
            USER_DELETE,
            DOCUMENT_READ,
            DOCUMENT_CREATE,
            DOCUMENT_UPDATE,
            DOCUMENT_DELETE,
        ],
        "ADMIN": [
            USER_READ,
            USER_CREATE,
            USER_UPDATE,
            USER_DELETE,
            DEPARTMENT_CONNECTION_READ,
            DOCUMENT_CATEGORY_READ,
            DOCUMENT_CATEGORY_CREATE,
            DOCUMENT_CATEGORY_UPDATE,
            DOCUMENT_CATEGORY_DELETE,
            DOCUMENTARY_TOPIC_READ,
            DOCUMENTARY_TOPIC_CREATE,
            DOCUMENTARY_TOPIC_UPDATE,
            DOCUMENTARY_TOPIC_DELETE,
            EMPLOYEE_READ,
            EMPLOYEE_CREATE,
            EMPLOYEE_UPDATE,
            EMPLOYEE_DELETE,
            DOCUMENT_READ,
            DOCUMENT_CREATE,
            DOCUMENT_UPDATE,
        ],
        "MESA DE PARTES": [
            DOCUMENT_CATEGORY_READ,
            DOCUMENT_CATEGORY_CREATE,
            DOCUMENT_CATEGORY_UPDATE,
            DOCUMENTARY_TOPIC_READ,
            DOCUMENTARY_TOPIC_CREATE,
            DOCUMENTARY_TOPIC_UPDATE,
            DOCUMENTARY_TOPIC_DELETE,
            DOCUMENT_READ,
            DOCUMENT_CREATE,
            DOCUMENT_UPDATE,
            DOCUMENT_DELETE,
        ],
    }


scope_descriptions = {
    "document_category:read": "Read document category details",
    "document_category:create": "Create new document categories",
    "document_category:update": "Update document categories",
    "document_category:delete": "Delete document categories",
    "role:read": "Read role information",
    "role:create": "Create new roles",
    "role:update": "Update existing roles",
    "role:delete": "Delete roles",
    "department:read": "Read department information",
    "department:create": "Create new departments",
    "department:update": "Update existing departments",
    "department:delete": "Delete departments",
    "documentary_topic:read": "Read documentary topics information",
    "documentary_topic:create": "Create new documentary topics",
    "documentary_topic:update": "Update documentary topics",
    "documentary_topic:delete": "Delete documentary topics",
    "settlement:read": "Read settlements",
    "settlement:create": "Create settlements",
    "settlement:update": "Update settlements",
    "settlement:delete": "Delete settlements",
    "submitter:read": "Read submitter information",
    "submitter:create": "Create submitters",
    "submitter:update": "Update submitters",
    "submitter:delete": "Delete submitters",
    "position:read": "Read position information",
    "position:create": "Create new positions",
    "position:update": "Update positions",
    "position:delete": "Delete positions",
    "employee:read": "Read employee information",
    "employee:create": "Create new employees",
    "employee:update": "Update employees",
    "employee:delete": "Delete employees",
    "hamlet:read": "Read hamlet information",
    "hamlet:create": "Create new hamlets",
    "hamlet:update": "Update hamlets",
    "hamlet:delete": "Delete hamlets",
    "department_connection:read": "Read department connection information",
    "department_connection:create": "Create department connections",
    "department_connection:update": "Update department connections",
    "department_connection:delete": "Delete department connections",
    "user:read": "Read user information",
    "user:create": "Create new users",
    "user:update": "Update users",
    "user:delete": "Delete users",
    "document:read": "Read document information",
    "document:create": "Create new documents",
    "document:update": "Update documents",
    "document:delete": "Delete documents",
}
