import importer


testEvents = [
    {
        "name": "Normal Event",
        "summary": "I have a summary",
        "description": "I have a description",
        "start": {
            "dateTime": "2023-03-25T18:00:00-06:00"
        },
        "end" : {
            "dateTime": "2023-03-25T20:00:00-06:00"
        }
    },
    {
        "name": "Event without summary",
        "description": "I have a description",
        "start": {
            "dateTime": "2023-03-25T18:00:00-06:00"
        },
        "end" : {
            "dateTime": "2023-03-25T20:00:00-06:00"
        }
    },
    {
        "name": "Event without description",
        "summary": "I have a summary",
        "start": {
            "dateTime": "2023-03-25T18:00:00-06:00"
        },
        "end" : {
            "dateTime": "2023-03-25T20:00:00-06:00"
        }
    },
    {
        "name": "Event without start",
        "summary": "I have a summary",
        "description": "I have a description",
        "end" : {
            "dateTime": "2023-03-25T20:00:00-06:00"
        }
    },
    {
        "name": "Event without end",
        "summary": "I have a summary",
        "description": "I have a description",
        "start": {
            "dateTime": "2023-03-25T18:00:00-06:00"
        }
    },
    {
        "name": "Event without start dateTime",
        "summary": "I have a summary",
        "description": "I have a description",
        "start": {
        },
        "end" : {
            "dateTime": "2023-03-25T20:00:00-06:00"
        }
    },
    {
        "name": "Event without end dateTime",
        "summary": "I have a summary",
        "description": "I have a description",
        "start": {
            "dateTime": "2023-03-25T18:00:00-06:00"
        },
        "end" : {
        }
    },
    {
        "name": "Event with incorrect start dateTime format",
        "summary": "I have a summary",
        "description": "I have a description",
        "start": {
            "dateTime": "2023-03-25T18"
        },
        "end" : {
            "dateTime": "2023-03-25T20:00:00-06:00"
        }
    },
    {
        "name": "Event with incorrect end dateTime format",
        "summary": "I have a summary",
        "description": "I have a description",
        "start": {
            "dateTime": "2023-03-25T18:00:00-06:00"
        },
        "end" : {
            "dateTime": "2023-03-25T20"
        }
    }
]


for testEvent in testEvents:
    print("-----------------------------------------------")
    print(f'Testing {testEvent["name"]}')
    importer.eventVerifier(testEvent)
    print("-----------------------------------------------")