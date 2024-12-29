import requests

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
