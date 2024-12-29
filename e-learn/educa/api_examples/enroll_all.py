import requests

username = ''
password = ''

# Define the base URL for the API
base_url = 'http://127.0.0.1:8000/api/'
# Construct the URL for accessing the courses endpoint
url = f'{base_url}courses/'
# Initialize an empty list to store the titles of available courses
available_courses = []

# Loop to fetch courses as long as there are more pages (pagination)
while url is not None:
    print(f'Loading courses from {url}')
    # Send a GET request to the current URL to fetch courses data
    r = requests.get(url)
    # Parse the JSON response from the API
    response = r.json()
    # Update the URL to the 'next' page if available (for pagination)
    url = response['next']
    # Extract the list of courses from the response
    courses = response['results']
    # Add the titles of the courses to the available_courses list
    available_courses += [course['title'] for course in courses]
# Print all available courses once the data has been loaded
print(f'Available courses: {", ".join(available_courses)}')

# Iterate over each course in the 'courses' list
for course in courses:
    # Get the 'id' and 'title' of the current course
    course_id = course['id']
    course_title = course['title']
    # Send a POST request to the course's enrollment endpoint
    # 'auth' is used to authenticate the request using the provided username and password
    r = requests.post(
        f'{base_url}courses/{course_id}/enroll/',  # Endpoint for enrolling in the course
        auth=(username, password)  # Authentication using username and password
    )
    # Check if the enrollment request was successful (HTTP status code 200)
    if r.status_code == 200:
        # If the request was successful, print a message confirming enrollment
        print(f'Successfully enrolled in {course_title}')
