# SophiasPathBackend

[![wakatime](https://wakatime.com/badge/user/53e0bfc9-ae89-4cb3-99fe-c6cbc6359857/project/9acfc5c5-0ecd-4c7c-a8ef-b4663fc36fdc.svg)](https://wakatime.com/badge/user/53e0bfc9-ae89-4cb3-99fe-c6cbc6359857/project/9acfc5c5-0ecd-4c7c-a8ef-b4663fc36fdc)

This is backend project for [SophiasPath](https://sophiaspath.org)

Powered by [Django REST framework](https://www.django-rest-framework.org/)

## Documents

The following documents are generated by ChatGPT and corrected by myself. Might contain some errors and don't assume it always holds as the project is still under developments [Last update: 2024.09.28]

### Get School List

Fetches a list of schools.

Endpoint: `/getSchoolList`

Method: GET

URL: https://backend.sophiaspath.org/getSchoolList

Example Request:

```bash
curl -X GET "https://backend.sophiaspath.org/getSchoolList" \
-H "Content-Type: application/json"
```

Example Response:

```json
[
    {
        "title": "School of Athens",
        "description": "The School of Athens is a fresco painted by Raphael in 1509-1510 in the Stanza della Segnatura (Room of the Signature) of the Apostolic Palace in the Vatican City.",
        "date_created": "2024-09-28T00:00:00Z",
        "last_edit": "2024-09-28T00:00:00Z"
    },
    ...
]
```

### Get School by Slug

Fetches a school by its slug.

Endpoint: `/getSchool/<str:school_slug>`

Method: GET

URL: https://backend.sophiaspath.org/getSchool/<school_slug>

Example Request:

```bash
curl -X GET "https://backend.sophiaspath.org/getSchool/<str:school_slug>" \
-H "Content-Type: application/json"
```

### Get Development List

Fetches a list of developments.

Endpoint: `/getDevelopmentList`

Method: GET

URL: https://backend.sophiaspath.org/getDevelopmentList

Example Request:

```bash
curl -X GET "https://backend.sophiaspath.org/getDevelopmentList" \
-H "Content-Type: application/json"
```

Example Response:

```json
[
    {
        "start_school_id": 1,
        "end_school_id": 2,
        "name": "Founding",
        "description": "The School of Athens is a fresco painted by Raphael in 1509-1510 in the Stanza della Segnatura (Room of the Signature) of the Apostolic Palace in the Vatican City.",
        "date_created": "2024-09-28T00:00:00Z",
        "last_edit": "2024-09-28T00:00:00Z"
    },
    ...
]
```

### Get Developments by School

Fetches a list of developments associated with a specific school.

Endpoint: `/getDevelopmentBySchool/<str:school_slug>`

Method: GET

URL: https://backend.sophiaspath.org/getDevelopmentBySchool/<school_slug>

Example Request:

```bash
curl -X GET "https://backend.sophiaspath.org/getDevelopmentBySchool/<str:school_slug>" \
-H "Content-Type: application/json"
```

### Get Philosophers by School

Fetches a list of philosophers associated with a specific school.

Endpoint: `/getPhilosophers/<int:school_slug>`

Method: GET

URL: https://backend.sophiaspath.org/getPhilosophers/<int:school_slug>

Example Request:

```bash
curl -X GET "https://backend.sophiaspath.org/getPhilosophers/<int:school_slug>" \
-H "Content-Type: application/json"
```

Example Response:

```json
[
    {
        "title": "Socrates",
        "school_id": 1,
        "description": "Socrates was an ancient Greek philosopher credited as the founder of Western philosophy. He was a student of Plato and the teacher of Aristotle.",
        "date_created": "2024-09-28T00:00:00Z",
        "last_edit": "2024-09-28T00:00:00Z"
    },
    ...
]
```

### Get Philosopher by Slug

Fetches a philosopher by its slug.

Endpoint: `/getPhilosopher/<str:philosopher_slug>` 

Method: GET

URL: https://backend.sophiaspath.org/getPhilosopher/<str:philosopher_slug>

Example Request:

```bash
curl -X GET "https://backend.sophiaspath.org/getPhilosopher/<str:philosopher_slug>" \
-H "Content-Type: application/json"
```

Example Response:

```json
[
    {
        "title": "Socrates",
        "school_id": 1,
        "description": "Socrates was an ancient Greek philosopher credited as the founder of Western philosophy. He was a student of Plato and the teacher of Aristotle.",
        "date_created": "2024-09-28T00:00:00Z",
        "last_edit": "2024-09-28T00:00:00Z"
    }
]
```

### Get Affiliations

Fetches affiliations for a specific philosopher.

Endpoint: `/getAffiliations/<int:philosopher_pk>`

Method: GET

URL: https://backend.sophiaspath.org/getAffiliations/<philosopher_pk>

Example Request:

``` bash
curl -X GET "https://backend.sophiaspath.org/getAffiliations/1" \
-H "Content-Type: application/json"
```

Replace `1` with the appropriate philosopher_pk.

### Get Sections by Philosopher

Fetches sections associated with a specific philosopher.

Endpoint: `/getSections/<int:philosopher_pk>`

Method: GET

URL: https://backend.sophiaspath.org/getSections/<philosopher_pk>

Example Request:

```bash
curl -X GET "https://backend.sophiaspath.org/getSections/1" \
-H "Content-Type: application/json"
```

Replace `1` with the appropriate philosopher_pk.

### Get Relations List

Fetches the relations associated with a specific philosopher.

Endpoint: `/getRelationsList/<int:philosopher_pk>`

Method: GET

URL: https://backend.sophiaspath.org/getRelationsList/<philosopher_pk>

Example Request:

``` bash
curl -X GET "https://backend.sophiaspath.org/getRelationsList/1" \
-H "Content-Type: application/json"
```

Replace `1` with the appropriate philosopher_pk.

### Get Tags

Fetches a unique list of tags.

Endpoint: `/getTags`

Method: GET

URL: https://backend.sophiaspath.org/getTags

Example Request:

``` bash
curl -X GET "https://backend.sophiaspath.org/getTags" \
-H "Content-Type: application/json"
```

### Get Sections by Tag
Fetches sections associated with a specific tag.

Endpoint: `/getSectionsByTag/<int:tag_pk>`

Method: GET

URL: https://backend.sophiaspath.org/getSectionsByTag/<tag_pk>

Example Request:

```bash
curl -X GET "https://backend.sophiaspath.org/getSectionsByTag/1" \
-H "Content-Type: application/json" 
```
Replace `1` with the appropriate tag_pk.
